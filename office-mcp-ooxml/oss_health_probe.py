import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPOS = {
    "python-office-mcp-server": {
        "slug": "rcarmo/python-office-mcp-server",
        "path": "/tmp/office-mcp-ooxml-work/python-office-mcp-server",
    },
    "go-ooxml": {
        "slug": "rcarmo/go-ooxml",
        "path": "/tmp/office-mcp-ooxml-work/go-ooxml",
    },
}

def git(repo_path, *args):
    return subprocess.check_output(["git", "-C", repo_path, *args], text=True).strip()

def api(path):
    with urllib.request.urlopen(f"https://api.github.com/{path}") as r:
        return json.load(r)

def months_between(first_iso, last_iso):
    first = datetime.fromisoformat(first_iso.replace("Z", "+00:00"))
    last = datetime.fromisoformat(last_iso.replace("Z", "+00:00"))
    days = max((last - first).days, 1)
    return round(days / 30.4375, 2)

out = {}
for name, cfg in REPOS.items():
    path = cfg["path"]
    commits_all = git(path, "log", "--all", "--reverse", "--format=%cI").splitlines()
    first = commits_all[0]
    last = git(path, "log", "--all", "-1", "--format=%cI")
    commits_12_lines = git(path, "log", "--all", "--since=12 months ago", "--format=%H").splitlines()
    commits_12 = len(commits_12_lines)
    authors_all = git(path, "log", "--all", "--format=%an <%ae>").splitlines()
    authors_12 = git(path, "log", "--all", "--since=12 months ago", "--format=%an <%ae>").splitlines()
    repo = api(f"repos/{cfg['slug']}")
    prs_total = api(f"search/issues?q=repo:{cfg['slug']}+type:pr")["total_count"]
    prs_open = api(f"search/issues?q=repo:{cfg['slug']}+type:pr+state:open")["total_count"]
    out[name] = {
        "github": cfg["slug"],
        "first_commit": first,
        "last_commit": last,
        "commit_timespan_months": months_between(first, last),
        "commits_last_12_months": commits_12,
        "avg_commits_per_month_last_12_months": round(commits_12 / 12, 2),
        "different_authors_all_time": len(set(authors_all)),
        "different_authors_last_12_months": len(set(authors_12)),
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "open_issues_count": repo["open_issues_count"],
        "prs_total": prs_total,
        "prs_open": prs_open,
        "license": repo["license"]["spdx_id"] if repo.get("license") else None,
        "created_at": repo["created_at"],
        "pushed_at": repo["pushed_at"],
        "commercial_backing_or_offering_found": False,
        "commercial_note": "No commercial offering/backing found in README or GitHub metadata during this probe.",
    }

Path("office-mcp-ooxml/oss_health.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
