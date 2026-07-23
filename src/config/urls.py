from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

handler404 = "src.webapp.views.not_found"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("src.core.urls")),
    path("", RedirectView.as_view(url="/ru/", permanent=False), name="public-root"),
]

urlpatterns += i18n_patterns(
    path("", include("src.webapp.urls")),
    prefix_default_language=True,
)
