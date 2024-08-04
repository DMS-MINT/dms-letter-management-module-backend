import datetime

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Incoming, Internal, Letter, Outgoing


def generate_reference_number(instance, new_slug=None, count=1):
    if instance.language == Letter.Languages.AMHARIC:
        department_abbreviation = instance.owner.department.abbreviation_am
        fiscal_year = 2016
    elif instance.language == Letter.Languages.ENGLISH:
        department_abbreviation = instance.owner.department.abbreviation_en
        fiscal_year = datetime.datetime.now().year
    else:
        fiscal_year = datetime.datetime.now().year
        department_abbreviation = "UNK"

    if new_slug:
        slug = new_slug
    else:
        slug = f"{department_abbreviation}-{fiscal_year}-{count:04d}"

    qs = Letter.objects.filter(reference_number=slug).exclude(id=instance.id)

    if qs.exists():
        count += 1
        new_slug = f"{department_abbreviation}-{fiscal_year}-{count:04d}"
        return generate_reference_number(instance, new_slug, count)

    return slug


@receiver(pre_save, sender=Incoming)
@receiver(pre_save, sender=Internal)
@receiver(pre_save, sender=Outgoing)
def letter_pre_save(sender, instance, **kwargs):
    if not instance.reference_number:
        instance.reference_number = generate_reference_number(instance)


@receiver(post_save, sender=Incoming)
@receiver(post_save, sender=Internal)
@receiver(post_save, sender=Outgoing)
def letter_post_save(sender, instance, created, **kwargs):
    if created and not instance.reference_number:
        instance.reference_number = generate_reference_number(instance)
        instance.save()
