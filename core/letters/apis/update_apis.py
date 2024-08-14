from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.common.utils import get_object
from core.letters.models import Letter
from core.letters.serializers import LetterCreateSerializer, LetterDetailSerializer
from core.letters.services.update_services import letter_update
from core.participants.serializers import ParticipantInputSerializer
from core.permissions.mixins import ApiPermMixin


class LetterUpdateApi(ApiAuthMixin, ApiPermMixin, APIView):
    class InputSerializer(serializers.Serializer):
        subject = serializers.CharField(required=False, allow_blank=True)
        body = serializers.CharField(required=False, allow_blank=True)
        participants = ParticipantInputSerializer(many=True)

    serializer_class = InputSerializer

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
            output_serializer = LetterDetailSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {"data": output_serializer.data, "permissions": permissions}

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
