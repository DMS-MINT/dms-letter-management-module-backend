from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.exceptions import APIError
from core.api.mixins import ApiAuthMixin
from core.authentication.services import verify_otp
from core.common.utils import get_object
from core.letters.models import Letter
from core.letters.serializers import LetterDetailSerializer
from core.letters.services.delete_services import letter_hide, letter_move_to_trash, letter_restore_from_trash
from core.permissions.mixins import ApiPermMixin


class LetterBulkTrashApi(ApiAuthMixin, ApiPermMixin, APIView):
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
        permission_errors = []

        for ref_number in reference_numbers:
            try:
                letter_instance = get_object(Letter, reference_number=ref_number)
                self.check_object_permissions(request, letter_instance)

                letter_instance = letter_move_to_trash(letter_instance=letter_instance)
                updated_letters.append(letter_instance)

                output_serializer = LetterDetailSerializer(letter_instance)
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

            except PermissionDenied:
                failed_references.append(ref_number)

            except ValueError:
                failed_references.append(ref_number)

            except Exception:
                failed_references.append(ref_number)

        succeeded_references = [
            ref for ref in reference_numbers if ref not in failed_references and ref not in permission_errors
        ]

        if permission_errors or failed_references:
            error_message = (
                f"Operation summary:\n"
                f"Successfully moved to trash: {", ".join(succeeded_references)}.\n"
                f"Permission denied for: {", ".join(permission_errors)}.\n"
                f"Failed to move to trash due to errors: {", ".join(failed_references)}."
            )

            raise APIError(
                error_code="BATCH_OPERATION_FAILED",
                status_code=http_status.HTTP_400_BAD_REQUEST,
                message="Validation error",
                extra={
                    "succeeded_references": succeeded_references,
                    "permission_errors": permission_errors,
                    "failed_references": failed_references,
                    "message": error_message,
                },
            )

        response_data = {"message": "The letters have been moved to the trash."}
        return Response(data=response_data, status=http_status.HTTP_200_OK)


class LetterBulkRestoreApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_restore_letter"]

    class InputSerializer(serializers.Serializer):
        reference_numbers = serializers.ListField(child=serializers.CharField())

    def put(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        reference_numbers = input_serializer.validated_data.get("reference_numbers")

        updated_letters = []
        failed_references = []
        permission_errors = []

        for ref_number in reference_numbers:
            try:
                letter_instance = get_object(Letter, reference_number=ref_number)
                self.check_object_permissions(request, letter_instance)

                letter_instance = letter_restore_from_trash(letter_instance=letter_instance)
                updated_letters.append(letter_instance)

                output_serializer = LetterDetailSerializer(letter_instance)
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
            except PermissionDenied:
                failed_references.append(ref_number)

            except ValueError as e:
                failed_references.append({"reference_number": ref_number, "error": str(e)})

            except Exception as e:
                failed_references.append({"reference_number": ref_number, "error": str(e)})

        succeeded_references = [
            ref for ref in reference_numbers if ref not in failed_references and ref not in permission_errors
        ]

        if permission_errors or failed_references:
            error_message = (
                f"Operation summary:\n"
                f"Successfully moved to trash: {", ".join(succeeded_references)}.\n"
                f"Permission denied for: {", ".join(permission_errors)}.\n"
                f"Failed to move to trash due to errors: {", ".join(failed_references)}."
            )

            raise APIError(
                error_code="BATCH_OPERATION_FAILED",
                status_code=http_status.HTTP_400_BAD_REQUEST,
                message="Validation error",
                extra={
                    "succeeded_references": succeeded_references,
                    "permission_errors": permission_errors,
                    "failed_references": failed_references,
                    "message": error_message,
                },
            )

        response_data = {"message": "The letters have been moved to the trash."}
        return Response(data=response_data, status=http_status.HTTP_200_OK)


class LetterBulkDeleteApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_permanently_delete_letter"]

    class InputSerializer(serializers.Serializer):
        reference_numbers = serializers.ListField(child=serializers.CharField())
        otp = serializers.CharField()

    def put(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        reference_numbers = input_serializer.validated_data.get("reference_numbers")
        otp = input_serializer.validated_data.get("otp")

        verify_otp(current_user=request.user, otp=otp)

        failed_references = []
        permission_errors = []

        for ref_number in reference_numbers:
            try:
                letter_instance = get_object(Letter, reference_number=ref_number)
                self.check_object_permissions(request, letter_instance)

                letter_hide(letter_instance=letter_instance)

            except APIError as e:
                raise APIError(e.error_code, e.status_code, e.message, e.extra)

            except PermissionDenied:
                failed_references.append(ref_number)

            except ValueError as e:
                failed_references.append({"reference_number": ref_number, "error": str(e)})

            except Exception as e:
                failed_references.append({"reference_number": ref_number, "error": str(e)})

        succeeded_references = [
            ref for ref in reference_numbers if ref not in failed_references and ref not in permission_errors
        ]

        if permission_errors or failed_references:
            error_message = (
                f"Operation summary:\n"
                f"Successfully moved to trash: {", ".join(succeeded_references)}.\n"
                f"Permission denied for: {", ".join(permission_errors)}.\n"
                f"Failed to move to trash due to errors: {", ".join(failed_references)}."
            )

            raise APIError(
                error_code="BATCH_OPERATION_FAILED",
                status_code=http_status.HTTP_400_BAD_REQUEST,
                message="Validation error",
                extra={
                    "succeeded_references": succeeded_references,
                    "permission_errors": permission_errors,
                    "failed_references": failed_references,
                    "message": error_message,
                },
            )

        response_data = {"message": "The letters have been moved to the trash."}
        return Response(data=response_data, status=http_status.HTTP_200_OK)
