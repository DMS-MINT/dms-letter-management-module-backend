from django.apps import AppConfig


class ParticipantsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.participants"

    # def ready(self):
    #     import core.participants.signals  # noqa: F401
