# Workspace

此目录存放用户的个人健康数据，不会被提交到 Git。

## 目录结构

首次使用时由 Agent 自动创建：

```
workspace/
├── logs/YYYY-MM/DD.md        — 每日 Markdown 日志
├── data/YYYY-MM/DD.json      — 零点结算后的结构化 JSON
├── medical/YYYY-MM-DD-*.md   — 体检报告解读
├── reports/                   — 周报/月报
└── food-library/my-foods.json — 用户自建常吃食物库
```
