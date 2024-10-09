from django.apps import AppConfig


class LettersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.letters"

    # def ready(self):
    #     import core.letters.signals  # noqa: F401
