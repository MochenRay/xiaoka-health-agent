# Workspace

此目录存放用户的个人健康数据，不会被提交到 Git。

仓库标准约定：

- 用户档案和目标文件在根目录 `config/` 下
- 运行时健康数据全部放在 `workspace/` 下
- 每日日志和结算 JSON 使用按月分目录的路径，而不是根目录平铺

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

以下根目录路径视为旧版部署遗留，不再作为仓库标准：

- `logs/`
- `data/`
- `medical/`
- `reports/`
- `food-library/`
