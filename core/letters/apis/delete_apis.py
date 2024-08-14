from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.exceptions import APIError
from core.api.mixins import ApiAuthMixin
from core.authentication.services import verify_otp
from core.common.utils import get_object
from core.letters.models import Letter
from core.letters.serializers import LetterDetailPolymorphicSerializer
from core.letters.services.delete_services import letter_hide, letter_move_to_trash, letter_restore_from_trash
from core.permissions.mixins import ApiPermMixin


class LetterTrashApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_trash_letter"]

    serializer_class = LetterDetailPolymorphicSerializer

    def put(self, request, reference_number) -> Response:
        try:
            letter_instance = get_object(Letter, reference_number=reference_number)
            self.check_object_permissions(request, letter_instance)

            letter_instance = letter_move_to_trash(letter_instance=letter_instance)

            output_serializer = LetterDetailPolymorphicSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {"message": "The Letter has been moved to the trash."}

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"letter_{reference_number}",
                {
                    "type": "letter_update",
                    "message": {
                        "data": output_serializer.data,
                        "permissions": permissions,
                    },
                },
            )

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterRestoreApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_restore_letter"]

    serializer_class = LetterDetailPolymorphicSerializer

    def put(self, request, reference_number) -> Response:
        try:
            letter_instance = get_object(Letter, reference_number=reference_number)
            self.check_object_permissions(request, letter_instance)

            letter_instance = letter_restore_from_trash(letter_instance=letter_instance)

            output_serializer = LetterDetailPolymorphicSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {"message": "The Letter has been restored from the trash."}

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"letter_{reference_number}",
                {
                    "type": "letter_update",
                    "message": {
                        "data": output_serializer.data,
                        "permissions": permissions,
                    },
                },
            )

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterDeleteApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_permanently_delete_letter"]

    class InputSerializer(serializers.Serializer):
        otp = serializers.CharField()

    serializer_class = InputSerializer

    def put(self, request, reference_number) -> Response:
        try:
            letter_instance = get_object(Letter, reference_number=reference_number)
            self.check_object_permissions(request, letter_instance)

            input_serializer = self.InputSerializer(data=request.data)
            input_serializer.is_valid(raise_exception=True)

            result = verify_otp(current_user=request.user, **input_serializer.validated_data)

            if not result:
                raise ValueError("Invalid OTP provided.")

            letter_hide(letter_instance=letter_instance)

            response_data = {"message": "The Letter has been deleted successfully."}

            return Response(data=response_data, status=http_status.HTTP_204_NO_CONTENT)

        except APIError as e:
            raise APIError(e.error_code, e.status_code, e.message, e.extra)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
