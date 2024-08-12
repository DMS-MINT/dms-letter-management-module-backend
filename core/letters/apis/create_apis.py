from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse
from guardian.shortcuts import assign_perm
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.exceptions import APIError
from core.api.mixins import ApiAuthMixin
from core.authentication.services import verify_otp
from core.common.utils import get_object
from core.letters.serializers import LetterCreateSerializer, LetterDetailSerializer
from core.letters.services.create_services import letter_create
from core.permissions.mixins import ApiPermMixin
from core.workflows.services import letter_submit


class LetterCreateApi(ApiAuthMixin, ApiPermMixin, APIView):
    serializer_class = LetterCreateSerializer

    def post(self, request) -> Response:
        input_serializer = LetterCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            letter_instance = letter_create(current_user=request.user, **input_serializer.validated_data)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            output_serializer = LetterDetailSerializer(letter_instance)
            response_data = {"letter": output_serializer.data, "permissions": permissions}

            return Response(data=response_data, status=http_status.HTTP_201_CREATED)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
