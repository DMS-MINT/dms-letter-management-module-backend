from django.core.management import call_command
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.members.services import set_owner

from .middleware import set_db_for_router
from .models import Tenant


@receiver(post_save, sender=Tenant)
def create_tenant_database(sender, instance, created, **kwargs):
    if created:
        # tenant_database_name = instance.database_name
        tenant_database_name = "tenant"
        try:
            call_command("migrate", database=tenant_database_name)
        except Exception as e:
            raise ValueError(e)

        set_db_for_router(tenant_database_name)

        set_owner(current_user=instance.owner, tenant_instance=instance)
