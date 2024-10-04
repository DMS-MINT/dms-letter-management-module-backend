from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.emails.services import email_send_type
from core.users.models import User

from .models import Notification, NotificationRecipient, Tag
from .serializers import NotificationSerializer
from .services import notification_create, notification_send


class NotificationListApi(ApiAuthMixin, APIView):
    serializer_class = NotificationSerializer

    def get(self, request) -> Response:
        try:
            notifications = Notification.objects.filter(notification_recipients__user=request.user).distinct()
            output_serializer = NotificationSerializer(
                notifications,
                many=True,
                context={"user": request.user},
            )

            response_data = {"notifications": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class MarkNotificationAsRead(ApiAuthMixin, APIView):
    def put(self, request, notification_id) -> Response:
        try:
            recipient = NotificationRecipient.objects.select_related("notification").get(
                notification_id=notification_id,
                user=request.user,
            )

            recipient.has_read = True
            recipient.save()

            response_data = {"message": "Notification marked as read."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class BulkMarkNotificationAsRead(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        ids = serializers.ListField(child=serializers.UUIDField())

    serializer_class = InputSerializer

    def put(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        ids = input_serializer.get("ids")
        try:
            with transaction.atomic():
                recipients = NotificationRecipient.objects.filter(notification_id__in=ids, user=request.user)

                recipients.update(has_read=True)

            response_data = {"message": "Notifications marked as read."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class MarkNotificationAsNotified(ApiAuthMixin, APIView):
    def put(self, request, notification_id) -> Response:
        try:
            recipient = NotificationRecipient.objects.select_related("notification").get(
                notification_id=notification_id,
                user=request.user,
            )

            recipient.has_notified = True
            recipient.save()

            response_data = {"message": "Notification marked as read."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class SendReminderApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        to = serializers.ListField(child=serializers.UUIDField())
        message = serializers.CharField(required=False)
        channels = serializers.ListField(child=serializers.CharField(), required=False, default=["in-app"])
        details = serializers.JSONField()

        def validate_channel(self, value):
            valid_channels = {"sms", "email", "in-app"}

            if any(channel not in valid_channels for channel in value):
                raise serializers.ValidationError("Invalid channel specified.")

            return value

    serializer_class = InputSerializer

    def post(self, request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            reminder_tag, _ = Tag.objects.get_or_create(name="Reminder")
            letter_tag, _ = Tag.objects.get_or_create(name="Letter")

            tags = [reminder_tag, letter_tag]
            subject = f"Reminder Notification from {request.user.full_name_en}"

            # details = {
            #     "notification_type":""
            # }


            if "email" in input_serializer.validated_data.get("channels", []):
                recipients = input_serializer.validated_data.get("to", [])
                notification_message = input_serializer.validated_data.get("message")

                user_email=[]               
                for uuid in recipients:
                    user = get_object_or_404(User, id=uuid)
                    user_email.append(user.email)
                    
                for email in user_email:
                    email_send_type(
                        to=email,                             
                        subject=subject,                     
                        template_name="notification",        
                        context={
                            "notification_message":notification_message,
                            "first_name": user.first_name_en
                            }     
                )
                


            notification_instance = notification_create(subject=subject, tags=tags, **input_serializer.validated_data)

            # transaction.on_commit(lambda: send_notifications_task.delay(notification_id))

            response_data = {"message": "Reminder sent successfully"}

            notification_send(notification_instance=notification_instance)

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
