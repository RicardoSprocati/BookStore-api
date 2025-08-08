"""
Django settings for bookstore project (produção com Docker + Nginx + Gunicorn).
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# Básico / Segurança
# -------------------------------------------------------------------
DEBUG = os.getenv("DEBUG", "0") == "1"
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key-change-me")

# Ex.: "18.188.24.138,example.com,localhost,127.0.0.1"
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]

# Para evitar erro de CSRF atrás de proxy / IP
# Ex.: "http://18.188.24.138,https://example.com"
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]

# Se estiver atrás de proxy/Load Balancer terminando TLS, ative:
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# -------------------------------------------------------------------
# Apps
# -------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework.authtoken",

    "order",
    "product",
]

# debug_toolbar só em desenvolvimento
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar", "django_extensions"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = "bookstore.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bookstore.wsgi.application"

# -------------------------------------------------------------------
# Banco de Dados (usa envs do docker-compose)
# -------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("DB_NAME", str(BASE_DIR / "db.sqlite3")),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# -------------------------------------------------------------------
# Senhas
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------------------------------------------
# i18n / fuso
# -------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Edmonton"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# Arquivos estáticos e de mídia
# -------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Se quiser servir estáticos via Whitenoise dentro do Django (não necessário com Nginx):
# INSTALLED_APPS.insert(0, "whitenoise.runserver_nostatic")
# MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Como estamos servindo via Nginx/volume, deixe o storage padrão do Django:
# (Se você ainda quiser manter o Whitenoise, descomente as 3 linhas acima.)
# Removendo configuração anterior:
# STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# -------------------------------------------------------------------
# DRF
# -------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}

# -------------------------------------------------------------------
# Debug Toolbar (somente em DEV)
# -------------------------------------------------------------------
INTERNAL_IPS = ["127.0.0.1"]
if DEBUG:
    # Em Docker pode precisar ajustar INTERNAL_IPS dinamicamente
    pass

# -------------------------------------------------------------------
# Logging básico para produção (stdout)
# -------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO" if not DEBUG else "DEBUG",
    },
}