from __future__ import annotations
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "social-post-drafts.md"

def sh(*args):
    try:
        return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""

repo = sh("git", "config", "--get", "remote.origin.url") or "your GitHub repository"
recent = sh("git", "log", "-5", "--pretty=format:- %s")

if not recent:
    recent = "- Added new engineering updates"

content = f"""# Social Post Drafts

Generated: {datetime.utcnow().strftime("%Y-%m-%d UTC")}

## LinkedIn

I’ve been working on a few engineering updates recently:

{recent}

I’m continuing to focus on production-ready full-stack, backend, cloud, and AI/LLM systems.

Repository: {repo}

#SoftwareEngineering #Python #React #AI #SaaS

## Short post

Shipping consistently matters.

Recent work:
{recent}

More on GitHub: {repo}

## Dev community post

This week I focused on practical engineering improvements rather than demo-only code.

{recent}

If you're working on similar Python, Node.js, React, cloud, or AI/LLM systems, feel free to check the repository and open an issue or discussion.
"""

OUT.write_text(content, encoding="utf-8")
print(f"Wrote {OUT}")
