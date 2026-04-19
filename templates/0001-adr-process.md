---
编号: 0001
标题: 建立 ADR 决策记录制度
状态: Accepted
日期: {{DATE}}
决策人: {{AUTHOR}}
标签: process, governance, hook
---

## 背景

Vibe coding 模式下，涉及架构选型、约束、协作规则的重要决策往往散落在实时对话中，缺少统一的归档、汇总与检索机制，导致：

- 同一议题被反复推翻或重新论证。
- 新人或未来的自己无法快速理解"为什么当初这样做"。
- 与 `CLAUDE.md` 的静态约束相比，临时决策缺少沉淀入口。
- 重要功能反复出现问题，根因是决策未被记住。

## 决策

在 **{{PROJECT}}** 项目启用 `adr-governance` plugin 提供的轻量 ADR 制度，由**系统自动提醒**触发归档：

1. **目录**：`docs/decisions/`
2. **文件命名**：`NNNN-kebab-slug.md`（4 位递增编号）
3. **索引**：`INDEX.md`（一行一条摘要，会话启动时浏览）
4. **模板**：`TEMPLATE.md`
5. **自动提醒**：Stop hook + AI 自检双保险——命中决策关键词且本会话未归档时强制提示。
6. **操作入口**：`/adr-governance:decide [主题]`。
7. **去抖策略**：同一会话只提示一次（`${CLAUDE_PLUGIN_DATA}/.runtime/decision-notified-<session>` 标记）。

## 权衡与备选

| 方案 | 优势 | 放弃原因 |
|------|------|----------|
| **ADR + 自动 hook**（采纳） | 结构化、可检索、自动提醒，降低遗忘率 | — |
| 只扩展 `tasks/lessons.md` | 轻量、零成本 | Lessons 是助手协作纠偏，与项目决策语义不同，混用会稀释两者 |
| 外部工具（Notion / Linear） | 跨项目统一 | 脱离代码仓易失同步；受环境限制 |
| 纯手动 `/decide` 触发 | 最简单 | 用户易忘，无法解决"反复踩坑"的根因 |
| 让 AI 自行记忆（memory 系统） | 无需文件 | 不在代码仓中，团队无法共享、不可 review |

## 后果

**正向**
- 决策可追溯、可 diff、可 code review。
- Hook 主动拦截，显著降低遗忘率。
- 与 Spec/Plan 形成分工明确的知识体系。
- 新会话启动读 `INDEX.md` 即可对齐历史决策。

**负向 / 风险**
- Hook 可能误报（已通过关键词收紧 + 会话级去抖缓解）。
- 需要团队养成"接受提醒即归档"的习惯。
- 关键词匹配覆盖有限，AI 自检是第二道防线。

**需要后续跟进**
- 观察 2 周后统计误报率与漏报率，调整关键词。
- 如 ADR 数量超过 30 条，考虑按领域拆分子目录。

## 关联

- `CLAUDE.md` §决策记录制度章节
- `docs/decisions/README.md` 使用指南
- [`adr-governance` plugin](https://github.com/laiwenqiang/adr-governance-plugin) 自动化实现
