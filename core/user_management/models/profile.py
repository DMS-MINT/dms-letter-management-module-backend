from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class UserProfile(BaseModel):
    member = models.ForeignKey("user_management.Member", on_delete=models.CASCADE, related_name="member_profile")

    first_name_en = models.CharField(max_length=35, blank=True, verbose_name=_("First Name (English)"))
    middle_name_en = models.CharField(max_length=35, blank=True, verbose_name=_("Middle Name (English)"))
    last_name_en = models.CharField(max_length=35, blank=True, verbose_name=_("Last Name (English)"))

    first_name_am = models.CharField(max_length=35, blank=True, verbose_name=_("First Name (Amharic)"))
    middle_name_am = models.CharField(max_length=35, blank=True, verbose_name=_("Middle Name (Amharic)"))
    last_name_am = models.CharField(max_length=35, blank=True, verbose_name=_("Last Name (Amharic)"))

    job_title = models.ForeignKey("job_titles.JobTitle", on_delete=models.CASCADE)
    department = models.ForeignKey("departments.Department", on_delete=models.CASCADE)
    phone_number = models.PositiveBigIntegerField(_("phone number"), unique=True)

    class Meta:
        unique_together = ("member",)
        verbose_name: str = "User Profile"
        verbose_name_plural: str = "User Profiles"

    def __str__(self) -> str:
        return f"{self.full_name_en} - {self.job_title}"

    @property
    def full_name_en(self) -> str:
        return f"{self.first_name_en} {self.middle_name_en} {self.last_name_en}"

    @property
    def full_name_am(self) -> str:
        return f"{self.first_name_am} {self.middle_name_am} {self.last_name_am}"
