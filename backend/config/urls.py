from django.contrib import admin
from django.urls import path, include
from modules.common.views import healthz

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz", healthz),
    path("api/v1/", include("modules.jobs.urls")),
]
