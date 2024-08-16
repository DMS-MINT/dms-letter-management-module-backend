# from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

# from core.users.serializers import UserCreateSerializer
from .models import BaseParticipant
from .serializers import ParticipantOutputSerializer

# from .services import initialize_participants


class ParticipantListApi(APIView):
    def get(self, request):
        try:
            participants = BaseParticipant.objects.all()
            output_serializer = ParticipantOutputSerializer(participants, many=True)

            response_data = {"participants": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


# class ParticipantCreateApi(APIView):
#     class InputSerializer(serializers.Serializer):
#         user = UserCreateSerializer()
#         role = serializers.ChoiceField(choices=BaseParticipant.Roles.choices)
#         message = serializers.CharField(required=False, allow_null=True)

#     serializer_class = InputSerializer

#     def post(self, request):
#         input_serializer = self.InputSerializer(data=request.data, many=True)

#         if input_serializer.is_valid():
#             try:
#                 participant_instance = initialize_participants(
#                     validated_data=input_serializer.validated_data,
#                     letter_id=input_serializer.validated_data,
#                 )

#                 output_serializer = ParticipantListApi.OutputSerializer(data=participant_instance, many=True)

#                 output_serializer.is_valid()

#                 return Response(data=output_serializer.data)
#             except ValueError as e:
#                 return Response({"detail": str(e)}, status=http_status.HTTP_400_BAD_REQUEST)

#         else:
#             return Response(input_serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
