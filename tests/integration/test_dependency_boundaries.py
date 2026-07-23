from pathlib import Path


def test_web_dependency_graph_has_no_ml_stack():
    pyproject = Path("pyproject.toml").read_text()
    for package in ("torch", "pykan", "efficient-kan"):
        assert package not in pyproject.lower()


def test_worker_compose_does_not_receive_web_secret():
    compose = Path("compose.worker.yaml").read_text()
    assert "DJANGO_SECRET_KEY" not in compose
    assert "POSTGRES_PASSWORD" not in compose
