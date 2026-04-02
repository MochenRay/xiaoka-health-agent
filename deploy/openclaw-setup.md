# OpenClaw 部署指南

## 前提条件

- OpenClaw Gateway 已运行
- Telegram Bot Token 已获取（从 @BotFather 创建）
- 多模态模型可用（推荐 `bailian/qwen3.5-plus`）

## 步骤

### 1. Clone 仓库到 workspace

```bash
cd ~/.openclaw
git clone https://github.com/MochenRay/xiaoka-health-agent.git workspace-xiaoka
```

仓库已包含 OpenClaw 所需的 `SOUL.md` 和 `IDENTITY.md`，无需额外适配。

### 2. 创建数据目录

```bash
mkdir -p ~/.openclaw/workspace-xiaoka/workspace/{logs,data,medical,reports,food-library}
printf '[]\n' > ~/.openclaw/workspace-xiaoka/workspace/food-library/my-foods.json
```

仓库标准路径约定：

- `config/profile.md`、`config/goals.md`
- `workspace/logs/YYYY-MM/DD.md`
- `workspace/data/YYYY-MM/DD.json`
- `workspace/medical/`
- `workspace/reports/`
- `workspace/food-library/my-foods.json`

如果你机器上已经有旧版本地任务在读写根目录 `logs/` 或 `data/`，先迁移到 `workspace/` 约定，再启用新任务。

### 3. 注册 Agent

```bash
# 查看当前 agent 数量（假设返回 N）
openclaw config get agents.list | python3 -c "import json,sys; print(len(json.load(sys.stdin)))"

# 注册（把 N 替换为实际数字）
openclaw config set "agents.list[N].id" "xiaoka"
openclaw config set "agents.list[N].workspace" "$HOME/.openclaw/workspace-xiaoka"
openclaw config set "agents.list[N].model" "bailian/qwen3.5-plus"
openclaw config set "agents.list[N].identity.name" "小卡"
openclaw config set "agents.list[N].identity.emoji" "🏋️"
```

### 4. 配置 Telegram（顺序敏感！）

```bash
openclaw config set "channels.telegram.accounts.xiaoka.enabled" true
openclaw config set "channels.telegram.accounts.xiaoka.botToken" "<你的 bot token>"
# ⚠️ 先设 allowFrom 再设 dmPolicy
openclaw config set "channels.telegram.accounts.xiaoka.allowFrom[0]" "<你的 Telegram user ID>"
openclaw config set "channels.telegram.accounts.xiaoka.dmPolicy" "allowlist"
openclaw config set "channels.telegram.accounts.xiaoka.streaming" "partial"
openclaw config set "channels.telegram.accounts.xiaoka.ackReaction" "🔥"
```

### 5. 路由绑定（最容易漏！）

```bash
openclaw agents bind --agent xiaoka --bind "telegram:xiaoka"
```

不执行这步，消息会 fallback 到 main agent。

### 6. 重启 Gateway

```bash
openclaw daemon restart
# 或手动重启 launchd 服务
```

### 7. 验证

```bash
# 确认健康
curl -s http://127.0.0.1:18789/health
# 应返回 {"ok":true,"status":"live"}

# 确认路由绑定
openclaw agents list --bindings | grep xiaoka
# 应看到 Routing rules: 1
```

然后在 Telegram 给你的 Bot 发"你好"，确认小卡自动进入 Profile 引导。

## Cron 任务（Phase 2 配置）

这些任务属于 **OpenClaw Cron**，不是系统 `crontab`。

| 任务 | 时间 | 说明 |
|------|------|------|
| 零点结算 | 00:00 | 读当天 Markdown 日志 → 写入 JSON |
| 结算校验 | 00:30 | 对比 JSON 和 Markdown 数据一致性 |
| 前日汇总 | 08:00 | 有记录才发 |
| 周报 | 周六 20:00 | 始终生成，标注覆盖率 |
| 月报 | 月末 20:00 | 同上 |

## 注意事项

- Agent 需要 workspace 目录的文件读写权限
- 仓库里的 Phase 1 标准路径以 `workspace/` 为准；历史本地部署可能仍残留旧路径
- 推荐使用支持多模态（图片输入）的模型
- 使用云端模型时，对话内容会发送给模型提供商
- 后续更新：在 Mac Mini 上 `cd workspace-xiaoka && git pull` 即可同步
