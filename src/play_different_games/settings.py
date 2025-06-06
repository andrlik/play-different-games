# settings.py
#
# Copyright (c) 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import sys
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from environs import Env

env = Env()
env.read_env()

TESTING = "test" in sys.argv or "tox" in sys.argv

TIMEZONE = "UTC"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_TZ = True

with env.prefixed("DJANGO_"):
    # 1. Django Core Settings

    DEBUG = env.bool("DEBUG", False)
    SECRET_KEY = env.str(
        "SECRET_KEY",
        default="django-insecure-e)%i&m34u01!9vwuj4^89p5!shewk-2f+_$+^31d2vr2eovog1",
    )
    PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
    BASE_DIR = Path(PROJECT_DIR, "src")
    APPS_DIR = Path(BASE_DIR, "play_different_games")
    LOCALE_PATHS = [str(APPS_DIR / "locale")]

    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
    ADMIN_URL = env.str("ADMIN_URL", default="admin/")

    DATABASES = {
        "default": env.dj_db_url(
            "DATABASE_URL", default="postgres:///playdifferentgames"
        ),
    }
    DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql"
    DATABASES["default"]["ATOMIC_REQUESTS"] = True
    DATABASES["default"]["CONN_MAX_AGE"] = 300

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    DJANGO_APPS = [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # "django.contrib.humanize", # Handy template tags
        "django.contrib.admin",
        "django.forms",
    ]

    FIRST_PARTY_APPS = [
        "play_different_games.core",
        "play_different_games.users",
        "play_different_games.catalog",
    ]

    THIRD_PARTY_APPS = [
        "prune_media",
        "isbn_field",
        "django_browser_reload",
        "django_watchfiles",
        "django_q",
        "compressor",
        "crispy_forms",
        "crispy_bulma",
        "rules.apps.AutodiscoverRulesConfig",
        "django_htmx",
        "template_partials",
    ]

    if env("AWS_ACCESS_KEY_ID", default=None):  # no cov
        THIRD_PARTY_APPS += ["storages"]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django_htmx.middleware.HtmxMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django_browser_reload.middleware.BrowserReloadMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "play_different_games.users.middleware.TimezoneMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        # "django.middleware.common.BrokenLinkEmailsMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    if DEBUG and not TESTING:  # no cov
        THIRD_PARTY_APPS += ["debug_toolbar"]
        MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")

    INSTALLED_APPS = DJANGO_APPS + FIRST_PARTY_APPS + THIRD_PARTY_APPS

    CACHES = {
        "default": env.dj_cache_url(
            "CACHE_URL", default="locmem://play_different_games"
        )
    }
    CACHES["default"]["KEY_PREFIX"] = "PDG_"

    if not DEBUG:  # no cov
        SESSION_ENGINE = "django.contrib.sessions.backends.cache"
        SESSION_CACHE_ALIAS = "default"

    # Storages
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        }
    }
    if "storages" in INSTALLED_APPS:  # no cov
        STORAGES = {
            "default": {
                "BACKEND": "storages.backends.s3.S3Storage",
            }
        }
        _AWS_EXPIRY = 60 * 60 * 24 * 7
        AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", default=None)
        AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", default=None)
        AWS_STORAGE_BUCKET_NAME = env.str("AWS_BUCKET_NAME", default=None)
        AWS_S3_REGION_NAME = env.str("AWS_REGION_NAME", default=None)
        AWS_S3_ENDPOINT_URL = env.str("AWS_ENDPOINT_URL", default=None)
        AWS_DEFAULT_ACL = env.str("AWS_DEFAULT_ACL", default=None)
        AWS_S3_CUSTOM_DOMAIN = env.str("AWS_CUSTOM_DOMAIN", default=None)
        AWS_S3_OBJECT_PARAMETERS = {
            "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate"  # noqa: E501
        }

    # Static Files
    STORAGES["staticfiles"] = {  # type: ignore
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    }
    STATICFILES_DIRS = [str(APPS_DIR / "static")]
    STATIC_URL = env.str("STATIC_URL", default="/static/")
    STATIC_ROOT = str(PROJECT_DIR / "staticfiles")
    STATICFILES_FINDERS = [
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        "compressor.finders.CompressorFinder",
    ]

    # Media
    MEDIA_ROOT = str(PROJECT_DIR / "media")
    MEDIA_URL = "/media/"

    ROOT_URLCONF = "play_different_games.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [APPS_DIR / "templates"],
            # "APP_DIRS": True,
            "OPTIONS": {
                "debug": DEBUG,
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.template.context_processors.tz",
                    "django.contrib.messages.context_processors.messages",
                    "play_different_games.context_processors.provide_version",
                ],
                "loaders": [
                    (
                        "django.template.loaders.cached.Loader",
                        [
                            "django.template.loaders.filesystem.Loader",
                            "django.template.loaders.app_directories.Loader",
                        ],
                    ),
                ],
            },
        },
    ]

    if not DEBUG:  # no cov
        if "django-insecure" in SECRET_KEY:
            msg = "You are using an insecure SECRET_KEY in production mode."
            raise ImproperlyConfigured(msg)

        # SECURITY
        # ------------------------------------------------------------------------------
        # https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
        # https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
        SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
        # https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
        SESSION_COOKIE_SECURE = True
        # https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
        CSRF_COOKIE_SECURE = True
        # https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
        # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
        # TODO: set this to 60 seconds first and then to 518400 once you prove the former works  # noqa: E501
        SECURE_HSTS_SECONDS = 60
        # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
        SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
            "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
        )
        # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
        SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
        # https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
        SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
            "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
        )

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

AUTHENTICATION_BACKENDS = (
    "rules.permissions.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
)

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "rules": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "play_different_games": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
    },
}

# Django Q
Q_CLUSTER = {
    "name": "play_different_games",
    "compress": True,
    "timeout": 120,
    "retry": 240,
    "save_limit": 250,
    "label": "Django Q2",
    "orm": "default",
    "sync": False,
}

CRISPY_ALLOWED_TEMPLATE_PACKS = ("bulma",)

CRISPY_TEMPLATE_PACK = "bulma"

LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"
