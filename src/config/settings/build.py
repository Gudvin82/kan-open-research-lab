from .base import *  # noqa: F403

SECRET_KEY = "build-only-not-a-runtime-secret"  # noqa: S105
ALLOWED_HOSTS = ["build.invalid"]
STATIC_ROOT = BASE_DIR / "public" / "static"  # noqa: F405
