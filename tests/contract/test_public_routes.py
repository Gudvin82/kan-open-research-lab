from collections.abc import Iterable

import pytest
from django.test import Client

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
