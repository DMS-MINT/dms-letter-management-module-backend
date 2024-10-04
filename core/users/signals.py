import pyotp
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import User


@receiver(pre_save, sender=User)
def set_otp_secret(instance, **kwargs):
    if instance.otp_secret:
        instance.otp_secret = pyotp.random_base32()
