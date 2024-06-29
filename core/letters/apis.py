from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from guardian.shortcuts import assign_perm
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_polymorphic.serializers import PolymorphicSerializer

from core.api.mixins import ApiAuthMixin
from core.common.utils import get_object, inline_serializer
from core.permissions.mixins import ApiPermMixin
from core.users.serializers import UserCreateSerializer
from core.workflows.services import letter_submit

from .models import Incoming, Internal, Letter, Outgoing
from .selectors import letter_list
from .serializers import (
    LetterDetailSerializer,
    LetterListSerializer,
    OutgoingLetterDetailSerializer,
)
from .services import letter_create, letter_update
from .utils import process_request_data


class LetterListApi(ApiAuthMixin, APIView):
    class FilterSerializer(serializers.Serializer):
        category = serializers.ChoiceField(
            choices=["inbox", "outbox", "draft", "pending", "published"],
            required=True,
        )

    class OutputSerializer(PolymorphicSerializer):
        resource_type_field_name = "letter_type"
        model_serializer_mapping = {
            Internal: LetterListSerializer,
            Incoming: LetterListSerializer,
            Outgoing: LetterListSerializer,
        }

        def to_resource_type(self, model_or_instance):
            return model_or_instance._meta.object_name.lower()

    def get(self, request) -> Response:
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        letter_instances = letter_list(current_user=request.user, filters=filter_serializer.validated_data)

        serializer = self.OutputSerializer(letter_instances, many=True)

        response_data = {"data": serializer.data}

        return Response(data=response_data, status=http_status.HTTP_200_OK)


class LetterDetailApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter"]

    class OutputSerializer(PolymorphicSerializer):
        resource_type_field_name = "letter_type"
        model_serializer_mapping = {
            Internal: LetterDetailSerializer,
            Incoming: LetterDetailSerializer,
            Outgoing: OutgoingLetterDetailSerializer,
        }

        def to_resource_type(self, instance):
            return instance._meta.object_name.lower()

    def get(self, request, reference_number) -> Response:
        letter_instance = get_object(Letter, reference_number=reference_number)

        if request.user.is_staff and letter_instance.current_state in [
            Letter.States.SUBMITTED,
            Letter.States.PUBLISHED,
        ]:
            assign_perm("can_view_letter", request.user, letter_instance)
            assign_perm("can_publish_letter", request.user, letter_instance)

        self.check_object_permissions(request, letter_instance)

        output_serializer = self.OutputSerializer(letter_instance, many=False)
        permissions = self.get_object_permissions_details(letter_instance)

        response_data = {
            "data": output_serializer.data,
            "permissions": permissions,
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"letter_{letter_instance.reference_number}",
            {
                "type": "letter_update",
                "message": response_data,
            },
        )

        return Response(data=response_data, status=http_status.HTTP_200_OK)


class LetterCreateApi(ApiAuthMixin, ApiPermMixin, APIView):
    parser_classes = [MultiPartParser, FormParser]

    class InputSerializer(serializers.Serializer):
        subject = serializers.CharField(required=False, allow_blank=True)
        content = serializers.CharField(required=False, allow_blank=True)
        letter_type = serializers.ChoiceField(choices=["internal", "incoming", "outgoing"])
        signature = serializers.ImageField(required=False, allow_null=True)
        participants = inline_serializer(
            many=True,
            fields={
                "id": serializers.UUIDField(),
                "user": UserCreateSerializer(),
                "role": serializers.CharField(),
            },
        )
        attachments = serializers.ListField(
            required=False,
            child=serializers.FileField(
                allow_empty_file=True,
            ),
        )

    def post(self, request) -> Response:
        request_data = process_request_data(request)

        input_serializer = self.InputSerializer(data=request_data)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_instance = letter_create(current_user=request.user, **input_serializer.validated_data)
            permissions = self.get_object_permissions_details(letter_instance)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)

            response_data = {
                "data": output_serializer.data,
                "permissions": permissions,
            }

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"letter_{letter_instance.reference_number}",
                {
                    "type": "letter_update",
                    "message": response_data,
                },
            )

            return Response(data=response_data, status=http_status.HTTP_201_CREATED)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterCreateAndSubmitApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_submit_letter"]

    class InputSerializer(serializers.Serializer):
        subject = serializers.CharField(required=False, allow_blank=True)
        content = serializers.CharField(required=False, allow_blank=True)
        letter_type = serializers.ChoiceField(choices=["internal", "incoming", "outgoing"])
        signature = serializers.ImageField(required=False, allow_null=True)
        participants = inline_serializer(
            many=True,
            fields={
                "id": serializers.UUIDField(),
                "user": UserCreateSerializer(),
                "role": serializers.CharField(),
            },
        )
        attachments = serializers.ListField(
            required=False,
            child=serializers.FileField(
                allow_empty_file=True,
            ),
        )

    def post(self, request) -> Response:
        request_data = process_request_data(request)

        input_serializer = self.InputSerializer(data=request_data)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_instance = letter_create(current_user=request.user, **input_serializer.validated_data)
            response_message = "Letter created successfully. The letter has not been submitted."
            status_code = http_status.HTTP_201_CREATED

            try:
                self.check_object_permissions(request, letter_instance)
                letter_instance = letter_submit(current_user=request.user, letter_instance=letter_instance)
                response_message = "Letter created and submitted successfully."
                status_code = http_status.HTTP_200_OK
            except:
                pass

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions(request, letter_instance)

            response_data = {
                "message": response_message,
                "data": output_serializer.data,
                "permissions": permissions,
            }

            return Response(data=response_data, status=status_code)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterUpdateApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_update_letter"]

    class InputSerializer(serializers.Serializer):
        subject = serializers.CharField(required=False, allow_blank=True)
        content = serializers.CharField(required=False, allow_blank=True)
        letter_type = serializers.ChoiceField(choices=["internal", "incoming", "outgoing"])
        signature = serializers.ImageField(required=False, allow_null=True)
        participants = inline_serializer(
            many=True,
            required=False,
            fields={
                "id": serializers.UUIDField(),
                "user": UserCreateSerializer(),
                "role": serializers.CharField(),
            },
        )
        attachments = serializers.ListField(
            required=False,
            child=serializers.FileField(
                allow_empty_file=True,
            ),
        )

    def put(self, request, reference_number) -> Response:
        letter_instance = get_object_or_404(Letter, reference_number=reference_number)
        self.check_object_permissions(request, letter_instance)

        request_data = process_request_data(request)

        input_serializer = self.InputSerializer(data=request_data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_instance = letter_update(
                current_user=request.user,
                letter_instance=letter_instance,
                **input_serializer.validated_data,
            )
            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance)

            response_data = {
                "data": output_serializer.data,
                "permissions": permissions,
            }

            # Notify WebSocket consumers about the update
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


class LetterDeleteApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_delete_letter"]

    def delete(self, request, reference_number) -> Response:
        letter_instance = get_object_or_404(Letter, reference_number=reference_number)
        self.check_object_permissions(request, letter_instance)

        letter_instance.delete()
        return Response(status=http_status.HTTP_204_NO_CONTENT)
