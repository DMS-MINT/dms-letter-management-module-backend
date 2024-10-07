from django.db import transaction

from .models import JobTitle


@transaction.atomic
def job_title_create(*, title_en: str, title_am: str):
    return JobTitle.objects.create(
        title_en=title_en,
        title_am=title_am,
    )


@transaction.atomic
def job_title_update(
    *,
    job_title_instance: JobTitle,
    title_en: str = None,
    title_am: str = None,
):
    if title_en is not None:
        job_title_instance.title_en = str(title_en)

    if title_am is not None:
        job_title_instance.title_am = str(title_am)

    return job_title_instance
