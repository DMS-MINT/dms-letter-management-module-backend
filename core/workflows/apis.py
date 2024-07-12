from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.letters.apis import LetterDetailApi
from core.letters.models import Letter
from core.participants.services import add_participants
from core.permissions.mixins import ApiPermMixin

from .services import letter_close, letter_publish, letter_reject, letter_reopen, letter_retract, letter_submit


class LetterShareApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_share_letter"]

    class InputSerializer(serializers.Serializer):
        to = serializers.ListField(child=serializers.CharField())
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
        letter_instance = get_object_or_404(Letter, reference_number=reference_number)
        self.check_object_permissions(request, letter_instance)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            add_participants(
                current_user=request.user,
                letter_instance=letter_instance,
                participants=input_serializer.validated_data,
            )

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance)

            response_data = {
                "message": "Letter has been shared with the specified collaborators.",
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


class LetterSubmitApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_submit_letter"]

    def post(self, request, reference_number) -> Response:
        letter_instance = get_object_or_404(Letter, reference_number=reference_number)
        self.check_object_permissions(request, letter_instance)

        try:
            letter_instance = letter_submit(current_user=request.user, letter_instance=letter_instance)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance)

            response_data = {
                "message": "Letter has been submitted to the record office.",
                "permissions": permissions,
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


class LetterRetractApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_retract_letter"]

    def post(self, request, reference_number) -> Response:
        letter_instance = get_object_or_404(Letter, reference_number=reference_number)
        self.check_object_permissions(request, letter_instance)

        try:
            letter_instance = letter_retract(current_user=request.user, letter_instance=letter_instance)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance)

            response_data = {
                "message": "Letter has been retracted.",
                "permissions": permissions,
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


class LetterPublishApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_publish_letter"]
    permission_classes = [IsAdminUser]

    def post(self, request, reference_number) -> Response:
        letter_instance = get_object_or_404(Letter, reference_number=reference_number)

        try:
            letter_publish(current_user=request.user, letter_instance=letter_instance)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance)

            response_data = {
                "message": "Letter has been published.",
                "permissions": permissions,
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


class LetterRejectApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_reject_letter"]
    permission_classes = [IsAdminUser]

    def post(self, request, reference_number) -> Response:
        letter_instance = get_object_or_404(Letter, reference_number=reference_number)

        try:
            letter_reject(current_user=request.user, letter_instance=letter_instance)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance)

            response_data = {
                "message": "Letter has been rejected and sent back to the sender.",
                "permissions": permissions,
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


class LetterCloseApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_close_letter"]

    def post(self, request, reference_number) -> Response:
        letter_instance = get_object_or_404(Letter, reference_number=reference_number)
        self.check_object_permissions(request, letter_instance)

        try:
            letter_instance = letter_close(current_user=request.user, letter_instance=letter_instance)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance)

            response_data = {
                "message": "The letter has been officially closed.",
                "permissions": permissions,
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


class LetterReopenApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_reopen_letter"]

    def post(self, request, reference_number) -> Response:
        letter_instance = get_object_or_404(Letter, reference_number=reference_number)
        self.check_object_permissions(request, letter_instance)

        try:
            letter_instance = letter_reopen(current_user=request.user, letter_instance=letter_instance)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance)

            response_data = {
                "message": "The letter has been reopened.",
                "permissions": permissions,
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
