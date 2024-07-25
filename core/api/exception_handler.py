from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions
from rest_framework import status as http_status
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler

from .exceptions import APIError, ApplicationError


def drf_exception_handler(exc, context):
    """
    {
        "error_code": "Error code",
        "message": "Error message",
        "extra": {}
    }
    """
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, APIError):
        data = exc.to_dict()
        return Response(data, status=exc.status_code)

    response = exception_handler(exc, context)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        if isinstance(exc, ApplicationError):
            data = {
                "error_code": exc.error_code or "APPLICATION_ERROR",
                "message": exc.message,
                "extra": exc.extra,
            }
            return Response(data, status=http_status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "extra": {},
            },
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if isinstance(exc.detail, (list, dict)):
        response.data = {"detail": response.data}

    if isinstance(exc, exceptions.ValidationError):
        response.data["error_code"] = "VALIDATION_ERROR"
        response.data["message"] = "Validation error"  # type: ignore
        response.data["extra"] = {"fields": response.data["detail"]}  # type: ignore
    else:
        response.data["error_code"] = "VALIDATION_ERROR"
        response.data["message"] = response.data["detail"]  # type: ignore
        response.data["extra"] = {}  # type: ignore

    del response.data["detail"]  # type: ignore

    return response
