from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicManager, PolymorphicModel

from core.common.models import BaseModel


class CustomUserManager(UserManager, PolymorphicManager):
    pass


class BaseUser(PolymorphicModel, BaseModel):
    class Meta:
        verbose_name: str = "User"
        verbose_name_plural: str = "Users"


class Member(AbstractUser, BaseUser):
    job_title = models.CharField(
        _("job title"),
        max_length=254,
        unique=True,
        help_text=_("Enter the job title of the employee."),
    )
    department = models.CharField(
        _("department"),
        max_length=254,
        help_text=_("Enter the department of the employee."),
    )

    phone_number = models.CharField(
        _("phone number"),
        max_length=20,
        unique=True,
        help_text=_("Enter the phone number of the employee."),
    )
    email = models.EmailField(
        _("email address"),
        blank=False,
        max_length=254,
        unique=True,
        help_text=_("Enter the email address of the employee."),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    class Meta:
        verbose_name: str = "Member"
        verbose_name_plural: str = "Members"

    def __str__(self) -> str:
        return f"{self.full_name} - {self.job_title}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Guest(BaseUser):
    name = models.CharField(
        _("Name"),
        max_length=255,
        unique=True,
        help_text=_("Enter the name of the guest."),
    )

    email = models.EmailField(
        _("Email Address"),
        blank=True,
        null=True,
        help_text=_("Enter the email address of the guest."),
    )
    phone_number = models.CharField(
        _("Phone Number"),
        blank=True,
        null=True,
        max_length=20,
        help_text=_("Enter the phone number of the guest."),
    )

    address = models.CharField(
        _("Address"),
        max_length=255,
        blank=True,
        default="Addis Ababa, Ethiopia",
        help_text=_("Enter the address of the guest."),
    )
    postal_code = models.PositiveIntegerField(
        _("Postal Code"),
        blank=True,
        null=True,
        help_text=_("Enter the postal code of the guest."),
    )

    class Meta:
        verbose_name: str = "Guest"
        verbose_name_plural: str = "Guests"

    def __str__(self) -> str:
        return self.name
