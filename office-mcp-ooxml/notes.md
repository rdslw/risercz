# Notes

- Started investigation on 2026-07-07. Created work folder `office-mcp-ooxml`.

- Cloned python-office-mcp-server and go-ooxml into /tmp for analysis.
python-office-mcp-server commit: d61959f4e3c3d627745f61238257745067675e9d
go-ooxml commit: 43eda6edfe45db20da5879ba332ec6a25d598efa

- Wrote Python and Go generators in the work folder.

- Ran Python Office MCP unified read/inspect over both Python- and Go-created artifacts.
- Ran Go OOXML open/read inspection over both Python- and Go-created artifacts.

- Wrote README report with installation, creation, cross-analysis, and recommendation.

- Re-ran Python/Go creation and analysis scripts successfully before commit.

- Cleaned unused imports and gofmt-ed Go probes.

- Follow-up requested: expanding open-source health and local LLM/user workflow analysis. Tried to fetch current PR branch but no `origin` remote is configured in this workspace. Refreshed upstream clones in /tmp.

- Queried GitHub API for stars, PR counts, license, and repository timestamps.

- Added OSS health and local-LLM workflow probe scripts.

- Ran OSS health probe and local-LLM workflow probe successfully.

- Expanded README with open-source health and local LLM workflow sections.

- Removed generated binary Office artifacts from the branch so the PR contains only text/code/report outputs.
