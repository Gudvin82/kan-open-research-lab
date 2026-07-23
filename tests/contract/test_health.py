from unittest.mock import patch

import pytest
from django.db import OperationalError

pytestmark = pytest.mark.django_db


def test_liveness_has_no_dependency_details(client):
    response = client.get("/health/live/")
    assert response.status_code == 200
    assert set(response.json()) == {"status", "checked_at"}
    assert response.json()["status"] == "ok"


def test_readiness_is_ready_with_database(client):
    response = client.get("/health/ready/")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_readiness_hides_database_failure(client):
    with patch(
        "src.core.views.connection.cursor",
        side_effect=OperationalError("postgresql://user:password@private/db"),
    ):
        response = client.get("/health/ready/")
    assert response.status_code == 503
    assert response.json()["code"] == "database_unavailable"
    assert "password" not in response.content.decode()
