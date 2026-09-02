from __future__ import annotations
import json
import os
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "profile-config.json"
README = ROOT / "README.md"
TEMPLATE = ROOT / "PROFILE_README_TEMPLATE.md"

def sh(*args: str) -> str:
    try:
        return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""

def replace_block(text: str, start: str, end: str, body: str) -> str:
    a = text.find(start)
    b = text.find(end)
    if a == -1 or b == -1 or b < a:
        return text
    return text[:a + len(start)] + "\n" + body.strip() + "\n" + text[b:]

def recent_activity() -> str:
    log = sh("git", "log", "-8", "--pretty=format:%ad|%s", "--date=short")
    if not log:
        return "- Recent activity will appear here after the repository has commits."
    rows = []
    for line in log.splitlines():
        if "|" in line:
            date, subject = line.split("|", 1)
            rows.append(f"- **{date}** — {subject}")
    return "\n".join(rows)

def main():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    if not README.exists() or "FEATURED_REPOS_START" not in README.read_text(encoding="utf-8"):
        README.write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")

    text = README.read_text(encoding="utf-8")

    featured = "\n".join(
        f"- `{repo}` — keep this repository polished, documented, and actively maintained."
        for repo in cfg.get("featured_repositories", [])
    ) or "- Add repositories in `profile-config.json`."

    text = replace_block(
        text,
        "<!-- FEATURED_REPOS_START -->",
        "<!-- FEATURED_REPOS_END -->",
        featured
    )

    text = replace_block(
        text,
        "<!-- RECENT_ACTIVITY_START -->",
        "<!-- RECENT_ACTIVITY_END -->",
        recent_activity()
    )

    README.write_text(text, encoding="utf-8")
    print("Profile README updated.")

if __name__ == "__main__":
    main()
