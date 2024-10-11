from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class MemberProfile(BaseModel):
    member = models.OneToOneField("members.Member", on_delete=models.CASCADE, related_name="member_profile")

    first_name_en = models.CharField(max_length=35, blank=True, verbose_name=_("First Name (English)"))
    middle_name_en = models.CharField(max_length=35, blank=True, verbose_name=_("Middle Name (English)"))
    last_name_en = models.CharField(max_length=35, blank=True, verbose_name=_("Last Name (English)"))

    first_name_am = models.CharField(max_length=35, blank=True, verbose_name=_("First Name (Amharic)"))
    middle_name_am = models.CharField(max_length=35, blank=True, verbose_name=_("Middle Name (Amharic)"))
    last_name_am = models.CharField(max_length=35, blank=True, verbose_name=_("Last Name (Amharic)"))

    job_title = models.ForeignKey("job_titles.JobTitle", on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey("departments.Department", on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.PositiveBigIntegerField(unique=True, null=True, blank=True, verbose_name=_("phone number"))

    class Meta:
        verbose_name: str = "Member Profile"
        verbose_name_plural: str = "Member Profiles"

    def __str__(self) -> str:
        return f"{self.full_name_en} - {self.job_title}"

    @property
    def full_name_en(self) -> str:
        return f"{self.first_name_en} {self.middle_name_en} {self.last_name_en}"

    @property
    def full_name_am(self) -> str:
        return f"{self.first_name_am} {self.middle_name_am} {self.last_name_am}"
