from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.letters.models import Letter

from .services import comment_create, comment_update


class CommentCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        content = serializers.CharField()

    def post(self, request, letter_id):
        letter_instance = get_object_or_404(Letter, pk=letter_id)
        input_instance = self.InputSerializer(data=request.data)
        input_instance.is_valid(raise_exception=True)

        try:
            comment_create(user=request.user, letter_instance=letter_instance, **input_instance.validated_data)
            return Response(data={"message": "Comment successfully created"}, status=http_status.HTTP_201_CREATED)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class CommentUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        content = serializers.CharField()

    def put(self, request, comment_id):
        comment_instance = get_object_or_404(Letter, pk=comment_id)
        input_instance = self.InputSerializer(data=request.data)
        input_instance.is_valid(raise_exception=True)

        if comment_instance.author != request.user:
            raise PermissionDenied("You do not have permission to update this comment.")

        try:
            comment_update(comment_instance=comment_instance, **input_instance.validated_data)
            return Response(data={"message": "Comment successfully updated"}, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class CommentDeleteApi(ApiAuthMixin, APIView):
    def delete(self, request, comment_id) -> Response:
        comment_instance = get_object_or_404(Letter, pk=comment_id)

        if comment_instance.author != request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")

        comment_instance.delete()
        return Response(status=http_status.HTTP_204_NO_CONTENT)
