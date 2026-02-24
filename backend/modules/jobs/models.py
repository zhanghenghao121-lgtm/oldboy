import uuid
from django.db import models


class JobNormalized(models.Model):
    id = models.BigAutoField(primary_key=True)
    job_id = models.CharField(max_length=64, unique=True, db_index=True)
    source = models.CharField(max_length=64)
    source_job_id = models.CharField(max_length=128, blank=True, default="")
    source_url = models.URLField(max_length=500, blank=True, default="")
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    salary_text = models.CharField(max_length=100, blank=True, default="")
    region = models.CharField(max_length=100, blank=True, default="")
    jd = models.TextField(blank=True, default="")
    tags = models.JSONField(default=list)
    publish_time = models.DateField(null=True, blank=True)
    extra = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["source", "source_job_id"]),
            models.Index(fields=["title", "company"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["source", "source_job_id"],
                name="uniq_source_source_job_id",
            )
        ]

    @staticmethod
    def new_job_id() -> str:
        return f"job_{uuid.uuid4().hex[:12]}"


class JobAnalysisCache(models.Model):
    id = models.BigAutoField(primary_key=True)
    job = models.ForeignKey(JobNormalized, on_delete=models.CASCADE, related_name="analysis")
    cache_key = models.CharField(max_length=128, unique=True)
    model_name = models.CharField(max_length=128, blank=True, default="")
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["job", "updated_at"])]
