from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from core.common.utils import inline_serializer
from core.contacts.models import Contact
from core.enterprises.models import Enterprise
from core.participants.models import BaseParticipant
from core.users.models import User
from core.users.serializers import UserListSerializer

from .models import EnterpriseParticipant, ExternalUserParticipant, InternalUserParticipant


class AddressSerializer(serializers.Serializer):
    city_en = serializers.CharField(max_length=100)
    city_am = serializers.CharField(max_length=100)


class BaseParticipantInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    role = serializers.CharField()

    def to_internal_value(self, data):
        role = data.pop("role")
        role = self.get_role_from_string(role)
        data["role"] = role
        return super().to_internal_value(data)

    def get_role_from_string(self, role: str):
        role_map = {choice[1]: choice[0] for choice in BaseParticipant.Roles.choices}
        return role_map.get(role, None)


class InternalParticipantInputSerializer(BaseParticipantInputSerializer):
    user_id = serializers.UUIDField()


class EnterpriseParticipantInputSerializer(BaseParticipantInputSerializer):
    enterprise_id = serializers.UUIDField()


class ExternalParticipantInputSerializer(BaseParticipantInputSerializer):
    contact = inline_serializer(
        fields={
            "full_name_en": serializers.CharField(max_length=500),
            "full_name_am": serializers.CharField(max_length=500),
            "email": serializers.EmailField(allow_blank=True, required=False),
            "phone_number": serializers.CharField(max_length=20, allow_blank=True, required=False),
            "address": AddressSerializer(),
        },
    )


class ParticipantInputSerializer(PolymorphicSerializer):
    resource_type_field_name = "participant_type"
    model_serializer_mapping = {
        User: InternalParticipantInputSerializer,
        Enterprise: EnterpriseParticipantInputSerializer,
        Contact: ExternalParticipantInputSerializer,
    }

    def to_resource_type(self, model_or_instance):
        return model_or_instance._meta.object_name.lower()


class BaseParticipantOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    role = serializers.ChoiceField(choices=BaseParticipant.Roles.choices, source="get_role_display")


class InternalParticipantOutputSerializer(BaseParticipantOutputSerializer):
    user = UserListSerializer()


class EnterpriseParticipantOutputSerializer(BaseParticipantOutputSerializer):
    enterprise = inline_serializer(
        fields={
            "id": serializers.UUIDField(),
            "name_en": serializers.CharField(),
            "name_am": serializers.CharField(),
            "email": serializers.EmailField(),
            "phone_number": serializers.IntegerField(),
            "address": serializers.CharField(),
            "postal_code": serializers.IntegerField(),
            "logo": serializers.ImageField(),
        },
    )


class ExternalParticipantOutputSerializer(BaseParticipantOutputSerializer):
    contact = inline_serializer(
        fields={
            "id": serializers.UUIDField(),
            "full_name_en": serializers.CharField(max_length=500),
            "full_name_am": serializers.CharField(max_length=500),
            "email": serializers.EmailField(allow_blank=True, required=False),
            "phone_number": serializers.CharField(max_length=20, allow_blank=True, required=False),
            "address": AddressSerializer(),
        },
    )


class ParticipantOutputSerializer(PolymorphicSerializer):
    resource_type_field_name = "participant_type"
    model_serializer_mapping = {
        InternalUserParticipant: InternalParticipantOutputSerializer,
        EnterpriseParticipant: EnterpriseParticipantOutputSerializer,
        ExternalUserParticipant: ExternalParticipantOutputSerializer,
    }

    model_to_resource_type = {
        "internaluserparticipant": "user",
        "enterpriseparticipant": "enterprise",
        "externaluserparticipant": "contact",
    }

    def to_resource_type(self, model_or_instance):
        object_name = model_or_instance._meta.object_name.lower()

        if object_name in self.model_to_resource_type:
            return self.model_to_resource_type[object_name]

        raise ValueError("Invalid participant type")
