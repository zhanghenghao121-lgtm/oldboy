from __future__ import annotations

import hashlib
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from modules.common.response import ok, fail
from modules.ai.services import analyze_job_jd
from .models import JobNormalized, JobAnalysisCache
from .serializers import JobSearchSerializer, AnalyzeSerializer
from .services import search_jobs


@api_view(["GET", "POST"])
def job_search(request):
    payload = request.query_params if request.method == "GET" else request.data
    serializer = JobSearchSerializer(data=payload)
    if not serializer.is_valid():
        return fail(message="invalid params", data=serializer.errors)
    try:
        data = search_jobs(serializer.validated_data)
        return ok(data)
    except Exception as exc:
        return fail(
            message="search service error",
            code=5001,
            data={"error": str(exc)},
            status=500,
        )


@api_view(["GET"])
def job_detail(request, job_id: str):
    job = get_object_or_404(JobNormalized, job_id=job_id)
    return ok(
        {
            "job_id": job.job_id,
            "title": job.title,
            "company": job.company,
            "salary_text": job.salary_text,
            "region": job.region,
            "source": job.source,
            "source_url": job.source_url,
            "jd": job.jd,
            "tags": job.tags,
            "company_info": job.extra.get("company_info", {}),
        }
    )


@api_view(["POST"])
def job_analyze(request, job_id: str):
    serializer = AnalyzeSerializer(data=request.data)
    if not serializer.is_valid():
        return fail(message="invalid params", data=serializer.errors)

    job = get_object_or_404(JobNormalized, job_id=job_id)
    payload = serializer.validated_data
    cache_enabled = payload.get("cache", True)
    cache_key = hashlib.sha256(f"{job.job_id}:{job.updated_at.timestamp()}".encode()).hexdigest()

    if cache_enabled:
        existed = JobAnalysisCache.objects.filter(cache_key=cache_key).first()
        if existed:
            return ok(existed.payload)

    data = analyze_job_jd(job.jd, language=payload.get("language", "zh"))
    data.setdefault("generated_at", timezone.now().isoformat())
    data.setdefault("model", "unknown")

    if cache_enabled:
        JobAnalysisCache.objects.update_or_create(
            cache_key=cache_key,
            defaults={
                "job": job,
                "model_name": data.get("model", ""),
                "payload": data,
            },
        )

    return ok(data)
