#!/usr/bin/env python3
"""
Claude Code SessionStart hook (adr-governance plugin):
为 decision-detect.py 提供可靠的 session 起点。

- touch `session-start-<id>` marker（其 mtime 即本次 session 起点）
- 清理旧的 `decision-notified-<id>` marker，每次新 session 都能重新触发一次提醒

自检：项目未启用 ADR 制度（无 docs/decisions/）则静默退出。
状态文件放在 ${CLAUDE_PLUGIN_DATA}/.runtime/，跨 plugin 更新持久化。
"""
from __future__ import annotations

import json
import os
import sys
from typing import Optional


def project_dir() -> str:
    return os.environ.get("CLAUDE_PROJECT_DIR", "")


def docs_decisions_exists() -> bool:
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


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    if not docs_decisions_exists():
        return 0

    session_id = data.get("session_id", "")
    if not session_id:
        return 0

    run_dir = runtime_dir()
    if not run_dir:
        return 0

    # touch session-start marker（存在则刷新 mtime）
    start_marker = os.path.join(run_dir, f"session-start-{session_id}")
    try:
        open(start_marker, "w").close()
    except Exception:
        return 0

    # 清理同 session_id 的 notified marker
    notified = os.path.join(run_dir, f"decision-notified-{session_id}")
    try:
        if os.path.exists(notified):
            os.remove(notified)
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
