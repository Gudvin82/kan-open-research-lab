from django.urls import path

from . import views

app_name = "public"

urlpatterns = [
    path("", views.home, name="home"),
    path("research/", views.research, name="research"),
    path("methods/", views.methods, name="methods"),
    path("methods/<slug:method>/", views.method_detail, name="method-detail"),
    path("knowledge/", views.knowledge, name="knowledge"),
    path("about/", views.about, name="about"),
]
