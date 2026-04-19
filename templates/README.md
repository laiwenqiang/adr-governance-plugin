# 架构决策记录（ADR）

本目录用于沉淀**{{PROJECT}}** 项目中的重要决策，避免同一问题反复被推翻或重新论证。

## 何时写一条 ADR（由系统自动提醒）

**识别由 Stop hook + AI 双保险完成**，你一般不需要主动判断。命中以下任一信号时会被自动提示：

1. **选型/替代**：多方案取舍。
2. **约束/底线**：确立一条"不能越过的线"。
3. **架构形状**：影响模块边界、继承体系、调用链。
4. **流程/规则**：团队协作或开发规范。

> 提醒触发后你可以选择归档或拒绝；同一会话只提示一次，避免噪音。

## 如何写

- **推荐**：在 Claude Code 中输入 `/adr-governance:decide [主题]`，助手会从上下文提炼并归档。
- **手动**：复制 [`TEMPLATE.md`](./TEMPLATE.md)，新建 `NNNN-slug.md`，编号递增 4 位数字。
- 每新增一条，**必须同步更新** [`INDEX.md`](./INDEX.md)。

## 文件命名

```
NNNN-kebab-case-title.md
例：0001-adr-process.md
```

## 状态机

| 状态 | 含义 |
|------|------|
| `Proposed` | 草稿，待讨论 |
| `Accepted` | 已生效 |
| `Deprecated` | 已废弃但保留历史 |
| `Superseded by NNNN` | 被新决策取代 |

已 `Accepted` 的决策**不得就地修改**——要么新增一条 `Supersede`，要么改状态为 `Deprecated`。

## 与其他产物的边界

| 产物 | 位置 | 内容 |
|------|------|------|
| **ADR**（本目录） | `docs/decisions/` | "为什么这样做" |
| **Spec** | `docs/specs/` 或类似 | "做成什么样"（设计） |
| **Plan** | `docs/plans/` 或类似 | "怎么一步步做"（步骤） |

ADR 引用 Spec，Spec 遵循 ADR。

## 自动化机制

本项目通过 [`adr-governance`](https://github.com/laiwenqiang/adr-governance-plugin) Claude Code plugin 实现：
- **Stop hook** 扫描决策关键词，未归档则弹提示
- **SessionStart hook** 建立 session 基准时间，保证去抖可靠
- **`/adr-governance:decide`** 执行归档
- **`/adr-governance:init-adr`** 初始化项目
- **`writing-adr`** skill 指导写作

关闭自动提醒：`/plugin disable adr-governance`
