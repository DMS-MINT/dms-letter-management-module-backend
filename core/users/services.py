from django.core.exceptions import ValidationError

from .models import Guest


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
