import pyotp
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager as BUM  # noqa: N817
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class BaseUserManager(BUM):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        otp_secret = pyotp.random_base32()

        user = self.model(email=email, otp_secret=otp_secret, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, password, **extra_fields)


class User(BaseModel, AbstractUser, PermissionsMixin):
    username = None
    job_title = models.CharField(max_length=254, unique=True, verbose_name=_("Job title"))
    department = models.ForeignKey("departments.Department", on_delete=models.CASCADE)
    phone_number = models.PositiveBigIntegerField(_("phone number"), unique=True)
    email = models.EmailField(blank=False, max_length=255, unique=True, verbose_name=_("Email address"))

    otp_secret = models.TextField(editable=False, null=True, blank=True)
    is_2fa_enabled = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "job_title", "department", "phone_number"]

    class Meta:
        verbose_name: str = "User"
        verbose_name_plural: str = "Users"

    def __str__(self) -> str:
        return f"{self.full_name} - {self.job_title}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
