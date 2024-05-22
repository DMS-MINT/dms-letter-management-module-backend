from rest_framework import serializers
from rest_framework.views import APIView

from core.users.apis import UserListApi

from .models import Participant


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
