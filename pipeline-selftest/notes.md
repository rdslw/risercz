# Working notes

- Ported the plumbing from simonw/research: cog-driven README index, GitHub Models summaries, AI-note injection, GitHub Pages build with per-folder hooks.
- Repo-specific changes made while porting:
  - Workflow trigger `main` → `master`.
  - Cog script project links `/tree/main/` → `/tree/master/`.
  - `render-readme-index.py`: fallback `GITHUB_REPOSITORY` context and User-Agent updated to `rdslw/risercz`.
  - AI-note text links to this repo instead of simonw/research.
- Checked the risk of workflow loops: the bot commit only touches `README.md`, `*/README.md` and `*/_summary.md`, all covered by `paths-ignore`, so no retrigger.
- `_summary.md` for this folder must NOT be committed by hand — its absence is what triggers the GitHub Models summary generation, which is one of the things this self-test verifies.
- demo.html kept dependency-free so it cannot fail for reasons unrelated to hosting.
