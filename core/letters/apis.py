from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse
from guardian.shortcuts import assign_perm
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_polymorphic.serializers import PolymorphicSerializer

from core.api.exceptions import APIError
from core.api.mixins import ApiAuthMixin
from core.authentication.services import verify_otp
from core.common.utils import get_object
from core.permissions.mixins import ApiPermMixin
from core.workflows.services import letter_submit

from .models import Incoming, Internal, Letter, Outgoing
from .selectors import letter_list, letter_pdf
from .serializers import (
    LetterCreateSerializer,
    LetterDetailSerializer,
    LetterListSerializer,
    OutgoingLetterDetailSerializer,
)
from .services import (
    letter_create,
    letter_create_and_publish,
    letter_hide,
    letter_move_to_trash,
    letter_restore_from_trash,
    letter_update,
)
from .utils import process_request_data


class LetterPDF(APIView):
    def get(self, request, reference_number) -> Response:
        letter_instance = get_object(Letter, reference_number=reference_number)

        try:
            pdf_content = letter_pdf(letter_instance=letter_instance)

            response = HttpResponse(pdf_content, content_type="application/pdf")
            response["Content-Disposition"] = f'inline; filename="letter_{letter_instance.reference_number}.pdf"'
            return response

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterListApi(ApiAuthMixin, APIView):
    class FilterSerializer(serializers.Serializer):
        category = serializers.ChoiceField(
            choices=["inbox", "outbox", "draft", "trash", "pending", "published"],
            required=True,
        )

    class OutputSerializer(PolymorphicSerializer):
        resource_type_field_name = "letter_type"
        model_serializer_mapping = {
            Internal: LetterListSerializer,
            Incoming: LetterListSerializer,
            Outgoing: LetterListSerializer,
        }

        def to_resource_type(self, model_or_instance):
            return model_or_instance._meta.object_name.lower()

    serializer_class = FilterSerializer

    def get(self, request) -> Response:
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        letter_instances = letter_list(current_user=request.user, filters=filter_serializer.validated_data)

        serializer = self.OutputSerializer(letter_instances, many=True)

        response_data = {"letters": serializer.data}

        return Response(data=response_data, status=http_status.HTTP_200_OK)


class LetterDetailApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter"]

    class OutputSerializer(PolymorphicSerializer):
        resource_type_field_name = "letter_type"
        model_serializer_mapping = {
            Internal: LetterDetailSerializer,
            Incoming: LetterDetailSerializer,
            Outgoing: OutgoingLetterDetailSerializer,
        }

        def to_resource_type(self, instance):
            return instance._meta.object_name.lower()

    serializer_class = OutputSerializer

    def get(self, request, reference_number) -> Response:
        current_user = request.user
        letter_instance = get_object(Letter, reference_number=reference_number)

        if isinstance(letter_instance, Incoming):
            if request.user.is_staff:
                assign_perm("can_view_letter", request.user, letter_instance)
                assign_perm("can_reject_letter", request.user, letter_instance)
                assign_perm("can_publish_letter", request.user, letter_instance)

        else:
            if request.user.is_staff and letter_instance.current_state in [
                Letter.States.SUBMITTED,
                Letter.States.PUBLISHED,
            ]:
                assign_perm("can_view_letter", request.user, letter_instance)
                assign_perm("can_reject_letter", request.user, letter_instance)
                assign_perm("can_publish_letter", request.user, letter_instance)

        try:
            self.check_object_permissions(request, letter_instance)

            output_serializer = self.OutputSerializer(letter_instance, many=False)
            permissions = self.get_object_permissions_details(letter_instance, current_user)

            response_data = {
                "letter": output_serializer.data,
                "permissions": permissions,
            }

            # channel_layer = get_channel_layer()
            # async_to_sync(channel_layer.group_send)(
            #     f"letter_{letter_instance.reference_number}",
            #     {
            #         "type": "letter_update",
            #         "message": response_data,
            #     },
            # )

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterCreateApi(ApiAuthMixin, ApiPermMixin, APIView):
    serializer_class = LetterCreateSerializer

    def post(self, request) -> Response:
        input_serializer = LetterCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_instance = letter_create(current_user=request.user, **input_serializer.validated_data)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)

            response_data = {
                "letter": output_serializer.data,
                "permissions": permissions,
            }

            return Response(data=response_data, status=http_status.HTTP_201_CREATED)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterCreateAndSubmitApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_submit_letter"]

    class InputSerializer(serializers.Serializer):
        letter = LetterCreateSerializer()
        otp = serializers.IntegerField()

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

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
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
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    class InputSerializer(serializers.Serializer):
        letter = LetterCreateSerializer()
        otp = serializers.IntegerField()

    serializer_class = InputSerializer

    def post(self, request) -> Response:
        request_data = process_request_data(request)

        input_serializer = self.InputSerializer(data=request_data)
        input_serializer.is_valid(raise_exception=True)

        try:
            otp = input_serializer.validated_data.pop("otp")
            verify_otp(current_user=request.user, otp=otp)

            letter_data = input_serializer.validated_data.pop("letter")
            letter_instance = letter_create_and_publish(
                current_user=request.user,
                **letter_data,
            )
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)

            response_data = {
                "message": "The letter has been successfully created and distributed to all recipients.",
                "data": output_serializer.data,
                "permissions": permissions,
            }

            return Response(data=response_data, status=http_status.HTTP_201_CREATED)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterUpdateApi(ApiAuthMixin, ApiPermMixin, APIView):
    serializer_class = LetterCreateSerializer

    def put(self, request, reference_number) -> Response:
        letter_instance = get_object(Letter, reference_number=reference_number)
        self.check_object_permissions(request, letter_instance)

        input_serializer = LetterCreateSerializer(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_instance = letter_update(
                current_user=request.user,
                letter_instance=letter_instance,
                **input_serializer.validated_data,
            )
            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {
                "data": output_serializer.data,
                "permissions": permissions,
            }

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"letter_{reference_number}",
                {
                    "type": "letter_update",
                    "message": response_data,
                },
            )

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterTrashApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_trash_letter"]

    def put(self, request, reference_number) -> Response:
        try:
            letter_instance = get_object(Letter, reference_number=reference_number)
            self.check_object_permissions(request, letter_instance)

            letter_instance = letter_move_to_trash(letter_instance=letter_instance)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {
                "message": "The Letter has been moved to the trash.",
            }

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


class LetterBatchTrashApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_trash_letter"]

    class InputSerializer(serializers.Serializer):
        reference_numbers = serializers.ListSerializer(child=serializers.CharField())

    def put(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        reference_numbers = input_serializer.validated_data.get("reference_numbers")

        response_data = {"message": "The letters have been moved to the trash."}
        updated_letters = []
        failed_references = []

        for ref_number in reference_numbers:
            try:
                letter_instance = get_object(Letter, reference_number=ref_number)
                self.check_object_permissions(request, letter_instance)

                letter_instance = letter_move_to_trash(letter_instance=letter_instance)
                updated_letters.append(letter_instance)

                output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
                permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"letter_{ref_number}",
                    {
                        "type": "letter_update",
                        "message": {
                            "data": output_serializer.data,
                            "permissions": permissions,
                        },
                    },
                )

            except ValueError:
                failed_references.append(ref_number)

            except Exception:
                failed_references.append(ref_number)

        response_data = {
            "message": "The Letter has been moved to the trash.",
        }

        if failed_references:
            response_data["errors"] = {
                "failed_references": failed_references,
                "message": "Some letters could not be moved to the trash.",
            }

        return Response(data=response_data, status=http_status.HTTP_200_OK)


class LetterRestoreApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_restore_letter"]

    def put(self, request, reference_number) -> Response:
        try:
            letter_instance = get_object(Letter, reference_number=reference_number)
            self.check_object_permissions(request, letter_instance)

            letter_instance = letter_restore_from_trash(letter_instance=letter_instance)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {
                "message": "The Letter has been restored from the trash.",
            }

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


class LetterBatchRestoreApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_restore_letter"]

    class InputSerializer(serializers.Serializer):
        reference_numbers = serializers.ListField(child=serializers.CharField())

    def put(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        reference_numbers = input_serializer.validated_data.get("reference_numbers")

        updated_letters = []
        failed_references = []

        for ref_number in reference_numbers:
            try:
                letter_instance = get_object(Letter, reference_number=ref_number)
                self.check_object_permissions(request, letter_instance)

                letter_instance = letter_restore_from_trash(letter_instance=letter_instance)
                updated_letters.append(letter_instance)

                output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
                permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"letter_{ref_number}",
                    {
                        "type": "letter_update",
                        "message": {
                            "data": output_serializer.data,
                            "permissions": permissions,
                        },
                    },
                )

            except ValueError as e:
                failed_references.append({"reference_number": ref_number, "error": str(e)})

            except Exception as e:
                failed_references.append({"reference_number": ref_number, "error": str(e)})

        response_data = {"message": "The letters have been restored from the trash."}

        if failed_references:
            response_data["errors"] = {
                "failed_references": failed_references,
                "message": "Some letters could not be restored from the trash.",
            }

        return Response(data=response_data, status=http_status.HTTP_200_OK)


class LetterPermanentlyDeleteApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_permanently_delete_letter"]

    class InputSerializer(serializers.Serializer):
        otp = serializers.IntegerField()

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

            response_data = {
                "message": "The Letter has been deleted successfully.",
            }

            return Response(data=response_data, status=http_status.HTTP_204_NO_CONTENT)

        except APIError as e:
            raise APIError(e.error_code, e.status_code, e.message, e.extra)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterBatchPermanentlyDeleteApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_permanently_delete_letter"]

    class InputSerializer(serializers.Serializer):
        reference_numbers = serializers.ListField(child=serializers.CharField())
        otp = serializers.IntegerField()

    def put(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        reference_numbers = input_serializer.validated_data.get("reference_numbers")
        otp = input_serializer.validated_data.get("otp")

        verify_otp(current_user=request.user, otp=otp)

        failed_references = []

        for ref_number in reference_numbers:
            try:
                letter_instance = get_object(Letter, reference_number=ref_number)
                self.check_object_permissions(request, letter_instance)

                letter_hide(letter_instance=letter_instance)

            except APIError as e:
                raise APIError(e.error_code, e.status_code, e.message, e.extra)

            except ValueError as e:
                failed_references.append({"reference_number": ref_number, "error": str(e)})

            except Exception as e:
                failed_references.append({"reference_number": ref_number, "error": str(e)})

        response_data = {"message": "The letters have been deleted successfully."}

        if failed_references:
            response_data["errors"] = {
                "failed_references": failed_references,
                "message": "Some letters could not be permanently deleted.",
            }

        return Response(data=response_data, status=http_status.HTTP_204_NO_CONTENT)
