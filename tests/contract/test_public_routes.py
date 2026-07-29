from collections.abc import Iterable

import pytest
from django.test import Client, override_settings

PRIMARY_PATHS = (
    "",
    "research/",
    "methods/",
    "knowledge/",
    "about/",
)
METHOD_PATHS = (
    "methods/kan/",
    "methods/mlp/",
    "methods/pinn/",
    "methods/comparison/",
)


@pytest.mark.parametrize("locale", ("ru", "en"))
@pytest.mark.parametrize("path", (*PRIMARY_PATHS, *METHOD_PATHS))
def test_public_routes_render_without_database(
    client: Client, locale: str, path: str
) -> None:
    response = client.get(f"/{locale}/{path}")

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/html")
    assert response.context["request"].LANGUAGE_CODE == locale


@pytest.mark.parametrize("locale", ("ru", "en"))
@pytest.mark.parametrize("path", PRIMARY_PATHS)
def test_primary_pages_have_semantic_contract(
    client: Client, locale: str, path: str
) -> None:
    response = client.get(f"/{locale}/{path}")
    html = response.content.decode()

    required_fragments: Iterable[str] = (
        f'<html lang="{locale}"',
        'class="skip-link"',
        "<header",
        '<nav aria-label="',
        '<main id="main-content"',
        "<footer",
        'rel="canonical"',
        'hreflang="ru"',
        'hreflang="en"',
        "<h1",
    )
    for fragment in required_fragments:
        assert fragment in html


def test_root_redirects_deterministically_to_russian(client: Client) -> None:
    response = client.get("/", HTTP_ACCEPT_LANGUAGE="en-US,en;q=0.9")

    assert response.status_code == 302
    assert response.headers["Location"] == "/ru/"


def test_public_shell_does_not_require_a_database(client: Client) -> None:
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("DATABASE_URL", "")
        response = client.get("/ru/")

    assert response.status_code == 200


@pytest.mark.parametrize(
    ("locale", "title"),
    (("ru", "Страница не найдена"), ("en", "Page not found")),
)
def test_not_found_page_is_localized(client: Client, locale: str, title: str) -> None:
    response = client.get(f"/{locale}/missing-page/")
    html = response.content.decode()

    assert response.status_code == 404
    assert f'<html lang="{locale}"' in html
    assert f"<h1>{title}</h1>" in html
    assert f'href="/{locale}/"' in html


@override_settings(
    PUBLIC_BASE_URL="https://kan-open-research-lab.vercel.app",
    ALLOWED_HOSTS=[
        "testserver",
        "kan-open-research-immutable-test.vercel.app",
    ],
)
@pytest.mark.parametrize("locale", ("ru", "en"))
def test_canonical_and_hreflang_use_stable_base_not_request_host(
    client: Client, locale: str
) -> None:
    response = client.get(
        f"/{locale}/research/",
        HTTP_HOST="kan-open-research-immutable-test.vercel.app",
    )
    html = response.content.decode()

    assert (
        '<link rel="canonical" '
        f'href="https://kan-open-research-lab.vercel.app/{locale}/research/">'
    ) in html
    assert (
        '<link rel="alternate" hreflang="ru" '
        'href="https://kan-open-research-lab.vercel.app/ru/research/">'
    ) in html
    assert (
        '<link rel="alternate" hreflang="en" '
        'href="https://kan-open-research-lab.vercel.app/en/research/">'
    ) in html
    assert "kan-open-research-immutable-test.vercel.app" not in html
