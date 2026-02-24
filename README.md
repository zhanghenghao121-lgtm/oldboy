# Oldboy 招聘聚合 + 技能分析

已实现：
- Django/DRF 后端 API：`/healthz`、`/api/v1/jobs/search`、`/api/v1/jobs/{job_id}`、`/api/v1/jobs/{job_id}/analyze`
- 数据模型：`JobNormalized`、`JobAnalysisCache`
- 招聘来源适配器框架（默认 Mock）
- Docker Compose 部署编排（Nginx + Backend + MariaDB + Redis）
- uni-app 小程序联调骨架（搜索/详情/分析页）

开发文档：`docs/开发文档.md`
