from __future__ import annotations

from collections import Counter
from datetime import datetime
import re
import requests
from django.conf import settings


def _heuristic_extract(jd: str) -> dict:
    candidates = [
        "Python",
        "Django",
        "DRF",
        "MySQL",
        "Redis",
        "Docker",
        "Linux",
        "Nginx",
        "Vue3",
        "TypeScript",
        "uni-app",
    ]
    found = [c for c in candidates if c.lower() in jd.lower()]
    top = Counter(found)
    skills = [
        {"name": name, "level": "掌握", "evidence": f"JD提及{name}"}
        for name, _ in top.most_common(6)
    ]
    summary = "该岗位侧重工程落地能力与核心技术栈协同，建议重点准备JD中高频技能。"
    return {
        "summary": summary,
        "skills": skills,
        "bonus_skills": ["沟通协作", "问题定位", "文档能力"],
        "risk_points": ["业务变化快，要求学习速度", "需承担跨团队协作"],
        "model": settings.MODEL_NAME or "heuristic-analyzer",
        "generated_at": datetime.now().astimezone().isoformat(),
    }


def analyze_job_jd(jd: str, language: str = "zh") -> dict:
    if not settings.MODEL_API_BASE or not settings.MODEL_API_KEY:
        return _heuristic_extract(jd)

    prompt = (
        "你是招聘技能分析助手。请根据岗位JD输出JSON，字段为"
        "summary, skills(name, level, evidence), bonus_skills, risk_points。"
        "仅返回JSON。"
    )
    payload = {
        "model": settings.MODEL_NAME,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": jd},
        ],
        "temperature": 0.2,
    }
    headers = {
        "Authorization": f"Bearer {settings.MODEL_API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(
            settings.MODEL_API_BASE.rstrip("/") + "/chat/completions",
            json=payload,
            headers=headers,
            timeout=20,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        content = re.sub(r"^```json|```$", "", content.strip(), flags=re.MULTILINE).strip()
        data = requests.models.complexjson.loads(content)
        data["model"] = settings.MODEL_NAME
        return data
    except Exception:
        return _heuristic_extract(jd)
