from .base import *  # noqa: F403

SECRET_KEY = "test-only-not-a-secret"  # noqa: S105
DEBUG = False
PUBLIC_BASE_URL = "http://testserver"
ALLOWED_HOSTS = ["testserver"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
STORAGES["staticfiles"] = {  # noqa: F405
    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
}
