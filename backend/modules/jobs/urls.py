from django.urls import path
from .views import job_search, job_detail, job_analyze

urlpatterns = [
    path("jobs/search", job_search),
    path("jobs/<str:job_id>", job_detail),
    path("jobs/<str:job_id>/analyze", job_analyze),
]
