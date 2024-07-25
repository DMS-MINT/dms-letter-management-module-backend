from django.db.models import Model
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import NotFound

from core.api.exceptions import APIError


def get_list(model_or_queryset, **kwargs):
    try:
        return get_list_or_404(model_or_queryset)
    except Http404:
        raise NotFound("Users Not Found")


def get_model_name(model_or_queryset):
    if isinstance(model_or_queryset, QuerySet):
        return model_or_queryset.model.__name__
    if isinstance(model_or_queryset, type) and issubclass(model_or_queryset, Model):
        return model_or_queryset.__name__

    raise ValueError("Invalid model or queryset")


def get_object(model_or_queryset, **kwargs):
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        model_name = get_model_name(model_or_queryset)
        raise APIError(
            error_code=f"{model_name.upper()}_NOT_FOUND",
            status_code=http_status.HTTP_404_NOT_FOUND,
            message="Not Found Error",
            extra={"detail": f"The requested {model_name.lower()} was not found."},
        )


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name="inline_serializer", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
