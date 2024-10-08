import os

from config.env import APPS_DIR, BASE_DIR, env

env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-eb7x*euse3jj879p3vtb_^gbolpga@rl$18pqnn93@t0n*@!$a"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)  # type: ignore

ALLOWED_HOSTS: list[str] = ["*"]

# Shared Third-Party Applications
# These are third-party apps that are used across all tenants

SHARED_THIRD_PARTY_APPS: list[str] = [
    "corsheaders",
    "django_browser_reload",
    "django_filters",
    "django_tenants",
    "drf_spectacular",
    "tailwind",
    "tenant_users.permissions",
    "tenant_users.tenants",
    "theme",
]

# Shared Local Applications
# These are apps that are part of the core system and shared by all tenants

SHARED_LOCAL_APPS: list[str] = [
    "core.authentication.apps.AuthenticationConfig",
    "core.organizations.apps.OrganizationsConfig",
    "core.common.apps.CommonConfig",
    "core.users.apps.UsersConfig",
]

# Shared Apps (Django + Shared Third-Party and Local Apps)
# A combination of core Django apps, shared third-party apps, and shared local apps

SHARED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    *SHARED_THIRD_PARTY_APPS,
    *SHARED_LOCAL_APPS,
]

# Tenant-Specific Third-Party Applications
# These apps are specific to each tenant

TENANT_THIRD_PARTY_APPS: list[str] = [
    # "easyaudit",
    "corsheaders",
    "polymorphic",
    "django_extensions",
    "rest_framework",
    "guardian",
    "tenant_users.permissions",
]

# Tenant-Specific Local Applications
# These are tenant-specific local apps providing functionality to each tenant

TENANT_LOCAL_APPS: list[str] = [
    "core.api.apps.ApiConfig",
    "core.attachments.apps.AttachmentsConfig",
    "core.comments.apps.CommentsConfig",
    "core.common.apps.CommonConfig",
    "core.contacts.apps.ContactsConfig",
    "core.departments.apps.DepartmentsConfig",
    "core.emails.apps.EmailsConfig",
    "core.enterprises.apps.EnterprisesConfig",
    "core.job_titles.apps.JobTitlesConfig",
    "core.letters.apps.LettersConfig",
    "core.notifications.apps.NotificationsConfig",
    "core.participants.apps.ParticipantsConfig",
    "core.permissions.apps.PermissionsConfig",
    "core.signatures.apps.SignaturesConfig",
    "core.user_management.apps.UserManagementConfig",
    "core.workflows.apps.WorkflowsConfig",
]

# Tenant Apps (Django + Tenant-Specific Apps)
# A combination of core Django apps, tenant-specific third-party, and local apps

TENANT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    *TENANT_THIRD_PARTY_APPS,
    *TENANT_LOCAL_APPS,
]

# Installed Applications
# This is the final list of installed apps combining both shared and tenant apps,

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

# Middleware Configuration

MIDDLEWARE: list[str] = [
    "django_tenants.middleware.main.TenantMainMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "tenant_users.tenants.middleware.TenantAccessMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
    # "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(APPS_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI and ASGI Configuration

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD"),
        "HOST": env.str("DB_HOST"),
        "PORT": env.str("DB_PORT"),
    },
}

DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = (
    "tenant_users.permissions.backend.UserBackend",
    "guardian.backends.ObjectPermissionBackend",
)

ANONYMOUS_USER_NAME = None
GUARDIAN_GET_CONTENT_TYPE = "polymorphic.contrib.guardian.get_polymorphic_base_content_type"

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

INTERNAL_IPS = [env.str("INTERNAL_IPS", default="http://localhost:8000")]

APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")  # type: ignore

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "core", "static"),
]

TAILWIND_APP_NAME = "theme"

# Settings for configuring the Django REST Framework.
# https://www.django-rest-framework.org/api-guide/settings/#settings
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "core.api.exception_handler.drf_exception_handler",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# https://drf-spectacular.readthedocs.io/en/latest/settings.html#example-swaggerui-settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Document Management System API",
    "DESCRIPTION": "Documentation for the Document Management System APIs.",
    "VERSION": "2.0.0",
}

from config.settings.tenant import *  # noqa
from config.settings.celery import *  # noqa
from config.settings.logging import *  # noqa
from config.settings.cors import *  # noqa
from config.settings.email_sending import *  # noqa
from config.settings.files_and_storages import *  # noqa
from config.settings.sessions import *  # noqa

from config.settings.debug_toolbar.settings import *  # noqa
from config.settings.debug_toolbar.setup import DebugToolbarSetup  # noqa


INSTALLED_APPS, MIDDLEWARE = DebugToolbarSetup.do_settings(INSTALLED_APPS, MIDDLEWARE)
