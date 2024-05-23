from pkg_resources import require
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.users.apis import UserListApi
from core.users.serializers import UserCreateSerializer

from .models import Participant
from .services import participant_create


class ParticipantListApi(APIView):
    class OutputSerializer(serializers.HyperlinkedModelSerializer):
        role = serializers.ChoiceField(choices=Participant.Roles.choices, source="get_role_display")
        user = UserListApi.OutputSerializer()

        class Meta:
            model = Participant
            fields: list[str] = [
                "id",
                "role",
                "user",
                "message",
                "created",
                "modified",
            ]


class ParticipantCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        user = UserCreateSerializer()
        role = serializers.ChoiceField(choices=Participant.Roles.choices)
        message = serializers.CharField(required=False, allow_null=True)

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data, many=True)

        if input_serializer.is_valid():
            try:
                participant_instance = participant_create(
                    validated_data=input_serializer.validated_data, letter_id=input_serializer.validated_data
                )

                output_serializer = ParticipantListApi.OutputSerializer(data=participant_instance, many=True)

                output_serializer.is_valid()

                return Response(data=output_serializer.data)
            except ValueError as e:
                return Response({"detail": str(e)}, status=http_status.HTTP_400_BAD_REQUEST)

        else:
            return Response(input_serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
