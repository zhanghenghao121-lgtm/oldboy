# API 文档

## 通用返回

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

## 健康检查
- `GET /healthz`

## 岗位搜索
- `POST /api/v1/jobs/search`

请求示例：
```json
{
  "salary_min": 15000,
  "salary_max": 30000,
  "job_type": "后端开发",
  "work_time": "全职",
  "education": "本科",
  "region": "深圳",
  "page": 1,
  "page_size": 20
}
```

## 岗位详情
- `GET /api/v1/jobs/{job_id}`

## 技能分析
- `POST /api/v1/jobs/{job_id}/analyze`

请求示例：
```json
{
  "mode": "skills_summary",
  "language": "zh",
  "cache": true
}
```
