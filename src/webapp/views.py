from typing import Any

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .content import METHODS, PAGES, RESEARCH, UI, PageCopy


def _locale(request: HttpRequest) -> str:
    locale = getattr(request, "LANGUAGE_CODE", "ru")
    return locale if locale in {"ru", "en"} else "ru"


def _base_context(request: HttpRequest, page_key: str) -> dict[str, Any]:
    locale = _locale(request)
    return {
        "page": PAGES[locale][page_key],
        "nav_key": page_key,
        "methods": METHODS[locale].values(),
    }


@require_GET  # type: ignore[untyped-decorator]
def home(request: HttpRequest) -> HttpResponse:
    locale = _locale(request)
    context = _base_context(request, "home")
    context.update(
        {
            "research_cards": RESEARCH[locale],
            "featured_cards": RESEARCH[locale][:2],
        }
    )
    return render(request, "lab/pages/home.html", context)


@require_GET  # type: ignore[untyped-decorator]
def research(request: HttpRequest) -> HttpResponse:
    locale = _locale(request)
    context = _base_context(request, "research")
    cards = RESEARCH[locale]
    context.update(
        {
            "reproduced_cards": tuple(
                card for card in cards if card.collection == "reproduced"
            ),
            "open_cards": tuple(card for card in cards if card.collection == "open"),
        }
    )
    return render(request, "lab/pages/research.html", context)


@require_GET  # type: ignore[untyped-decorator]
def methods(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "lab/pages/methods.html",
        _base_context(request, "methods"),
    )


@require_GET  # type: ignore[untyped-decorator]
def method_detail(request: HttpRequest, method: str) -> HttpResponse:
    locale = _locale(request)
    method_copy = METHODS[locale].get(method)
    if method_copy is None:
        raise Http404
    page = PageCopy(
        key=f"method-{method}",
        title=method_copy.title,
        eyebrow=PAGES[locale]["methods"].title,
        summary=method_copy.summary,
        description=method_copy.summary,
    )
    return render(
        request,
        "lab/pages/method_detail.html",
        {
            "page": page,
            "nav_key": "methods",
            "method": method_copy,
            "methods": METHODS[locale].values(),
        },
    )


@require_GET  # type: ignore[untyped-decorator]
def knowledge(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "lab/pages/knowledge.html",
        _base_context(request, "knowledge"),
    )


@require_GET  # type: ignore[untyped-decorator]
def about(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "lab/pages/about.html",
        _base_context(request, "about"),
    )


def not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    del exception
    locale = _locale(request)
    page = PageCopy(
        key="not-found",
        title=UI[locale]["not_found_title"],
        eyebrow="404",
        summary=UI[locale]["not_found_summary"],
        description=UI[locale]["not_found_summary"],
    )
    return render(
        request,
        "lab/pages/404.html",
        {
            "page": page,
            "nav_key": "",
            "methods": METHODS[locale].values(),
        },
        status=404,
    )
