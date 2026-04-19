---
description: Guidance for writing high-quality Architecture Decision Records (ADRs). Use this skill when drafting or reviewing content in docs/decisions/, especially when articulating tradeoffs, selecting between alternatives, establishing architectural constraints, or when the user is crafting a decision record.
---

# Writing ADRs — 写作指南

## 核心原则

1. **只写 Why，不写 How**：ADR 是"为什么这样做"，实施细节归 Spec。如果一段话换成"在类 X 加方法 Y"更合适，那它不属于 ADR。
2. **权衡必须有**：至少列一个被放弃的备选方案及放弃理由；无权衡的决策不值得归档。
3. **可证伪性**：写后果时具体到可观察的信号（"P99 延迟从 200ms 降到 50ms"，而不是"性能更好"）。
4. **锁定时间**：已 `Accepted` 的决策**不得就地修改**；翻盘必须新建 ADR 并 Supersede。

## 字段写作要点

### 背景
- 痛点用**现象**描述（错误率、延迟、开发体验问题），不用形容词（"慢"、"乱"）。
- 约束明列（技术栈、合规、人力、时间窗口）。
- 交代"为什么现在要决定"——时机比道理重要。

### 决策
- **第一句必须是结论式陈述**（"采用 X"、"禁止 Y"），不要铺垫。
- 细节分层：关键取舍 → 实现参数。
- 参数给默认值，但明示可调（"默认 3 次，由配置驱动"）。

### 权衡与备选
- 表格形式：| 方案 | 优势 | 放弃原因 |
- 被放弃方案**至少一个**要是"看起来合理但实际不行"的——展示真的思考过。
- 写放弃原因时给**硬约束**（"不兼容 WebSphere Parent-Last"）或**可量化代价**（"引入 200MB 依赖"），不要"不合适"。

### 后果
- 分三档：**正向** / **负向** / **待跟进**。
- 每条给具体指标、事件、信号，不写"更稳定""更好维护"。
- 待跟进是给未来自己的提醒："2 周后复盘误报率"。

### 关联
- 向前：引用前置 ADR（`Supersedes:` / 依赖）。
- 向下：关联的 Spec / Plan 路径。
- 横向：相关议题的 ADR 编号。

## 何时新增 vs 修改

| 场景 | 操作 |
|------|------|
| 新议题 | 新增一条 ADR |
| 翻盘旧决策 | 新 ADR（Accepted）+ 旧 ADR 状态改 `Superseded by NNNN` |
| 小幅修订（打字错误、链接失效） | 直接改，不需要新 ADR |
| 澄清既有决策 | 在原 ADR 末尾加 "Clarifications" 节，不动决策本身 |
| 决策不再适用但没人取代 | 改状态为 `Deprecated`，保留历史 |

## 禁忌清单

- ❌ 在已 Accepted 的 ADR 里修改"决策"/"背景"/"权衡"字段。
- ❌ 写成"我们应该……"的倡议书；ADR 是**已决事实**。
- ❌ 把实施步骤写进 ADR（归 Plan）。
- ❌ 无权衡、无备选——这样的决策不值得归档。
- ❌ 用"可能"/"也许"/"大概"；ADR 是承诺，不是探讨。
