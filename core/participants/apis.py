from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.common.utils import get_object

from .models import BaseParticipant


class ParticipantRemoveApi(APIView):
    def delete(self, request, participant_id):
        try:
            participant_instance = get_object(BaseParticipant, pk=participant_id)

            participant_instance.delete()

            response_data = {"message": "Participant successfully deleted"}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
