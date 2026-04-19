---
description: Archive a decision from the current conversation into docs/decisions/ as a numbered ADR file, and update the index. Use this skill when the user explicitly asks to save, archive, or document a decision (e.g. "归档", "存成 ADR", "/decide").
disable-model-invocation: true
---

# decide — 把本次会话中的决策归档为 ADR

## 前置检查

1. 若项目根不存在 `docs/decisions/INDEX.md`：提示用户先运行 `/adr-governance:init-adr` 初始化，然后终止本次执行。
2. 若存在，读取它确定下一个编号（表格中最大编号 +1，4 位补零：`0001`、`0002`…）。

## 字段提炼

从当前对话上下文中提炼：
- **标题**：如用户给了 `$ARGUMENTS` 优先用作线索；否则自行拟定（≤12 字）。
- **背景**：为什么要做这个决策（痛点 / 约束 / 契机）。
- **决策**：最终采纳的方案——一句话结论 + 细节展开。
- **权衡与备选**：至少列出 1 个被放弃的备选及放弃原因。
- **后果**：正向 / 负向 / 待跟进。
- **关联**：相关 Spec、Plan、前置 ADR（如有）。

**信息不足时的处理**：任何字段在对话中找不到依据，**先停下来列出缺口让用户补全**，不要编造。

## 写文件

参考 `${CLAUDE_PLUGIN_ROOT}/templates/TEMPLATE.md` 的结构，在 `docs/decisions/NNNN-kebab-slug.md` 生成新 ADR：

- slug 用小写英文 + 连字符，便于检索。
- Frontmatter：
  - `编号` = NNNN
  - `日期` = 今天
  - `决策人` = `git config user.name` 的结果
  - `状态` = `Accepted`（除非用户明确说"草稿"或"待定"）
  - `标签` = 从内容提炼的逗号分隔关键词

## 更新索引

向 `docs/decisions/INDEX.md`：
1. 表格追加一行：编号 / 状态 / 日期 / 标题 / 关键词。
2. 在对应领域速查小节补一条 `- [NNNN](./NNNN-slug.md) — 标题`。

## 输出回执

给用户一段简洁反馈：
- 新文件路径
- 标题 + 一句话摘要
- 是否需要为它建关联 Spec / Plan（仅建议，不自动建）

## 硬约束

- 内容**只能**来自用户已确认的信息，不要凭空补。
- ADR 只写"为什么"，实施细节归 Spec（别越界）。
- 发现与已有 ADR 冲突时**先指出冲突**并询问是否 Supersede，不要默默覆盖。
- 写完**不**自动 commit，把提交时机交给用户。
