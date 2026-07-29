import os

from django.core.exceptions import ImproperlyConfigured

from src.config.public_urls import (
    normalize_public_base_url,
    unique_hosts,
)

from .base import *  # noqa: F403


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ImproperlyConfigured(f"Required setting is missing: {name}")
    return value


SECRET_KEY = required("DJANGO_SECRET_KEY")

immutable_url = os.environ.get("VERCEL_URL", "")
stable_url = os.environ.get("PUBLIC_BASE_URL", "") or os.environ.get(
    "VERCEL_PROJECT_PRODUCTION_URL", ""
)
if not immutable_url.strip() or not stable_url.strip():
    raise ImproperlyConfigured(
        "Production host configuration is missing: VERCEL_URL and either "
        "PUBLIC_BASE_URL or VERCEL_PROJECT_PRODUCTION_URL are required"
    )

host_sources = [
    ("VERCEL_URL", immutable_url),
    (
        "VERCEL_PROJECT_PRODUCTION_URL",
        os.environ.get("VERCEL_PROJECT_PRODUCTION_URL", ""),
    ),
    ("PUBLIC_BASE_URL", os.environ.get("PUBLIC_BASE_URL", "")),
]
host_sources.extend(
    ("DJANGO_ALLOWED_HOSTS", value)
    for value in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
)
ALLOWED_HOSTS = unique_hosts((source, value) for source, value in host_sources if value)
PUBLIC_BASE_URL = normalize_public_base_url(
    stable_url,
    source=(
        "PUBLIC_BASE_URL"
        if os.environ.get("PUBLIC_BASE_URL", "").strip()
        else "VERCEL_PROJECT_PRODUCTION_URL"
    ),
)
PUBLIC_INDEXING_ENABLED = False

# Vercel serves the build output from ``public/static`` at the edge. The Python
# function does not receive that collectstatic manifest, so runtime URL
# generation must not depend on reading it from ``/var/task/staticfiles``.
if os.environ.get("VERCEL_ENV") == "production":
    STORAGES = {  # noqa: F405
        **STORAGES,  # noqa: F405
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
    MIDDLEWARE = [  # noqa: F405
        middleware
        for middleware in MIDDLEWARE  # noqa: F405
        if middleware != "whitenoise.middleware.WhiteNoiseMiddleware"
    ]

if os.environ.get("DATABASE_URL") and os.environ.get("DATABASE_ENV") != "production":
    raise ImproperlyConfigured(
        "Production DATABASE_URL requires DATABASE_ENV=production"
    )

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31_536_000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
