import pytest
from django.conf import settings
from django.test import Client

COUNTERPARTS = (
    ("/ru/", "/en/"),
    ("/ru/research/", "/en/research/"),
    ("/ru/methods/", "/en/methods/"),
    ("/ru/knowledge/", "/en/knowledge/"),
    ("/ru/about/", "/en/about/"),
    ("/ru/methods/kan/", "/en/methods/kan/"),
    ("/ru/methods/mlp/", "/en/methods/mlp/"),
    ("/ru/methods/pinn/", "/en/methods/pinn/"),
    ("/ru/methods/comparison/", "/en/methods/comparison/"),
)


@pytest.mark.parametrize(("russian", "english"), COUNTERPARTS)
def test_language_switch_preserves_entity(
    client: Client, russian: str, english: str
) -> None:
    ru_response = client.get(russian)
    en_response = client.get(english)

    assert f'href="{english}" hreflang="en"' in ru_response.content.decode()
    assert f'href="{russian}" hreflang="ru"' in en_response.content.decode()


@pytest.mark.parametrize(("locale", "path"), (("ru", "/ru/"), ("en", "/en/")))
def test_explicit_locale_is_persisted(client: Client, locale: str, path: str) -> None:
    response = client.get(path)

    assert response.cookies[settings.LANGUAGE_COOKIE_NAME].value == locale
    assert response.cookies[settings.LANGUAGE_COOKIE_NAME]["samesite"] == "Lax"


def test_url_locale_overrides_existing_preference(client: Client) -> None:
    client.cookies[settings.LANGUAGE_COOKIE_NAME] = "en"
    response = client.get("/ru/about/")

    assert response.context["request"].LANGUAGE_CODE == "ru"
    assert response.cookies[settings.LANGUAGE_COOKIE_NAME].value == "ru"


@pytest.mark.parametrize("path", ("/de/", "/fr/research/", "/ru/unknown/"))
def test_unsupported_or_unknown_locale_path_is_not_redirected(
    client: Client, path: str
) -> None:
    response = client.get(path)

    assert response.status_code == 404
