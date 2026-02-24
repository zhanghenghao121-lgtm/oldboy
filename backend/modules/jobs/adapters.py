from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class JobQuery:
    salary_min: int | None = None
    salary_max: int | None = None
    job_type: str = ""
    work_time: str = ""
    education: str = ""
    region: str = ""


class BaseAdapter:
    source_name = "base"

    def search(self, query: JobQuery) -> list[dict[str, Any]]:
        raise NotImplementedError

    def detail(self, source_job_id: str) -> dict[str, Any] | None:
        raise NotImplementedError

    def normalize(self, raw: dict[str, Any]) -> dict[str, Any]:
        return {
            "source": self.source_name,
            "source_job_id": str(raw.get("source_job_id", "")),
            "source_url": raw.get("source_url", ""),
            "title": raw.get("title", ""),
            "company": raw.get("company", ""),
            "salary_text": raw.get("salary_text", ""),
            "region": raw.get("region", ""),
            "jd": raw.get("jd", ""),
            "tags": raw.get("tags", []),
            "publish_time": raw.get("publish_time"),
            "extra": raw.get("extra", {}),
        }


class MockRecruitmentAdapter(BaseAdapter):
    source_name = "mock_platform"

    def __init__(self):
        self._jobs = [
            {
                "source_job_id": "m001",
                "title": "Python后端工程师",
                "company": "旧友科技",
                "salary_text": "20-35K·14薪",
                "region": "深圳·南山",
                "source_url": "https://example.com/jobs/m001",
                "jd": "岗位职责：负责Django后端开发，优化Redis缓存，参与接口设计。任职要求：熟悉Python、MySQL、Linux。",
                "tags": ["Python", "Django", "Redis", "MySQL"],
                "publish_time": date(2026, 2, 24),
            },
            {
                "source_job_id": "m002",
                "title": "前端开发工程师",
                "company": "旧友科技",
                "salary_text": "15-25K",
                "region": "上海·浦东",
                "source_url": "https://example.com/jobs/m002",
                "jd": "岗位职责：开发小程序和Web前端。任职要求：熟悉Vue3、TypeScript、uni-app。",
                "tags": ["Vue3", "TypeScript", "uni-app"],
                "publish_time": date(2026, 2, 23),
            },
        ]

    def search(self, query: JobQuery) -> list[dict[str, Any]]:
        records = self._jobs
        if query.job_type:
            keyword = query.job_type.lower()
            records = [j for j in records if keyword in j["title"].lower()]
        if query.region:
            records = [j for j in records if query.region in j["region"]]
        return records

    def detail(self, source_job_id: str) -> dict[str, Any] | None:
        for job in self._jobs:
            if job["source_job_id"] == source_job_id:
                return job
        return None


ADAPTERS: list[BaseAdapter] = [MockRecruitmentAdapter()]
