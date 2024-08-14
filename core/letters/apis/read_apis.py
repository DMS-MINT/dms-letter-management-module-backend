from django.http import HttpResponse
from guardian.shortcuts import assign_perm
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_polymorphic.serializers import PolymorphicSerializer

from core.api.mixins import ApiAuthMixin
from core.common.utils import get_object
from core.letters.models import Incoming, Internal, Letter, Outgoing
from core.letters.selectors import letter_list, letter_pdf
from core.letters.serializers import LetterDetailPolymorphicSerializer, LetterListSerializer
from core.permissions.mixins import ApiPermMixin


class LetterPdfView(APIView):
    def get(self, request, reference_number) -> Response:
        letter_instance = get_object(Letter, reference_number=reference_number)

        try:
            pdf_content = letter_pdf(letter_instance=letter_instance)

            response = HttpResponse(pdf_content, content_type="application/pdf")
            response["Content-Disposition"] = f'inline; filename="letter_{letter_instance.reference_number}.pdf"'

            return response

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterListApi(ApiAuthMixin, APIView):
    class FilterSerializer(serializers.Serializer):
        category = serializers.ChoiceField(
            choices=["inbox", "outbox", "draft", "trash", "pending", "published"],
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

    serializer_class = FilterSerializer

    def get(self, request) -> Response:
        try:
            filter_serializer = self.FilterSerializer(data=request.query_params)
            filter_serializer.is_valid(raise_exception=True)

            letter_instances = letter_list(current_user=request.user, filters=filter_serializer.validated_data)

            serializer = self.OutputSerializer(letter_instances, many=True)

            response_data = {"letters": serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LetterDetailApi(ApiAuthMixin, ApiPermMixin, APIView):
    required_object_perms = ["can_view_letter"]

    serializer_class = LetterDetailPolymorphicSerializer

    def get(self, request, reference_number) -> Response:
        current_user = request.user
        letter_instance = get_object(Letter, reference_number=reference_number)

        if isinstance(letter_instance, Incoming):
            if request.user.is_staff:
                assign_perm("can_view_letter", request.user, letter_instance)
                assign_perm("can_reject_letter", request.user, letter_instance)
                assign_perm("can_publish_letter", request.user, letter_instance)

        else:
            if request.user.is_staff and letter_instance.current_state in [
                Letter.States.SUBMITTED,
                Letter.States.PUBLISHED,
            ]:
                assign_perm("can_view_letter", request.user, letter_instance)
                assign_perm("can_reject_letter", request.user, letter_instance)
                assign_perm("can_publish_letter", request.user, letter_instance)

        try:
            self.check_object_permissions(request, letter_instance)

            output_serializer = LetterDetailPolymorphicSerializer(letter_instance, many=False)
            permissions = self.get_object_permissions_details(letter_instance, current_user)

            response_data = {"letter": output_serializer.data, "permissions": permissions}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
