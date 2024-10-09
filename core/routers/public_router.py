from django.conf import settings


class PublicRouter:
    shared_django_apps_labels = {"admin", "auth", "contenttypes", "sessions", "messages", "runserver_nostatic"}
    shared_local_apps_labels = {app_config_path.split(".")[1] for app_config_path in settings.SHARED_LOCAL_APPS}

    def db_for_read(self, model, **hints):
        """Point all read operations on shared apps to 'public'."""
        if (
            model._meta.app_label in self.shared_django_apps_labels
            or model._meta.app_label in settings.SHARED_THIRD_PARTY_APPS
            or model._meta.app_label in self.shared_local_apps_labels
        ):
            return "public"
        return None

    def db_for_write(self, model, **hints):
        """Point all write operations on shared apps to 'public'."""
        if (
            model._meta.app_label in self.shared_django_apps_labels
            or model._meta.app_label in settings.SHARED_THIRD_PARTY_APPS
            or model._meta.app_label in self.shared_local_apps_labels
        ):
            return "public"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if a model in the public db is involved."""
        if (
            obj1._meta.app_label in self.shared_django_apps_labels
            or obj2._meta.app_label in self.shared_django_apps_labels
        ):
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Allow migrations for shared apps in the public db."""
        if (
            app_label in self.shared_django_apps_labels
            or app_label in settings.SHARED_THIRD_PARTY_APPS
            or app_label in self.shared_local_apps_labels
        ):
            return db == "public"
        return None
