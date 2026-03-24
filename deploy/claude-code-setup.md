# Claude Code 使用指南

> 详细步骤将在 Phase 4 补充。以下为概要。

## 使用方式

1. Clone 本仓库
2. 在 Claude Code 中将本仓库目录作为工作目录
3. SKILL.md 和 agent.md 会作为项目上下文自动加载
4. references/ 目录作为知识库参考
5. 首次对话发送任意消息，小卡会自动检测 profile.md 是否存在并引导初始化

## 推荐配置

在 `.claude/CLAUDE.md` 或项目级配置中引用：

```markdown
请加载以下文件作为你的行为规范：
- agent.md（人格设定）
- SKILL.md（技能路由和 workflow）
```

## 注意事项

- Claude Code 中 Cron 任务需要手动触发或通过外部调度
- 周报/月报可通过对话触发："生成本周报告"
