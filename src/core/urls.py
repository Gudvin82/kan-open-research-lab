from django.urls import path

from .views import compute_status, liveness, readiness

urlpatterns = [
    path("health/live/", liveness, name="liveness"),
    path("health/ready/", readiness, name="readiness"),
    path(
        "api/v1/system/compute-status/",
        compute_status,
        name="compute-status",
    ),
]
