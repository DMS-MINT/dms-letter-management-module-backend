from enum import Enum

import django_filters
from django.db.models import Q

from .models import Member


class Filter(Enum):
    ALL = "all"
    ADMIN = "admin"
    STAFF = "staff"
    STAFF_AND_ADMIN = "staff_and_admin"


class BaseMemberFilter(django_filters.FilterSet):
    filter = django_filters.CharFilter(method="filter_by_filter")
    include_current_user = django_filters.BooleanFilter(method="filter_by_current_user", required=False)

    def __init__(self, data=None, queryset=None, *, current_user=None, **kwargs):
        super().__init__(data, queryset, **kwargs)
        self.current_user = current_user

    class Meta:
        model = Member
        fields = []

    def filter_by_filter(self, queryset, name, value):
        match value:
            case Filter.ALL.value:
                return self.filter_all(queryset)
            case Filter.STAFF.value:
                return self.filter_staff(queryset)
            case Filter.ADMIN.value:
                return self.filter_admin(queryset)
            case Filter.STAFF_AND_ADMIN.value:
                return self.filter_staff_and_admin(queryset)
            case _:
                return queryset.none()

    def filter_all(self, queryset):
        return queryset

    def filter_staff(self, queryset):
        return queryset.filter(member_permissions__is_staff=True)

    def filter_admin(self, queryset):
        return queryset.filter(member_permissions__is_admin=True)

    def filter_staff_and_admin(self, queryset):
        return queryset.filter(Q(member_permissions__is_staff=True) & Q(member_permissions__is_admin=True))

    def filter_by_current_user(self, queryset, name, value):
        current_user = self.current_user
        if not value:
            return queryset.exclude(user_id=current_user.id)
        return queryset
