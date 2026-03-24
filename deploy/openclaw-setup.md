# OpenClaw 部署指南

> 详细步骤将在 Phase 4 补充。以下为概要。

## 前提条件

- OpenClaw Gateway 已运行
- Telegram Bot Token 已获取
- 多模态模型可用（推荐 qwen3.5-plus）

## 步骤

1. Clone 本仓库到 OpenClaw workspace 目录
2. 创建 Agent 配置（agent ID、默认模型、personality 指向 agent.md）
3. 绑定 Telegram Bot
4. 配置 Cron 任务：
   - 零点结算（00:00）
   - 结算校验（00:30）
   - 前日汇总（08:00，有记录才发）
   - 周报（周六 20:00）
   - 月报（月末 20:00）
5. 首次对话测试——发送"你好"，确认自动进入 Profile 引导

## 注意事项

- Agent 需要文件读写权限（workspace 目录）
- 推荐使用支持多模态（图片输入）的模型
- 使用云端模型时，对话内容会发送给模型提供商
