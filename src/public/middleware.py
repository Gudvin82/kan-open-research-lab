from collections.abc import Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse


class LocalePreferenceMiddleware:
    """Persist an explicit locale URL without overriding future explicit URLs."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        locale = getattr(request, "LANGUAGE_CODE", "")
        path_locale = request.path_info.strip("/").split("/", 1)[0]
        if locale in {"ru", "en"} and path_locale == locale:
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME,
                locale,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                secure=not settings.DEBUG,
                httponly=False,
                samesite=settings.LANGUAGE_COOKIE_SAMESITE,
            )
        return response
