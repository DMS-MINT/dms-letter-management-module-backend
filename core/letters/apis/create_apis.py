from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.exceptions import APIError
from core.api.mixins import ApiAuthMixin
from core.authentication.services import verify_otp
from core.letters.serializers import LetterCreateSerializer, LetterDetailPolymorphicSerializer
from core.letters.services.create_services import letter_create, letter_create_and_publish
from core.permissions.mixins import ApiPermMixin
from core.workflows.services import letter_submit


class LetterCreateApi(ApiAuthMixin, ApiPermMixin, APIView):
    serializer_class = LetterCreateSerializer

    def post(self, request) -> Response:
        input_serializer = LetterCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_instance = letter_create(current_user=request.user, **input_serializer.validated_data)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            output_serializer = LetterDetailPolymorphicSerializer(letter_instance)
            response_data = {"letter": output_serializer.data, "permissions": permissions}

            return Response(data=response_data, status=http_status.HTTP_201_CREATED)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterCreateAndSubmitApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_submit_letter"]

    class InputSerializer(serializers.Serializer):
        letter = LetterCreateSerializer()
        otp = serializers.CharField()

    serializer_class = InputSerializer

    def post(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            otp = input_serializer.validated_data.pop("otp")
            verify_otp(current_user=request.user, otp=otp)

            letter_data = input_serializer.validated_data.pop("letter")

            letter_instance = letter_create(current_user=request.user, **letter_data)

            response_message = "Warning: The letter has been successfully created but has not yet been submitted."
            status_code = http_status.HTTP_201_CREATED

            try:
                self.check_object_permissions(request, letter_instance)
                letter_instance = letter_submit(
                    current_user=request.user,
                    letter_instance=letter_instance,
                    signature_method="Default",
                )
                response_message = "Success: The letter has been successfully created and submitted."
                status_code = http_status.HTTP_200_OK
            except Exception as e:
                raise e

            output_serializer = LetterDetailPolymorphicSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {
                "message": response_message,
                "letter": output_serializer.data,
                "permissions": permissions,
            }

            return Response(data=response_data, status=status_code)

        except APIError as e:
            raise APIError(e.error_code, e.status_code, e.message, e.extra)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterCreateAndPublish(ApiAuthMixin, ApiPermMixin, APIView):
    permission_classes = [IsAdminUser]

    class InputSerializer(serializers.Serializer):
        letter = LetterCreateSerializer()
        otp = serializers.CharField()

    serializer_class = InputSerializer

    def post(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            otp = input_serializer.validated_data.pop("otp")
            verify_otp(current_user=request.user, otp=otp)

            letter_data = input_serializer.validated_data.pop("letter")
            letter_instance = letter_create_and_publish(current_user=request.user, **letter_data)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            output_serializer = LetterDetailPolymorphicSerializer(letter_instance)

            response_data = {
                "message": "The letter has been successfully created and distributed to all recipients.",
                "data": output_serializer.data,
                "permissions": permissions,
            }

            return Response(data=response_data, status=http_status.HTTP_201_CREATED)

        except APIError as e:
            raise APIError(e.error_code, e.status_code, e.message, e.extra)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
