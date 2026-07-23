import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "").strip()
if not SECRET_KEY:
    raise ImproperlyConfigured("Required setting is missing: DJANGO_SECRET_KEY")
if os.environ.get("DATABASE_URL") and os.environ.get("DATABASE_ENV") != "preview":
    raise ImproperlyConfigured("Preview DATABASE_URL requires DATABASE_ENV=preview")
ALLOWED_HOSTS = [".vercel.app"]
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
