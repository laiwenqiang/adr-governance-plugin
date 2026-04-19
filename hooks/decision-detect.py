#!/usr/bin/env python3
"""
Claude Code Stop hook (adr-governance plugin): 自动提醒决策归档。

读取当前会话 transcript 最近若干条 assistant 文本，若命中"决策类"关键词
且本会话尚未更新 <project>/docs/decisions/INDEX.md，则通过 `decision: block`
阻止停止，强制 Claude 向用户确认是否归档为 ADR。

自检开关：仅当用户项目根有 `docs/decisions/` 目录时才启用（未初始化的项目
不会被打扰）。

状态文件放在 ${CLAUDE_PLUGIN_DATA}/.runtime/，跨 plugin 更新持久化。
"""
from __future__ import annotations

import json
import os
import re
import sys
from typing import Optional


KEYWORD_PATTERN = re.compile(
    r'('
    # 中文强信号
    r'决定采用|决定使用|决定不用|决策|选型|技术选型|采用方案|'
    r'禁止使用|严禁|不允许|约束(?!条件)|底线|不变量|'
    r'权衡|取舍|替代方案|代替方案|用\s*\S+\s*代替|用\s*\S+\s*替换|'
    r'架构决策|设计决策|规范约定|统一规则|定一条规则|'
    # 英文强信号
    r'\bdecide\b|\bdecision\b|\btradeoff\b|\badopt(?:ed)?\b|'
    r'\bmust not\b|\bshould not\b|\barchitecture decision\b|'
    r'\breject(?:ed)?\b|\bsupersede'
    r')',
    re.IGNORECASE,
)

MAX_RECENT_ASSISTANT_MESSAGES = 3


def project_dir() -> str:
    return os.environ.get("CLAUDE_PROJECT_DIR", "")


def docs_decisions_exists() -> bool:
    """自检开关：未初始化的项目直接静默退出。"""
    proj = project_dir()
    if not proj:
        return False
    return os.path.isdir(os.path.join(proj, "docs", "decisions"))


def runtime_dir() -> Optional[str]:
    base = os.environ.get("CLAUDE_PLUGIN_DATA")
    if base:
        path = os.path.join(base, ".runtime")
    else:
        proj = project_dir()
        if not proj:
            return None
        path = os.path.join(proj, ".claude", ".runtime")
    try:
        os.makedirs(path, exist_ok=True)
        return path
    except Exception:
        return None


def read_input() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def extract_recent_assistant_text(transcript_path: str) -> str:
    if not transcript_path or not os.path.isfile(transcript_path):
        return ""
    messages: list[str] = []
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get("type") != "assistant":
                    continue
                content = obj.get("message", {}).get("content", [])
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "text":
                        messages.append(c.get("text", ""))
    except Exception:
        return ""
    return "\n".join(messages[-MAX_RECENT_ASSISTANT_MESSAGES:])


def session_start_time(run_dir: str, session_id: str) -> Optional[float]:
    marker = os.path.join(run_dir, f"session-start-{session_id}")
    if not os.path.isfile(marker):
        return None
    try:
        return os.path.getmtime(marker)
    except Exception:
        return None


def index_updated_in_session(run_dir: str, session_id: str) -> bool:
    start = session_start_time(run_dir, session_id)
    if start is None:
        return False
    index = os.path.join(project_dir(), "docs", "decisions", "INDEX.md")
    if not os.path.isfile(index):
        return False
    try:
        return os.path.getmtime(index) >= start
    except Exception:
        return False


def emit_block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))


def main() -> int:
    data = read_input()

    if data.get("stop_hook_active"):
        return 0

    # 自检：项目未启用 ADR 制度则静默
    if not docs_decisions_exists():
        return 0

    session_id = data.get("session_id", "")
    transcript = data.get("transcript_path", "")
    if not session_id:
        return 0

    run_dir = runtime_dir()
    if not run_dir:
        return 0

    notified = os.path.join(run_dir, f"decision-notified-{session_id}")
    if os.path.exists(notified):
        return 0

    text = extract_recent_assistant_text(transcript)
    if not text or not KEYWORD_PATTERN.search(text):
        return 0

    if index_updated_in_session(run_dir, session_id):
        return 0

    try:
        open(notified, "w").close()
    except Exception:
        pass

    emit_block(
        "【决策归档提醒】本轮对话命中决策类关键词，但 docs/decisions/INDEX.md "
        "本会话内未更新。在响应用户前请执行以下动作：\n"
        "1) 判断本轮是否确实包含架构/选型/约束/流程类决策。\n"
        "2) 若是：主动询问用户『是否归档为 ADR？』——同意则立即运行 "
        "/adr-governance:decide 流程。\n"
        "3) 若否（仅澄清、讨论、复述既有决策）：向用户简短说明『本轮无需归档』。\n"
        "本提醒同一会话仅触发一次，不会重复打扰。"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
