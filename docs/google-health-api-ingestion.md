# Google Health API 接入决策

> 状态：2026-05-28 CST 已完成人工 OAuth read smoke；仓库 importer、token refresh
> 和 OpenClaw runtime 自动同步尚未实现。

## 结论

Google Health API 取代 Apple Watch / Apple Health 截图，成为运动、步数、睡眠设备数据的第一接入路径。

截图识别不再作为首选方案，只保留为 fallback：

- 用户临时发来单张截图时，仍可按现有 A4/A6 规则手动记录。
- 食物照片、营养标签和体检单图片不受影响，仍需要 Vision/OCR。
- `fixtures/synthetic/phase2c/` 继续证明 legacy screenshot mapping，不代表新主路径。

## 已验证事实

2026-05-28 通过 Google OAuth Playground 手动授权后，使用只读 scope 实测：

- `identity` 返回 HTTP 200。
- `steps` data points 返回 HTTP 200。
- `sleep` data points 返回 HTTP 200。
- `exercise` data points 返回 HTTP 200。
- `steps` daily rollup 返回非空日级数据。
- 返回来源中出现 `HEALTH_KIT` 与 Apple 设备/应用来源，说明 iOS Apple Health 经 Google Health API 可读。

本次验证没有把 OAuth token、refresh token、账号 email、health user id、原始响应或真实健康明细写入仓库。

## Scope 和接口边界

最小只读 scope：

- `https://www.googleapis.com/auth/googlehealth.activity_and_fitness.readonly`
- `https://www.googleapis.com/auth/googlehealth.sleep.readonly`

首批只接以下 data types：

- `steps`
- `sleep`
- `exercise`

请求形状：

- list data points 用 `filter` 限定日期窗口，例如 `steps.interval.civil_start_time`、`sleep.interval.civil_end_time`。
- daily rollup 不接受 `startTime` / `endTime` 顶层字段；应使用 `range.start.date`、`range.end.date` 与 `windowSizeDays`。
- API key 不可用，必须走 Google OAuth。

## 替换映射

| 旧截图方案 | 新主路径 |
|------------|----------|
| Apple Health 活动摘要截图识别 steps | Google Health API `steps` + `dailyRollUp` |
| Apple Health / Apple Watch 睡眠截图识别睡眠时长 | Google Health API `sleep` data points |
| Apple Watch workout 截图识别运动记录 | Google Health API `exercise` data points |
| OCR 置信度与用户确认 | OAuth 授权、API 状态、字段完整性和幂等导入检查 |
| 真实 OCR runtime smoke | Google Health API read/import smoke |

## 写入 Xiaoka 的原则

导入器应优先把规范化后的设备记录写入 `workspace/logs/YYYY-MM/DD.md`，再让既有零点结算生成 `workspace/data/YYYY-MM/DD.json`。只有历史回填或测试需要时，才允许在备份后直接生成 daily JSON。

建议 source 取值：

- `google_health_api`
- `google_health_api_healthkit`

可以记录的非敏感来源字段：

- `source_platform`: 例如 `HEALTH_KIT`
- `source_application`: 例如 Apple Health 或第三方睡眠应用 package name
- `source_device_form_factor`: 例如 `PHONE`

不要写入 daily JSON：

- OAuth access token / refresh token
- client secret
- Google account email
- `healthUserId` / `legacyUserId`
- 原始完整 API response

## 安全边界

- token、client secret、OAuth Playground 导出、API response cache 只能放在本机被 ignore 的路径，或系统 keychain / OpenClaw 本地 secret store。
- 日志中必须 redact `Authorization`、`access_token`、`refresh_token`、`client_secret`、`healthUserId`、`legacyUserId`。
- GitHub 只能提交文档、synthetic fixture、脱敏 schema 和导入代码；不能提交真实健康数据或 token cache。
- `workspace/*`、`.env*`、`*token*.json`、`client_secret*.json`、`*credentials*.json`、`google-health-cache/` 必须保持 ignored。

## 后续实现切片

1. 本地 OAuth 配置：使用用户自己的 OAuth client，token cache 放 ignored local path。
2. 只读 import script：按日期窗口拉取 `steps`、`sleep`、`exercise`，输出规范化 records。
3. 幂等写入：按 date + data type + source + interval 去重，避免重复追加。
4. runtime smoke：用户确认测试窗口后，用真实账号拉取短窗口数据，写入 ignored `workspace/`，不触发 Telegram。
5. 报告验证：复用既有周报/月报、E1/S1/C8 数据门槛，不因为接入 API 就提高医学断言强度。
