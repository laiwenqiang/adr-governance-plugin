---

## 决策记录制度（ADR）

### 💡 动机
Vibe coding 中重要决策易散落在对话里，导致同一问题反复踩坑。所有**选型 / 约束 / 架构 / 流程规则**类决策一律沉淀为 ADR，存放在 `docs/decisions/`。

### 🔁 自动提醒（双保险，非人工判断）
1. **Stop hook**（`adr-governance` plugin）在每轮响应结束时扫描最近 assistant 文本，命中决策关键词且本会话 `INDEX.md` 未更新则 `decision: block`，强制助手向用户确认归档。
2. **AI 自检**：助手在回答中识别到以下信号时必须主动提示归档——
   - 技术选型 / 替代方案 / 放弃某方案
   - 新的架构约束或不变量
   - 流程规则 / 协作规范
   - 明确的"不用 X，用 Y"判断
3. 关键词匹配覆盖有限，AI 自检是第二道防线；hook 是兜底。

### 🛠 操作入口
- `/adr-governance:decide [主题]`：把当前会话中的决策归档为一条 ADR。
- `/adr-governance:init-adr`：初始化（本项目已执行过）。
- 手动：复制 `docs/decisions/TEMPLATE.md`，编号递增，同步 `INDEX.md`。

### 📐 使用约束
- **会话开始**如涉及架构 / 选型 / 规则话题，**先读 `docs/decisions/INDEX.md`** 再作答，避免违背既有决策。
- 已 `Accepted` 的决策**不得就地修改**——用新 ADR `Supersede` 或改状态为 `Deprecated`。
- ADR 只写"为什么"，实施细节归 Spec，步骤归 Plan。
- 元 ADR：见 `docs/decisions/0001-adr-process.md`。
