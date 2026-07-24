import os

from django.core.exceptions import ImproperlyConfigured

from src.config.public_urls import normalize_public_base_url

from .base import *  # noqa: F403

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "").strip()
if not SECRET_KEY:
    raise ImproperlyConfigured("Required setting is missing: DJANGO_SECRET_KEY")
DEBUG = False
if os.environ.get("DATABASE_URL") and os.environ.get("DATABASE_ENV") != "preview":
    raise ImproperlyConfigured("Preview DATABASE_URL requires DATABASE_ENV=preview")
preview_host = os.environ.get("VERCEL_URL", "preview.vercel.app")
ALLOWED_HOSTS = [
    normalize_public_base_url(preview_host, source="VERCEL_URL").removeprefix(
        "https://"
    )
]
PUBLIC_BASE_URL = normalize_public_base_url(preview_host, source="VERCEL_URL")
PUBLIC_INDEXING_ENABLED = False
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
