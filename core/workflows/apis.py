from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.letters.models import Letter
from core.participants.services import add_participants
from core.permissions.mixins import ApiPermMixin

from .services import letter_close, letter_publish, letter_reopen, letter_retract, letter_submit

SHARE_LETTER_HRF = "api/letters/<slug:reference_number>/share/"
SUBMIT_LETTER_HRF = "api/letters/<slug:reference_number>/submit/"
PUBLISH_LETTER_HRF = "api/letters/<slug:reference_number>/publish/"
RETRACT_LETTER_HRF = "api/letters/<slug:reference_number>/retract/"
CLOSE_LETTER_HRF = "api/letters/<slug:reference_number>/close/"
REOPEN_LETTER_HRF = "api/letters/<slug:reference_number>/reopen/"
ARCHIVE_LETTER_HRF = "api/letters/<slug:reference_number>/archive/"
ACTIONS = (
    [
        {
            "name": "Share Listing",
            "hrf": SHARE_LETTER_HRF,
            "method": "GET",
        },
        {
            "name": "Submit Details",
            "hrf": SUBMIT_LETTER_HRF,
            "method": "GET",
        },
        {
            "name": "Publish Letter",
            "hrf": PUBLISH_LETTER_HRF,
            "method": "PUT",
        },
        {
            "name": "Retract Letter",
            "hrf": RETRACT_LETTER_HRF,
            "method": "PUT",
        },
        {
            "name": "Close Letter",
            "hrf": CLOSE_LETTER_HRF,
            "method": "DELETE",
        },
        {
            "name": "Archive Letter",
            "hrf": ARCHIVE_LETTER_HRF,
            "method": "DELETE",
        },
    ],
)


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

            response_data = {
                "action": ACTIONS,
                "message": "Letter has been shared with the specified collaborators.",
            }

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
            permissions = self.get_object_permissions(request, letter_instance)

            response_data = {
                "action": ACTIONS,
                "message": "Letter has been submitted to the record office.",
                "permissions": permissions,
            }

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
            permissions = self.get_object_permissions(request, letter_instance)

            response_data = {
                "action": ACTIONS,
                "message": "Letter has been retracted.",
                "permissions": permissions,
            }

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
            permissions = self.get_object_permissions(request, letter_instance)

            response_data = {
                "action": ACTIONS,
                "message": "Letter has been published.",
                "permissions": permissions,
            }

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
            permissions = self.get_object_permissions(request, letter_instance)

            response_data = {
                "action": ACTIONS,
                "message": "The letter has been officially closed.",
                "permissions": permissions,
            }

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
            permissions = self.get_object_permissions(request, letter_instance)

            response_data = {
                "action": ACTIONS,
                "message": "The letter has been reopened.",
                "permissions": permissions,
            }

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
