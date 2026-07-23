import os

from django.core.asgi import get_asgi_application

default_settings = (
    "src.config.settings.preview"
    if os.environ.get("VERCEL_ENV") == "preview"
    else "src.config.settings.production"
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", default_settings)

application = get_asgi_application()
