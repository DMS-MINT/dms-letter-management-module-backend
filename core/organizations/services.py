import time
from typing import Optional, Tuple

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django_tenants.utils import (
    get_public_schema_name,
    get_tenant_domain_model,
    get_tenant_model,
    schema_context,
)
from tenant_users.tenants.models import ExistsError, InactiveError
from tenant_users.tenants.utils import (  # noqa: F811
    get_public_schema_name,
    get_tenant_domain_model,
    get_tenant_model,
    get_user_model,
)

from core.common.models import Address

from .models import OrganizationProfile

INACTIVE_USER_ERROR_MESSAGE = "Inactive user can't be used to provision an organization."
UserModel = get_user_model()
TenantModel = get_tenant_model()
DomainModel = get_tenant_domain_model()


def create_public_organization(
    domain_url,
    owner_email,
    *,
    is_superuser: bool = False,
    is_staff: bool = False,
    organization_extra_data: Optional[dict] = None,
    verbosity=1,
    **owner_extra,
):
    """Creates a public organization and assigns an owner user.

    This function sets up a new organization in a multi-tenant Django application. It assigns an
    owner user to the organization, with the option to specify additional user and organization attributes.

    Args:
        domain_url (str): The URL for the organization's domain.
        owner_email (str): Email address of the owner user.
        is_superuser (bool): If True, the owner has superuser privileges. Defaults to False.
        is_staff (bool): If True, the owner has staff access. Defaults to False.
        organization_extra_data (dict, optional): Additional data for the organization model.
        **owner_extra: Arbitrary keyword arguments for additional owner user attributes.

    Returns:
        tuple: A tuple containing the organization object, domain object, and user object.
    """
    if organization_extra_data is None:
        organization_extra_data = {}

    public_schema_name = get_public_schema_name()

    if TenantModel.objects.filter(schema_name=public_schema_name).first():
        raise ExistsError(f"Organization with this schema name{public_schema_name} already exists")

    # Create an organization user. This user doesn't go through object manager
    # create_user function because organization does not exist yet
    profile = UserModel.objects.create(
        email=owner_email,
        is_active=True,
        **owner_extra,
    )

    public_organization = TenantModel(
        schema_name=public_schema_name,
        owner=profile,
        **organization_extra_data,
    )

    public_organization.save(verbosity=verbosity)

    # Add one or more domains for the organization
    domain = get_tenant_domain_model().objects.create(
        domain=domain_url,
        tenant=public_organization,
        is_primary=True,
    )

    # Add system user to public organization (no permissions)
    public_organization.add_user(profile, is_superuser=is_superuser, is_staff=is_staff)

    # Handle setting the password for the user
    if "password" in owner_extra:
        profile.set_password(owner_extra["password"])
    else:
        profile.set_unusable_password()
    profile.save(update_fields=["password"])

    return public_organization, domain, profile


@transaction.atomic()
def create_organization(  # noqa: PLR0913
    organization_slug: str,
    current_user: UserModel,  # type: ignore
    *,
    name_en: str,
    name_am: str,
    is_staff: bool = False,
    is_superuser: bool = True,
    bio: str = None,
    contact_phone: int = None,
    contact_email: str = None,
    postal_code: int = None,
    address: dict = None,
    logo=None,
) -> Tuple[TenantModel, DomainModel]:  # type: ignore
    """Creates and initializes a new organization with specified attributes and default roles.

    Args:
        organization_slug (str): A unique slug for the organization. It's used to create the schema_name.
        owner(UserModel): The owner (User) of the provision organization.
        is_staff (bool, optional): If True, the user has staff access. Defaults to False.
        is_superuser (bool, optional): If True, the user has all permissions. Defaults to True.
        organization_extra_data (dict, optional): Additional data for the organization model.

    Returns:
        tuple: A tuple containing:
            - organization object: The provisioned organization instance created.
            - domain object: The Fully Qualified Domain Name (FQDN) instance for the newly provisioned organization.

    Raises:
        InactiveError: If the user is inactive.
        ExistsError: If the organization URL already exists.
        SchemaError: If the organization type is not valid.
    """

    if not current_user.is_active:
        raise InactiveError(INACTIVE_USER_ERROR_MESSAGE)

    organization_primary_domain = f"{organization_slug}.{settings.TENANT_USERS_DOMAIN}"
    organization_admin_domain = f"{organization_slug}.admin.{settings.TENANT_USERS_DOMAIN}"

    if DomainModel.objects.filter(domain=organization_primary_domain).exists():
        raise ExistsError("Organization domain already exists.")

    time_string = str(int(time.time()))
    # Must be valid postgres schema characters see:
    # https://www.postgresql.org/docs/9.2/static/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS
    schema_name = f"{organization_slug}_{time_string}"

    # Attempt to create the organization and domain within the schema context
    with schema_context(get_public_schema_name()):
        # Create a new organization instance with provided data
        organization_instance = TenantModel.objects.create(
            slug=organization_slug,
            schema_name=schema_name,
            owner=current_user,
            name_en=name_en,
            name_am=name_am,
        )

        # Create a domain associated with the organization and mark as primary
        DomainModel.objects.create(domain=organization_primary_domain, tenant=organization_instance, is_primary=True)
        DomainModel.objects.create(domain=organization_admin_domain, tenant=organization_instance, is_primary=False)

        # Add the user to the organization with provided roles
        organization_instance.add_user(current_user, is_superuser=is_superuser, is_staff=is_staff)

        address_instance, _ = Address.objects.get_or_create(
            city_en=address.get("city_en"),
            city_am=address.get("city_am"),
        )

        OrganizationProfile.objects.create(
            organization=organization_instance,
            bio=bio,
            address=address_instance,
            contact_phone=contact_phone,
            contact_email=contact_email,
            postal_code=postal_code,
            logo=logo,
        )

    return organization_instance.id


@transaction.atomic
def update_organization(
    *,
    organization_instance: TenantModel,
    name_en: str = None,
    name_am: str = None,
    bio: str = None,
    address: dict = None,
    contact_phone: int = None,
    contact_email: str = None,
    postal_code: int = None,
    logo=None,
):
    organization_profile = organization_instance.organization_profile.first()

    if name_en is not None:
        organization_instance.name_en = str(name_en)

    if name_am is not None:
        organization_instance.name_am = str(name_am)

    organization_instance.save()

    if bio is not None:
        organization_profile.bio = str(bio)

    if contact_phone is not None:
        organization_profile.contact_phone = int(contact_phone)

    if contact_email is not None:
        organization_profile.contact_email = str(contact_email)

    if postal_code is not None:
        organization_profile.postal_code = str(postal_code)

    if logo is not None:
        organization_profile.logo = logo

    organization_profile.save()

    return organization_instance
