from django.db import transaction

from .models import Department


@transaction.atomic
def department_create(
    *,
    department_name_en: str,
    department_name_am: str,
    abbreviation_en: str,
    abbreviation_am: str,
    description: str = None,
    contact_phone: int = None,
    contact_email: str = None,
):
    return Department.objects.create(
        department_name_en=department_name_en,
        department_name_am=department_name_am,
        abbreviation_en=abbreviation_en,
        abbreviation_am=abbreviation_am,
        description=description,
        contact_phone=contact_phone,
        contact_email=contact_email,
    )


@transaction.atomic
def department_update(
    *,
    department_instance: Department,
    department_name_en: str = None,
    department_name_am: str = None,
    abbreviation_en: str = None,
    abbreviation_am: str = None,
    description: str = None,
    contact_phone: int = None,
    contact_email: str = None,
):
    if department_name_en is not None:
        department_instance.department_name_en = str(department_name_en)

    if department_name_am is not None:
        department_instance.department_name_am = str(department_name_am)

    if abbreviation_en is not None:
        department_instance.abbreviation_en = str(abbreviation_en)

    if abbreviation_am is not None:
        department_instance.abbreviation_am = str(abbreviation_am)

    if description is not None:
        department_instance.description = str(description)

    if contact_phone is not None:
        department_instance.contact_phone = int(contact_phone)

    if contact_email is not None:
        department_instance.contact_email = str(contact_email)

    department_instance.save()
    return department_instance
