# Public Release Checklist

本 checklist 用于公开 README、GitHub release、模板仓库或对外介绍发布前的最后核对。
目标是避免把个人运行态、未完成 runtime smoke 或固定模型推荐误写成公开能力。

## 1. Truthful capability claims

- 只能把以下内容写成已可用：本地文件驱动 Agent、核心记录工作流、稳定路径合同、
  OpenClaw 五条自动化任务、Google Health API read smoke、Phase 2B/2C/3A synthetic fixtures 与 validators。
- 必须明确区分 `runtime enabled`、`runtime smoke passed`、`static fixture
  validation` 和 `pending`。
- Google Health API 只能声称 read smoke 已通过；importer、token refresh 和 OpenClaw runtime
  同步未完成前，不得声称自动同步已闭环。
- Phase 2C 截图能力只能声称 fallback synthetic mapping 已验证；真实 screenshot/OCR
  runtime smoke 未完成前，不得声称真实截图识别已闭环。
- C8 只能声称 static contract 与 synthetic validator 已完成；C8 OpenClaw
  runtime smoke 未完成前，不得声称真实周报/月报已 runtime-proven。
- 不得声称 Google Health API 自动同步、Apple Health 文件式历史同步、Health Auto Export、Apple Health XML parser、
  Withings/体脂秤导入、Telegram 快捷操作或静态 dashboard 已完成。
- 不得声明固定模型推荐。只能声明 Xiaoka 支持多模型部署，且截图、照片、营养标签和
  体检单图片工作流必须使用支持图片输入、图片识别或 OCR 的多模态模型。
- 不得提供医疗诊断、处方、药物剂量调整或急症处理承诺。

## 2. Secret scan

在发布前运行至少一种 secret scan。若安装了 `gitleaks`，优先运行：

```bash
gitleaks detect --source . --no-git --redact
```

没有 `gitleaks` 时，至少运行 tracked-file pattern scan：

```bash
git grep -nE '(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|ya29\.[A-Za-z0-9._-]+|1//[A-Za-z0-9._-]+|GOCSPX-[A-Za-z0-9_-]+)' -- .
```

发布前确认：

- `.env.example` 只有占位符，不含真实 token、API key、client secret、chat id 或 webhook。
- `.env`、`.env.*`、`*.token`、`*token*.json`、`client_secret*.json`、`*credentials*.json`、个人 `config/profile.md`、`config/goals.md` 和
  `workspace/*` 没有进入 commit。
- 搜索结果若命中文档里的示例 pattern，必须人工确认不是实际 secret。

## 3. Ignored runtime files

确认运行态和私人健康数据仍被忽略：

```bash
git check-ignore -v \
  .env \
  .env.local \
  example.token \
  google-health-token.json \
  client_secret_google_health.json \
  google-health-cache/token.json \
  tokens/google-health.json \
  config/profile.md \
  config/goals.md \
  workspace/logs/example.md \
  workspace/data/example.json \
  workspace/medical/example.md \
  workspace/reports/example.md \
  workspace/food-library/my-foods.json
```

旧版根目录 runtime path 也必须保持废弃或兼容语境，不得重新作为标准路径发布：

```bash
# 旧版根目录 runtime path，仅用于确认废弃/兼容 ignore 规则
git check-ignore -v \
  logs/example.md \
  data/example.json \
  medical/example.md \
  reports/example.md \
  food-library/my-foods.json
```

允许 tracked 的例外是 `workspace/README.md` 和 synthetic fixture 下的非私人样例。

## 4. Markdown links and repository contract

运行仓库合同 validator。它会检查 tracked JSON、Markdown 本地链接、知识库 metadata、
`SKILL.md` 行数和旧 runtime path 语境。

```bash
python3 scripts/validate_repository_contract.py
python3 scripts/validate_settlement_prompt_contract.py
python3 scripts/validate_daily_json_schema.py
python3 scripts/validate_report_contracts.py
```

如发布页新增外部链接，人工打开关键外链；当前 validator 只检查本地 Markdown 链接。

## 5. Fixture validators

每次公开发布前运行全部 fixture validators：

```bash
python3 scripts/validate_phase2b_fixtures.py
python3 scripts/validate_phase2c_screenshot_fixtures.py
python3 scripts/validate_phase3a_c8_fixtures.py
```

通过这些 validators 只证明 synthetic fixtures 和静态合同一致，不证明真实 OCR、
OpenClaw runtime 或个人健康数据已闭环。

## 6. Whitespace and diff hygiene

发布前运行：

```bash
git diff --check
git diff --cached --check
```

确认没有 trailing whitespace、冲突标记或缩进噪音。

## 7. Runtime smoke gates

只有在对应 smoke 完成并登记后，才能升级公开声明：

- Google Health API importer/runtime smoke 通过后，才可声称 Apple Health / HealthKit
  设备数据可自动同步。
- 真实截图/OCR runtime smoke 通过后，才可声称真实 Apple Watch / Apple Health
  截图识别闭环。
- C8 OpenClaw runtime smoke 通过后，才可声称 C8 周报/月报 runtime-proven。
- M1/E1/S1 repo 层合同和模板只能声称为 static fixture validation；OpenClaw
  runtime 自动报告验证通过后，才可声称深度药物、运动、睡眠分析已进入自动报告。

## 8. Final pre-release review

- README、`docs/`、`deploy/`、`SKILL.md` 的路径合同一致。
- `CHANGELOG.md` 中 pending runtime smoke 项仍准确。
- [privacy-and-medical-boundaries.md](privacy-and-medical-boundaries.md) 已链接并与
  README 隐私段落一致。
- `git status --short` 只包含本次发布需要的 tracked 文件变更。
