from datetime import UTC, datetime

from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET


def checked_at() -> str:
    return datetime.now(UTC).isoformat()


@require_GET  # type: ignore[untyped-decorator]
def liveness(_request: object) -> JsonResponse:
    return JsonResponse({"status": "ok", "checked_at": checked_at()})


@require_GET  # type: ignore[untyped-decorator]
def readiness(_request: object) -> JsonResponse:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        return JsonResponse(
            {
                "status": "unavailable",
                "code": "database_unavailable",
                "checked_at": checked_at(),
            },
            status=503,
        )
    return JsonResponse({"status": "ready", "checked_at": checked_at()})


@require_GET  # type: ignore[untyped-decorator]
def compute_status(_request: object) -> JsonResponse:
    return JsonResponse(
        {
            "status": "unavailable",
            "code": "compute_node_unavailable",
            "checked_at": checked_at(),
        },
        status=503,
    )
