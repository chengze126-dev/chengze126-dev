from __future__ import annotations
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release-promotion-draft.md"

def sh(*args):
    try:
        return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""

tag = os.getenv("GITHUB_REF_NAME") or sh("git", "describe", "--tags", "--abbrev=0") or "latest release"
changes = sh("git", "log", "-8", "--pretty=format:- %s")

content = f"""# Release Promotion Draft

## {tag}

New release shipped.

### Highlights
{changes or "- Product improvements and fixes"}

### Promotion checklist
- Update repository README
- Add screenshots or demo GIF
- Publish GitHub Release notes
- Share to LinkedIn
- Share to Dev.to / Hashnode
- Mention the concrete problem solved
- Invite feedback, issues, and contributions
"""

OUT.write_text(content, encoding="utf-8")
print(f"Wrote {OUT}")
