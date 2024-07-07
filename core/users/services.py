from typing import Optional

from django.core.exceptions import ValidationError

from .models import Department, Guest, Member


def user_create(
    *,
    first_name: str,
    last_name: str,
    job_title: str,
    department: str,
    email: str,
    phone_number: str,
    is_active: bool = True,
    is_staff: bool = False,
    is_superuser: bool = False,
    password: Optional[str] = None,
) -> Member:
    department_instance = Department.objects.get(name=department)

    return (
        Member.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            job_title=job_title,
            department=department_instance,
            email=email,
            phone_number=phone_number,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            password=password,
        ),
    )


def guest_create(*, validated_data):
    name = validated_data.get("name")
    email = validated_data.get("email", "")
    address = validated_data.get("address", "")
    phone_number = validated_data.get("phone_number", "")
    postal_code = validated_data.get("postal_code")

    existing_guest = Guest.objects.filter(name=name).first()
    if existing_guest:
        return existing_guest

    try:
        new_guest = Guest.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            address=address,
            postal_code=postal_code,
        )

    except ValidationError as e:
        raise ValueError(f"Unable to create guest: {e}")

    return new_guest
