from django.conf import settings

from core.tenants.middleware import get_current_db_name


class TenantRouter:
    tenant_local_apps_labels = {app_config_path.split(".")[1] for app_config_path in settings.TENANT_LOCAL_APPS}

    def db_for_read(self, model, **hints):
        """Point all read operations on tenant apps to 'tenant'."""
        if (
            model._meta.app_label in settings.TENANT_THIRD_PARTY_APPS
            or model._meta.app_label in self.tenant_local_apps_labels
        ):
            return get_current_db_name()
        return None

    def db_for_write(self, model, **hints):
        """Point all write operations on tenant apps to 'tenant'."""
        if (
            model._meta.app_label in settings.TENANT_THIRD_PARTY_APPS
            or model._meta.app_label in self.tenant_local_apps_labels
        ):
            return get_current_db_name()
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if a model in the tenant db is involved."""
        if (
            obj1._meta.app_label in self.tenant_local_apps_labels
            or obj2._meta.app_label in self.tenant_local_apps_labels
        ):
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Allow migrations for tenant apps in the tenant db."""
        if app_label in settings.TENANT_THIRD_PARTY_APPS or app_label in self.tenant_local_apps_labels:
            return db == get_current_db_name()
        return False
