# Phase 1 最小可用约定

本文件定义仓库当前承诺的 Phase 1 最小可用标准，用来约束路径、初始化行为和数据落点。

## 目标

Phase 1 的目标只有一件事：

- clone 仓库后，Agent 能完成初始化，并马上开始记录饮食、体重、体检等基础数据

以下能力不属于 Phase 1 完成标准：

- Apple Health 解析脚本
- 周报/月报自动生成
- Cron 任务定义随仓库同步
- 深度分析模块的完整自动化闭环

## 标准路径

仓库标准只认这一套路径：

- `config/profile.md`
- `config/goals.md`
- `workspace/logs/YYYY-MM/DD.md`
- `workspace/data/YYYY-MM/DD.json`
- `workspace/medical/YYYY-MM-DD-*.md`
- `workspace/reports/weekly-YYYY-MM-DD.md`
- `workspace/reports/monthly-YYYY-MM.md`
- `workspace/food-library/my-foods.json`

说明：

- `config/` 只放用户档案和目标
- `workspace/` 放所有运行时健康数据
- 日志与 JSON 都按月分目录，避免根目录平铺

## 初始化约定

首次使用时，如果 `config/profile.md` 不存在或缺少必填字段，Agent 应：

1. 进入引导式问答，补齐必填档案字段
2. 计算 BMR、TDEE、热量目标和宏量目标
3. 生成 `config/profile.md` 与 `config/goals.md`
4. 确保以下目录存在：
   - `workspace/logs/`
   - `workspace/data/`
   - `workspace/medical/`
   - `workspace/reports/`
   - `workspace/food-library/`
5. 如 `workspace/food-library/my-foods.json` 不存在，初始化为 `[]`

## 写入约定

- 饮食、体重、运动、睡眠、补剂的白天写入目标是 `workspace/logs/YYYY-MM/DD.md`
- 零点结算后的结构化目标是 `workspace/data/YYYY-MM/DD.json`
- 体检解读归档到 `workspace/medical/`
- 周报/月报归档到 `workspace/reports/`
- 自建食物库写入 `workspace/food-library/my-foods.json`

## 兼容性说明

以下根目录路径视为旧版部署遗留，仓库不再将其视为标准：

- `logs/`
- `data/`
- `medical/`
- `reports/`
- `food-library/`

如果已有本地 Cron 或脚本仍在读写这些旧路径，启用自动化前应先迁移。
