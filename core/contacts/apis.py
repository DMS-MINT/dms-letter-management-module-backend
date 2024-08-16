from django.shortcuts import get_list_or_404
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.common.utils import get_object, inline_serializer

from .models import Contact
from .services import contact_create, contact_delete, contact_update


class ContactListApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        full_name_en = serializers.CharField()
        full_name_am = serializers.CharField()
        email = serializers.EmailField()
        phone_number = serializers.IntegerField()
        address = inline_serializer(
            fields={
                "city_en": serializers.CharField(),
                "city_am": serializers.CharField(),
            },
        )

    serializer_class = OutputSerializer

    def get(self, request):
        try:
            contacts = request.user.contacts.all()
            output_serializer = ContactDetailApi.OutputSerializer(contacts, many=True)

            response_data = {"contacts": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class ContactDetailApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        full_name_en = serializers.CharField()
        full_name_am = serializers.CharField()
        email = serializers.EmailField()
        phone_number = serializers.IntegerField()
        address = inline_serializer(
            fields={
                "city_en": serializers.CharField(),
                "city_am": serializers.CharField(),
            },
        )

    serializer_class = OutputSerializer

    def get(self, request, contact_id):
        contact_instance = get_object(Contact, id=contact_id)

        try:
            output_serializer = ContactDetailApi.OutputSerializer(contact_instance)

            response_data = {"contact": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class ContactCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        full_name_en = serializers.CharField()
        full_name_am = serializers.CharField()
        email = serializers.EmailField()
        phone_number = serializers.IntegerField()
        address = inline_serializer(
            fields={
                "city_en": serializers.CharField(),
                "city_am": serializers.CharField(),
            },
        )

    serializer_class = InputSerializer

    def post(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            contact_instance = contact_create(current_user=request.user, **input_serializer.validated_data)
            output_serializer = ContactDetailApi.OutputSerializer(contact_instance)

            response_data = {"contact": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class ContactUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        full_name_en = serializers.CharField()
        full_name_am = serializers.CharField()
        email = serializers.EmailField()
        phone_number = serializers.IntegerField()
        address = inline_serializer(
            fields={
                "city_en": serializers.CharField(),
                "city_am": serializers.CharField(),
            },
        )

    serializer_class = InputSerializer

    def post(self, request, contact_id):
        contact_instance = get_object(Contact, id=contact_id)

        input_serializer = self.InputSerializer(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            contact_instance = contact_update(
                current_user=request.user,
                contact_instance=contact_instance,
                **input_serializer.validated_data,
            )
            output_serializer = ContactDetailApi.OutputSerializer(contact_instance)

            response_data = {"contact": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class ContactDeleteApi(ApiAuthMixin, APIView):
    def delete(self, request, contact_id):
        contact_instance = get_object(Contact, id=contact_id)
        try:
            contact_delete(current_user=request.user, contact_instance=contact_instance)

            response_data = {"message": "Contact removed from your list successfully."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class ContactBulkDeleteApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        contact_ids = serializers.ListSerializer(child=serializers.UUIDField())

    serializer_class = InputSerializer

    def delete(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        contact_ids = input_serializer.validated_data["contact_ids"]

        contacts_to_delete = get_list_or_404(Contact, id__in=contact_ids)

        for contact in contacts_to_delete:
            try:
                contact_delete(current_user=request.user, contact_instance=contact)
            except ValueError as e:
                raise ValidationError(f"Error processing contact with ID {contact.id}: {str(e)}")

            except Exception as e:
                raise ValidationError(e)

        response_data = {"message": "Contacts processed successfully."}

        return Response(data=response_data, status=http_status.HTTP_200_OK)
