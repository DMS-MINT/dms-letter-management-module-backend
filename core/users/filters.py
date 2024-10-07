from enum import Enum

import django_filters
from django.db.models import Q

from .models import User


class Filter(Enum):
    ALL = "all"
    STAFF = "staff"
    SUPERUSER = "superuser"
    STAFF_AND_SUPERUSER = "staff_and_superuser"


class BaseUserFilter(django_filters.FilterSet):
    filter = django_filters.CharFilter(method="filter_by_filter")

    class Meta:
        model = User
        fields = []

    def filter_by_filter(self, queryset, name, value):
        match value:
            case Filter.ALL.value:
                return self.filter_all(queryset)
            case Filter.STAFF.value:
                return self.filter_staff(queryset)
            case Filter.SUPERUSER.value:
                return self.filter_superuser(queryset)
            case Filter.STAFF_AND_SUPERUSER.value:
                return self.filter_staff_and_superuser(queryset)
            case _:
                return queryset.none()

    def filter_all(self, queryset):
        return queryset

    def filter_staff(self, queryset):
        return queryset.filter(is_staff=True)

    def filter_superuser(self, queryset):
        return queryset.filter(is_superuser=True)

    def filter_staff_and_superuser(self, queryset):
        return queryset.filter(Q(is_staff=True) & Q(is_superuser=True))
