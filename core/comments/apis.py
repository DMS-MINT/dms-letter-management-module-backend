from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.letters.apis import LetterDetailApi
from core.letters.models import Letter
from core.permissions.mixins import ApiPermMixin

from .models import Comment
from .services import comment_create, comment_update


class CommentCreateApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_comment_letter"]

    class InputSerializer(serializers.Serializer):
        content = serializers.CharField()

    serializer_class = InputSerializer

    def post(self, request, reference_number):
        letter_instance = get_object_or_404(Letter, reference_number=reference_number)
        self.check_object_permissions(request, letter_instance)

        input_instance = self.InputSerializer(data=request.data)
        input_instance.is_valid(raise_exception=True)

        try:
            comment_create(
                current_user=request.user,
                letter_instance=letter_instance,
                **input_instance.validated_data,
            )

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

            response_data = {
                "data": output_serializer.data,
                "permissions": permissions,
            }

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"letter_{reference_number}",
                {
                    "type": "letter_update",
                    "message": response_data,
                },
            )

            return Response(
                data={"message": "Comment successfully created"},
                status=http_status.HTTP_201_CREATED,
            )

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class CommentUpdateApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_comment_letter"]

    class InputSerializer(serializers.Serializer):
        content = serializers.CharField()

    serializer_class = InputSerializer

    def put(self, request, comment_id):
        comment_instance = get_object_or_404(Comment, pk=comment_id)
        letter_instance = comment_instance.letter
        self.check_object_permissions(request, letter_instance)

        input_instance = self.InputSerializer(data=request.data)
        input_instance.is_valid(raise_exception=True)

        if comment_instance.author != request.user:
            raise PermissionDenied("You do not have permission to update this comment.")

        try:
            comment_update(comment_instance=comment_instance, **input_instance.validated_data)

            output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
            permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

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
            return Response(data={"message": "Comment successfully updated"}, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class CommentDeleteApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter", "can_comment_letter"]

    def delete(self, request, comment_id) -> Response:
        comment_instance = get_object_or_404(Comment, pk=comment_id)
        letter_instance = comment_instance.letter

        if comment_instance.author != request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")

        comment_instance.delete()

        output_serializer = LetterDetailApi.OutputSerializer(letter_instance)
        permissions = self.get_object_permissions_details(letter_instance, current_user=request.user)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"letter_{letter_instance.reference_number}",
            {
                "type": "letter_update",
                "message": {
                    "data": output_serializer.data,
                    "permissions": permissions,
                },
            },
        )

        return Response(data={"message": "Comment successfully deleted"}, status=http_status.HTTP_200_OK)
