from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.letters.models import Letter

from .services import letter_publish, letter_retract, letter_share, letter_submit

SHARE_LETTER_HRF = "api/workflow/<uuid:letter_id>/share/"
SUBMIT_LETTER_HRF = "api/workflow/<uuid:letter_id>/submit/"
PUBLISH_LETTER_HRF = "api/workflow/<uuid:letter_id>/publish/"
RETRACT_LETTER_HRF = "api/workflow/<uuid:letter_id>/retract/"
CLOSE_LETTER_HRF = "api/workflow/<uuid:letter_id>/close/"
ARCHIVE_LETTER_HRF = "api/workflow/<uuid:letter_id>/archive/"
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


class LetterShareApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        to = serializers.CharField()
        message = serializers.CharField()
        permissions = serializers.ListField(child=serializers.CharField(), required=False)

    def post(self, request, letter_id) -> Response:
        letter_instance = get_object_or_404(Letter, pk=letter_id)
        input_serializer = self.InputSerializer(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_share(user=request.user, letter_instance=letter_instance, **input_serializer.validated_data)

            response_data = {"action": ACTIONS, "message": "Letter has been shared with the specified collaborator."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterSubmitApi(ApiAuthMixin, APIView):
    def post(self, request, letter_id) -> Response:
        letter_instance = get_object_or_404(Letter, pk=letter_id)

        try:
            letter_submit(user=request.user, letter_instance=letter_instance)

            response_data = {"action": ACTIONS, "message": "Letter has been submitted to the record office."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterRetractApi(ApiAuthMixin, APIView):
    def post(self, request, letter_id) -> Response:
        letter_instance = get_object_or_404(Letter, pk=letter_id)

        try:
            letter_retract(user=request.user, letter_instance=letter_instance)

            response_data = {"action": ACTIONS, "message": "Letter has been retracted from the record office."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterPublishApi(ApiAuthMixin, APIView):
    def post(self, request, letter_id) -> Response:
        letter_instance = get_object_or_404(Letter, pk=letter_id)

        try:
            letter_publish(user=request.user, letter_instance=letter_instance)

            response_data = {"action": ACTIONS, "message": "Letter has been published."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
