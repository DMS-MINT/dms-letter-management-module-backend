from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.exceptions import APIError
from core.api.mixins import ApiAuthMixin
from core.authentication.services import verify_otp
from core.comments.services import comment_create
from core.common.utils import get_object
from core.letters.models import Letter
from core.letters.serializers import LetterDetailPolymorphicSerializer
from core.letters.tasks import generate_pdf_task
from core.participants.serializers import ParticipantInputSerializer
from core.participants.services import participants_create
from core.permissions.mixins import ApiPermMixin

from .notification_handler import handle_publish_letter_notification, handle_reject_letter_notification
from .services import letter_close, letter_publish, letter_reject, letter_reopen, letter_retract, letter_submit


class LetterShareApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_share_letter"]

    class InputSerializer(serializers.Serializer):
        participants = serializers.ListSerializer(child=ParticipantInputSerializer())
        message = serializers.CharField()
        permissions = serializers.ListField(
            child=serializers.ChoiceField(
                choices=[
                    "can_view_letter",
                    "can_update_letter",
                    "can_comment_letter",
                    "can_share_letter",
                ],
            ),
        )

    serializer_class = InputSerializer

    def post(self, request, reference_number) -> Response:
        letter_instance = get_object(Letter, reference_number=reference_number)

        self.check_object_permissions(request, letter_instance)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            message = input_serializer.validated_data.pop("message")

            participants_create(
                current_user=request.user,
                letter_instance=letter_instance,
                **input_serializer.validated_data,
            )

            comment_create(current_user=request.user, letter_instance=letter_instance, message=message)

            output_serializer = LetterDetailPolymorphicSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {"message": "Letter has been shared with the specified collaborators."}

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

        except APIError as e:
            raise APIError(e.error_code, e.status_code, e.message, e.extra)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterSubmitApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_submit_letter"]

    class InputSerializer(serializers.Serializer):
        signature_method = serializers.ChoiceField(required=False, choices=["Default", "Canvas"])
        otp = serializers.CharField()

    def put(self, request, reference_number) -> Response:
        letter_instance = get_object(Letter, reference_number=reference_number)
        self.check_object_permissions(request, letter_instance)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        _signature_method = input_serializer.validated_data.get("signature_method")
        otp = input_serializer.validated_data.get("otp")

        try:
            verify_otp(current_user=request.user, otp=otp)
            letter_instance = letter_submit(
                current_user=request.user,
                letter_instance=letter_instance,
                signature_method="Default",
            )

            output_serializer = LetterDetailPolymorphicSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {"message": "Letter has been submitted to the record office."}

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

            generate_pdf_task.delay_on_commit(letter_id=letter_instance.id)

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except APIError as e:
            raise APIError(e.error_code, e.status_code, e.message, e.extra)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterRetractApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_retract_letter"]

    class InputSerializer(serializers.Serializer):
        otp = serializers.CharField()

    def put(self, request, reference_number) -> Response:
        letter_instance = get_object(Letter, reference_number=reference_number)

        self.check_object_permissions(request, letter_instance)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            verify_otp(current_user=request.user, **input_serializer.validated_data)
            letter_instance = letter_retract(current_user=request.user, letter_instance=letter_instance)

            output_serializer = LetterDetailPolymorphicSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {
                "message": "Letter has been retracted.",
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

            generate_pdf_task.delay_on_commit(letter_id=letter_instance.id)

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except APIError as e:
            raise APIError(e.error_code, e.status_code, e.message, e.extra)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterPublishApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_publish_letter"]
    permission_classes = [IsAdminUser]

    class InputSerializer(serializers.Serializer):
        otp = serializers.CharField()

    def put(self, request, reference_number) -> Response:
        letter_instance = get_object(Letter, reference_number=reference_number)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        otp = input_serializer.validated_data.get("otp")

        try:
            verify_otp(current_user=request.user, otp=otp)
            letter_publish(current_user=request.user, letter_instance=letter_instance)

            output_serializer = LetterDetailPolymorphicSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            handle_publish_letter_notification(current_user=request.user, letter_instance=letter_instance)

            response_data = {"message": "Letter has been published."}

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

        except APIError as e:
            raise APIError(e.error_code, e.status_code, e.message, e.extra)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterRejectApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_reject_letter"]
    permission_classes = [IsAdminUser]

    class InputSerializer(serializers.Serializer):
        message = serializers.CharField()
        otp = serializers.CharField()

    def put(self, request, reference_number) -> Response:
        letter_instance = get_object(Letter, reference_number=reference_number)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        message = input_serializer.validated_data.get("message")
        otp = input_serializer.validated_data.get("otp")

        try:
            verify_otp(current_user=request.user, otp=otp)

            letter_reject(current_user=request.user, letter_instance=letter_instance)

            handle_reject_letter_notification(
                current_user=request.user,
                letter_instance=letter_instance,
                message=message,
            )

            output_serializer = LetterDetailPolymorphicSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {"message": "Letter has been rejected and sent back to the sender."}

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

        except APIError as e:
            raise APIError(e.error_code, e.status_code, e.message, e.extra)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterCloseApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_close_letter"]

    def put(self, request, reference_number) -> Response:
        letter_instance = get_object(Letter, reference_number=reference_number)

        self.check_object_permissions(request, letter_instance)

        try:
            letter_instance = letter_close(current_user=request.user, letter_instance=letter_instance)

            output_serializer = LetterDetailPolymorphicSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {
                "message": "The letter has been officially closed.",
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

        except APIError as e:
            raise APIError(e.error_code, e.status_code, e.message, e.extra)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterReopenApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_reopen_letter"]

    def put(self, request, reference_number) -> Response:
        letter_instance = get_object(Letter, reference_number=reference_number)

        self.check_object_permissions(request, letter_instance)

        try:
            letter_instance = letter_reopen(current_user=request.user, letter_instance=letter_instance)

            output_serializer = LetterDetailPolymorphicSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {
                "message": "The letter has been reopened.",
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

        except APIError as e:
            raise APIError(e.error_code, e.status_code, e.message, e.extra)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
