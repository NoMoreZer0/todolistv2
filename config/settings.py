# flake8: noqa
import hashlib
import os
from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR.joinpath("app")
env = environ.Env()
environ.Env.read_env(str(BASE_DIR / ".env"))

# GENERAL
# -----------------------------------------------------------------------------
DEBUG = True

SECRET_KEY = env.str("SECRET_KEY", "secretkey")

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LOCALE_NAME = "ru"

LOCALE_PATHS = [str(BASE_DIR / "locale")]

LIST_PER_PAGE = 20

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CONTAINER_ENVIRONMENT = env.str("CONTAINER_ENVIRONMENT", "local")
BUILD_VERSION = env.str("BUILD_VERSION", "0.1.0")

# INTERNATIONALIZATION
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "ru"

gettext = lambda s: s  # noqa

TIME_ZONE = "Asia/Aqtobe"

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

THOUSAND_SEPARATOR = " "

NUMBER_GROUPING = 3

LANGUAGES = [
    ("ru", gettext("Russian")),
    ("kk", gettext("Kazakh")),
    ("en", gettext("English")),
]

# HOSTS
# -----------------------------------------------------------------------------
ALLOWED_HOSTS = ["*"]

# APPLICATIONS
# -----------------------------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = ["app.core.apps.CoreConfig"]

THIRD_PARTY_APPS = [
    "drf_spectacular",
    "rest_framework",
    "waffle",
    "rest_framework.authtoken",
    "django_dramatiq",
    "imagekit",
    "corsheaders"
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
SITE_URL = "http://localhost:19000"

# DRAMATIQ_SETTINGS
# -----------------------------------------------------------------------------

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.rabbitmq.RabbitmqBroker",
    "OPTIONS": {
        "url": env.str("RABBITMQ_BROKER_URL", ""),
        "confirm_delivery": True,
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
    ],
}

# SPECTACULAR_SETTINGS
# -----------------------------------------------------------------------------

SPECTACULAR_SETTINGS = {
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "TITLE": "TodoList API",
    "DESCRIPTION": "Another one todolist",
    "SERVERS": [{"url": SITE_URL}],
    "SWAGGER_UI_SETTINGS": {
        "displayRequestDuration": True,
    },
}

# MIDDLEWARES
# -----------------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "waffle.middleware.WaffleMiddleware",
]

# TEMPLATES
# -----------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [APP_DIR.joinpath("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": [
                "django.templatetags.static",
                "waffle.templatetags.waffle_tags",
            ],
        },
    }
]
# STATIC
# -----------------------------------------------------------------------------
STATIC_ROOT = "/static"
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_ROOT = "/media"

# DATABASE
# -----------------------------------------------------------------------------
DATABASES = {"default": env.db(), "deploy": env.db(), "readonly": env.db()}

# REST FRAMEWORK
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# EMAIL BACKEND
# -----------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str("EMAIL_HOST", "")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", "")
FROM_EMAIL = env.str("FROM_EMAIL", "")
EMAIL_PORT = env.int("EMAIL_PORT", 587)
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_ON = env.bool("EMAIL_ON", False)

# AUTH
# -----------------------------------------------------------------------------
AUTH_USER_MODEL = "core.User"


