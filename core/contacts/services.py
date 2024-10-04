from django.db import transaction

from core.common.models import Address
from core.users.models import User

from .models import Contact


@transaction.atomic
def contact_create(
    *,
    current_user: User,
    full_name_en: str,
    full_name_am: str,
    email: str,
    phone_number: str,
    address: dict,
):
    address_instance, _ = Address.objects.get_or_create(
        city_en=address.get("city_en"),
        city_am=address.get("city_am"),
    )
    contact_instance, _ = Contact.objects.get_or_create(
        full_name_en=full_name_en,
        full_name_am=full_name_am,
        email=email,
        phone_number=phone_number,
        address=address_instance,
    )

    current_user.contacts.add(contact_instance)

    return contact_instance


@transaction.atomic
def contact_update(
    *,
    current_user: User,
    contact_instance: Contact,
    full_name_en: str,
    full_name_am: str,
    email: str,
    phone_number: str,
    address: dict,
):
    number_of_related_users = contact_instance.user.count()

    if number_of_related_users > 1:
        contact_instance.user.remove(current_user)
        return contact_create(
            current_user=current_user,
            full_name_en=full_name_en,
            full_name_am=full_name_am,
            email=email,
            phone_number=phone_number,
            address=address,
        )

    existing_contact = (
        Contact.objects.filter(
            full_name_en=full_name_en,
            full_name_am=full_name_am,
            address=address,
        )
        .exclude(id=contact_instance.id)
        .first()
    )

    if existing_contact:
        # Check if the contact is referenced in any letter if not delete it outre wise don't delete it
        contact_delete(current_user=current_user, contact_instance=contact_instance)
        existing_contact.user.add(current_user)
        return existing_contact

    contact_instance.full_name_en = full_name_en
    contact_instance.full_name_am = full_name_am
    contact_instance.email = email
    contact_instance.phone_number = phone_number
    contact_instance.address = address

    contact_instance.save()

    return contact_instance


def contact_delete(
    *,
    current_user: User,
    contact_instance: Contact,
):
    number_of_related_users = contact_instance.user.count()

    if number_of_related_users > 1:
        contact_instance.user.remove(current_user)
        return

    contact_instance.delete()
    return
