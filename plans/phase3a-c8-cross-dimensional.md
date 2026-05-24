# Phase 3A C8 跨维度洞察 Phase Plan

> 最近确认：2026-05-24

## 目标

将 C8 从路线图占位推进为一等 workflow，并接入周报/月报的“跨维度观察”章节，让小卡在数据足够时给出有证据的健康教练式观察，在数据不足时明确拒绝趋势或关联判断。

## 垂直切片

1. **C8 workflow 合同**
   - 定义触发语义、读取范围、最小样本门槛、输出形状。
   - 只使用现有 daily JSON、profile/goals 与可选体检资料。
   - 不新增 Apple Health parser、历史批量导入或新 staging schema。

2. **报告接入**
   - 周报/月报继续写入既有报告路径。
   - “跨维度观察”章节必须引用样本量和具体指标。
   - 不足 3 个有效日或不足 3 个配对日时，固定写“数据不足，暂不做关联判断。”

3. **Synthetic 验证**
   - 新增不含个人健康数据的 C8 fixtures。
   - 覆盖 sufficient 与 insufficient 两类分支。
   - 同时覆盖周报与月报粒度。

4. **项目状态同步**
   - 路线图、README、脚本说明与共享层状态统一口径。
   - 明确 C8 的本轮完成范围是静态合同与 synthetic report contract，不声明 OpenClaw runtime 已重新验证。

## 耐久决策

- C8 输出是“观察”，不是因果结论、诊断或处方。
- 跨维度判断必须带样本量，例如有效天数、配对日数量、覆盖率。
- 周报优先连接饮食、运动/活动、睡眠、体重；月报可提及补剂/体检，但只有存在明确来源时才写。
- 缺失字段不补猜；`null` 或缺省代表未知，不等于 `0`。
- C8 不绕过截图先行路径：Apple Watch / Apple Health 截图仍先进入 Markdown，再由现有结算进入 daily JSON。

## 验收标准

- 有一等 `C8 跨维度关联分析` workflow。
- 周报/月报模板与自动化 prompt 明确 C8 的数据门槛和输出边界。
- C8 synthetic fixtures 同时证明：
  - 数据足够时，报告可产出一条可追溯、低断言强度的跨维度观察。
  - 数据不足时，报告固定拒绝关联判断。
- Validator 能阻止 fixture 缺 marker、覆盖率错误、低样本硬编、强因果措辞和未出现维度的过度声明。
- 合并前本机通过现有 Phase 2B/2C validator 和新增 C8 validator；合并推送并同步 Mac Mini 后，再在 Mac Mini 跑同一组 validator 作为 finish gate。

## 明确不做

- 不实现真实报告生成器。
- 不改 OpenClaw cron runtime payload。
- 不做真实截图/OCR runtime smoke。
- 不实现 Apple Health XML、Health Auto Export、CSV/JSON 批量导入 parser。
- 不提交任何个人健康数据 fixture。
