# Changelog

本项目遵循 [Semantic Versioning](https://semver.org/) 和 [Keep a Changelog](https://keepachangelog.com/) 约定。

## [0.1.0] — 2026-04-19

### 新增
- **Stop hook** `decision-detect.py`：扫描对话中的决策关键词，未归档则返回 `decision: block` 强制提示。
- **SessionStart hook** `session-start.py`：建立会话基准时间，刷新去抖 marker，保证"本会话已归档"检测可靠。
- **Skill `decide`**：从对话上下文提炼字段，归档为 `docs/decisions/NNNN-*.md` 并更新 `INDEX.md`。
- **Skill `init-adr`**：复制模板到项目 `docs/decisions/`、追加 `CLAUDE.md` 决策章节、更新 `.gitignore`。
- **Skill `writing-adr`**（模型自动触发）：写作规范指南——只写 Why、必有权衡、可证伪。
- **Templates**：`README.md` / `INDEX.md` / `TEMPLATE.md` / `0001-adr-process.md` / `CLAUDE-section.md`，支持 `{{DATE}}` / `{{AUTHOR}}` / `{{PROJECT}}` 占位符。
- **自检开关**：仅当项目根存在 `docs/decisions/` 时启用 hook，未初始化的项目完全静默。
- **状态文件**：存放在 `${CLAUDE_PLUGIN_DATA}/.runtime/`，跨 plugin 更新持久化；不污染用户项目。

### 已知问题
- 触发 hook 的关键词列表基于中/英强信号，小众表达可能漏报；AI 自检作为第二道防线。
- Windows 需确保 `python3` 在 `$PATH`。
