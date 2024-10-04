from rest_framework import serializers


class DepartmentSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    department_name_en = serializers.CharField()
    department_name_am = serializers.CharField()
    abbreviation_en = serializers.CharField()
    abbreviation_am = serializers.CharField()
    description = serializers.CharField(allow_blank=True)
    contact_phone = serializers.IntegerField(allow_null=True)
    contact_email = serializers.EmailField(allow_blank=True)


class JobTitleSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title_en = serializers.CharField()
    title_am = serializers.CharField()
