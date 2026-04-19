---
description: Initialize the ADR (Architecture Decision Records) governance system in the current project by copying template files into docs/decisions/ and appending a governance section to CLAUDE.md. Use when the user explicitly asks to set up, bootstrap, or initialize ADR / decision records in a new project.
disable-model-invocation: true
---

# init-adr — 在当前项目初始化 ADR 制度

## 前置检查

1. 读 `docs/decisions/INDEX.md`：若已存在，告知"已初始化，无需重复"并终止（不覆盖已有文件）。
2. 从 git config 获取用户名：`git config user.name`（兜底用 "unknown"）。
3. 记录今天的日期（YYYY-MM-DD）。

## 复制模板

从 `${CLAUDE_PLUGIN_ROOT}/templates/` 读取并写入目标位置：

| 源 | 目标 |
|----|------|
| `templates/README.md` | `docs/decisions/README.md` |
| `templates/INDEX.md` | `docs/decisions/INDEX.md` |
| `templates/TEMPLATE.md` | `docs/decisions/TEMPLATE.md` |
| `templates/0001-adr-process.md` | `docs/decisions/0001-adr-process.md` |

对 `0001-adr-process.md` 和 `INDEX.md` 做占位符替换：
- `{{DATE}}` → 今天的日期
- `{{AUTHOR}}` → git user.name
- `{{PROJECT}}` → 项目根目录名（`basename $CLAUDE_PROJECT_DIR`）

## 更新 CLAUDE.md

读 `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE-section.md` 的内容：

- 若项目根有 `CLAUDE.md`：检查是否已包含"决策记录制度"章节；没有就追加到末尾。
- 若没有 `CLAUDE.md`：创建一个，内容就是该章节。

## 更新 .gitignore

在项目 `.gitignore` 追加一行 `/.claude/.runtime/`（若已存在则跳过；若无 `.gitignore` 则创建）。

## 输出回执

告诉用户：
1. 已创建 / 修改的文件清单。
2. 提示："SessionStart / Stop hook 会在下次会话自动生效；本会话也可用 `/adr-governance:decide` 手动归档。"
3. 如果检测到未 commit 的文件，建议用户 commit（但**不**自动 commit）。

## 硬约束

- **不覆盖**任何已存在的 `docs/decisions/*.md` 文件。
- CLAUDE.md 追加时**不删除**任何已有内容。
- **不**自动 commit。
