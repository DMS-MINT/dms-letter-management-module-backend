import datetime

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Incoming, Internal, Letter, Outgoing


def generate_reference_number(instance, new_slug=None, new_slug_am=None, count=1):
    department = instance.owner.department
    fiscal_year = datetime.datetime.now().year

    if new_slug:
        slug = new_slug
        slug_am = new_slug_am
    else:
        slug = f"{department.abbreviation_en}-{fiscal_year}-{count:04d}"
        slug_am = f"{department.abbreviation_am}-2016-{count:04d}"

    qs = Letter.objects.filter(reference_number=slug).exclude(id=instance.id)

    if qs.exists():
        count += 1
        new_slug = f"{department.abbreviation_en}-{fiscal_year}-{count:04d}"
        new_slug_am = f"{department.abbreviation_am}-2016-{count:04d}"
        return generate_reference_number(instance, new_slug, new_slug_am, count)

    return slug, slug_am


@receiver(pre_save, sender=Incoming)
@receiver(pre_save, sender=Internal)
@receiver(pre_save, sender=Outgoing)
def letter_pre_save(sender, instance, **kwargs):
    if not instance.reference_number:
        slug, slug_am = generate_reference_number(instance)

        instance.reference_number = slug
        instance.reference_number_am = slug_am


@receiver(post_save, sender=Incoming)
@receiver(post_save, sender=Internal)
@receiver(post_save, sender=Outgoing)
def letter_post_save(sender, instance, created, **kwargs):
    if created and not instance.reference_number:
        slug, slug_am = generate_reference_number(instance)

        instance.reference_number = slug
        instance.reference_number_am = slug_am
