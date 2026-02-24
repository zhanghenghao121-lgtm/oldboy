from __future__ import annotations

import hashlib
import json
from django.core.cache import cache
from .adapters import ADAPTERS, JobQuery
from .models import JobNormalized


def _cache_key(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return f"{prefix}:{hashlib.md5(raw.encode('utf-8')).hexdigest()}"


def search_jobs(params: dict) -> dict:
    key = _cache_key("jobs:search", params)
    cached = cache.get(key)
    if cached:
        return cached

    query = JobQuery(
        salary_min=params.get("salary_min"),
        salary_max=params.get("salary_max"),
        job_type=params.get("job_type", ""),
        work_time=params.get("work_time", ""),
        education=params.get("education", ""),
        region=params.get("region", ""),
    )
    merged: list[dict] = []
    for adapter in ADAPTERS:
        for raw in adapter.search(query):
            normalized = adapter.normalize(raw)
            job = _upsert_job(normalized)
            merged.append(_to_api_item(job))

    page = params.get("page", 1)
    page_size = params.get("page_size", 20)
    total = len(merged)
    start = (page - 1) * page_size
    end = start + page_size
    data = {
        "page": page,
        "page_size": page_size,
        "total": total,
        "list": merged[start:end],
    }
    cache.set(key, data, timeout=300)
    return data


def _upsert_job(normalized: dict) -> JobNormalized:
    source = normalized["source"]
    source_job_id = normalized.get("source_job_id", "")
    defaults = {
        "source_url": normalized.get("source_url", ""),
        "title": normalized.get("title", ""),
        "company": normalized.get("company", ""),
        "salary_text": normalized.get("salary_text", ""),
        "region": normalized.get("region", ""),
        "jd": normalized.get("jd", ""),
        "tags": normalized.get("tags", []),
        "publish_time": normalized.get("publish_time"),
        "extra": normalized.get("extra", {}),
    }
    obj, created = JobNormalized.objects.get_or_create(
        source=source,
        source_job_id=source_job_id,
        defaults={"job_id": JobNormalized.new_job_id(), **defaults},
    )
    if not created:
        changed = False
        for k, v in defaults.items():
            if getattr(obj, k) != v:
                setattr(obj, k, v)
                changed = True
        if changed:
            obj.save(update_fields=list(defaults.keys()) + ["updated_at"])
    return obj


def _to_api_item(job: JobNormalized) -> dict:
    return {
        "job_id": job.job_id,
        "title": job.title,
        "company": job.company,
        "salary_text": job.salary_text,
        "region": job.region,
        "source": job.source,
        "source_url": job.source_url,
        "tags": job.tags,
        "publish_time": job.publish_time.isoformat() if job.publish_time else "",
    }
