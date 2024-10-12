from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from core.emails.services import email_send_type
from .models import User
from django.utils.crypto import get_random_string


@receiver(pre_save, sender=User)
def pre_save_handler(sender, instance, *arg, **kwarg):
    if not instance.password:
        instance.password = get_random_string(length=8)


@receiver(post_save, sender=User)
def post_save_handler(sender, instance, created, *args, **kwargs):
    if created:
        if not instance.password:
            instance.password = get_random_string(length=8)
            email_send_type(
                instance.email,
                "Welcome to Our Service",
                "registration",
                context={
                    "username": instance.email,
                    "default_password": instance.password,
                    "first_name": instance.first_name_en,
                },
            )
        else:
            email_send_type(
                instance.email,
                "Welcome to Our Service",
                "welcome",
                context={
                    "first_name": instance.first_name_en,
                },
            )
