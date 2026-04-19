# adr-governance

> **自动提醒** + 规范化的架构决策记录（ADR）流程，打包为 Claude Code Plugin。

## 解决什么问题

Vibe coding 中重要决策容易散落在对话里：
- 选型理由说过就忘，重复踩坑；
- 约束和不变量没有沉淀，新成员无从参考；
- "为什么当初这样做"问十次解释十次。

本 plugin 通过 **Stop hook 自动识别 + skill 规范化归档** 把决策变成可检索的资产。

## 功能

| 组件 | 类型 | 作用 |
|------|------|------|
| `decision-detect.py` | Stop hook | 扫描每轮对话，命中决策关键词且本会话未归档则拦截并提示 |
| `session-start.py` | SessionStart hook | 建立可靠的 session 起点，保证去抖判断准确 |
| `/adr-governance:decide` | Skill | 从当前对话提炼字段，归档为 `docs/decisions/NNNN-*.md` 并更新索引 |
| `/adr-governance:init-adr` | Skill | 一键初始化项目：复制模板、追加 `CLAUDE.md` 章节、更新 `.gitignore` |
| `writing-adr` | Skill（模型自动触发） | 指导如何写高质量 ADR——只写 Why、必有权衡、可证伪 |

**自检开关**：hook 只在项目根有 `docs/decisions/` 目录时才启用；未初始化的项目完全静默，零噪音。

## 安装

```shell
# 1. 注册 marketplace（单插件仓库，既是 marketplace 又是 plugin）
/plugin marketplace add laiwenqiang/adr-governance-plugin

# 2. 安装 plugin
/plugin install adr-governance@adr-tools

# 3. 重启会话后生效
```

或用本地路径测试：

```shell
claude --plugin-dir /path/to/adr-governance-plugin
```

## 首次使用

```shell
# 在目标项目里：
/adr-governance:init-adr

# 回答中会列出新建的文件。下次对话 hook 自动生效。
```

然后正常工作。当 Claude 说"我决定采用 X 而不是 Y"之类的话时，Stop hook 会提醒：
> 【决策归档提醒】本轮对话命中决策类关键词…
> 同意归档就回"存一下"或运行 `/adr-governance:decide`。

## 更新

```shell
/plugin marketplace update adr-tools
/plugin update adr-governance
```

## 卸载

```shell
/plugin uninstall adr-governance
```

项目里已有的 `docs/decisions/` 内容保留，`CLAUDE.md` 的章节需要手动移除（因为它已经是项目规范的一部分）。

## 关键词（触发 hook 的信号）

中文：决定采用 / 决策 / 选型 / 技术选型 / 禁止使用 / 严禁 / 不允许 / 约束 / 底线 / 权衡 / 取舍 / 替代方案 / 代替 / 替换 / 架构决策 / 规范约定 / 统一规则

英文：decide / decision / tradeoff / adopt / must not / architecture decision / rejected / supersede

在 `hooks/decision-detect.py` 的 `KEYWORD_PATTERN` 里可调整。

## FAQ

**Q: hook 为什么有时不触发？**
A: 项目根必须有 `docs/decisions/` 目录；没有就静默退出。先跑 `/adr-governance:init-adr`。

**Q: 误报太多怎么办？**
A: 每个会话只提醒一次（`decision-notified-<session>` marker 去抖）。如果仍觉得噪音大，可以 fork 仓库收紧 `KEYWORD_PATTERN`。

**Q: 已经归档过，hook 还提醒？**
A: SessionStart hook 会建立基准时间，`INDEX.md` 在本会话内被更新过就不会再提醒。如果没触发 SessionStart，重启一次会话即可。

**Q: 支持 Windows 吗？**
A: 依赖 `python3` 在 `$PATH`。macOS / Linux 开箱即用；Windows 需要确保 `python3.exe` 可直接调用（或 fork 改为 `py -3`）。

## 贡献

欢迎 PR：
- 关键词误报/漏报的用例
- 新增 skill（如 `/adr-governance:review` 批量审阅 ADR）
- i18n（英文项目的 CLAUDE.md 模板）

## License

MIT — 见 [LICENSE](./LICENSE)。
