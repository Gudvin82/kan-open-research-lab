from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.urls import translate_url

from .content import UI


def public_shell(request: HttpRequest) -> dict[str, Any]:
    locale = getattr(request, "LANGUAGE_CODE", "ru")
    if locale not in UI:
        locale = "ru"
    other_locale = "en" if locale == "ru" else "ru"
    counterpart_path = translate_url(request.path, other_locale)
    public_base_url = settings.PUBLIC_BASE_URL.rstrip("/")

    def absolute_url(path: str) -> str:
        normalized_path = path if path.startswith("/") else f"/{path}"
        return f"{public_base_url}{normalized_path}"

    return {
        "locale": locale,
        "other_locale": other_locale,
        "ui": UI[locale],
        "current_url": absolute_url(request.path),
        "ru_url": (
            request.path if locale == "ru" else translate_url(request.path, "ru")
        ),
        "en_url": (
            request.path if locale == "en" else translate_url(request.path, "en")
        ),
        "counterpart_url": counterpart_path,
        "indexing_disabled": not settings.PUBLIC_INDEXING_ENABLED,
        "ru_absolute_url": absolute_url(
            request.path if locale == "ru" else translate_url(request.path, "ru")
        ),
        "en_absolute_url": absolute_url(
            request.path if locale == "en" else translate_url(request.path, "en")
        ),
    }
