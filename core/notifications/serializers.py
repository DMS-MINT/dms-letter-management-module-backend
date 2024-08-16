from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    subject = serializers.CharField()
    message = serializers.CharField()
    details = serializers.JSONField(default=dict)
    sent_at = serializers.DateTimeField()

    tags = serializers.SerializerMethodField()
    has_read = serializers.SerializerMethodField()
    has_notified = serializers.SerializerMethodField()

    def get_tags(self, obj) -> list[str]:
        return [tag.name for tag in obj.tags.all()]

    def get_has_read(self, obj) -> bool:
        current_user = self.context.get("user")

        recipient = obj.notification_recipients.filter(user=current_user).first()

        return recipient.has_read if recipient else False

    def get_has_notified(self, obj) -> bool:
        current_user = self.context.get("user")

        recipient = obj.notification_recipients.filter(user=current_user).first()

        return recipient.has_notified if recipient else False
