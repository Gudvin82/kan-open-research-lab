import pytest
from django.test import Client


@pytest.mark.parametrize("locale", ("ru", "en"))
def test_research_collections_and_claim_boundary(client: Client, locale: str) -> None:
    response = client.get(f"/{locale}/research/")
    html = response.content.decode()

    assert 'data-research-collection="reproduced"' in html
    assert 'data-research-collection="open"' in html
    assert 'data-field="scientific-status"' in html
    assert 'data-field="method"' in html
    assert 'data-field="evidence-level"' in html
    assert 'data-field="reproducibility"' in html
    if locale == "ru":
        assert "задача остаётся открытой" in html.lower()
        assert "численный результат не является доказательством" in html.lower()
    else:
        assert "problem remains open" in html.lower()
        assert "numerical result is not a proof" in html.lower()


@pytest.mark.parametrize("locale", ("ru", "en"))
@pytest.mark.parametrize("method", ("kan", "mlp", "pinn", "comparison"))
def test_method_pages_have_all_explanation_levels(
    client: Client, locale: str, method: str
) -> None:
    response = client.get(f"/{locale}/methods/{method}/")
    html = response.content.decode()

    for level in ("human", "technical", "scientific"):
        assert f'id="{level}"' in html
        assert f'href="#{level}"' in html
    assert 'data-performance-claim="none"' in html


@pytest.mark.parametrize("locale", ("ru", "en"))
def test_footer_contains_only_approved_external_destination(
    client: Client, locale: str
) -> None:
    response = client.get(f"/{locale}/")
    html = response.content.decode()

    assert "https://github.com/Gudvin82/kan-open-research-lab" in html
    assert "mailto:" not in html
    assert "cookie" not in html.lower()
    assert "analytics" not in html.lower()
    assert "privacy policy" not in html.lower()


def test_compute_state_remains_unavailable(client: Client) -> None:
    response = client.get("/ru/")

    assert "compute_node_unavailable" in response.content.decode()
