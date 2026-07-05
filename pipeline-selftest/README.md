# Pipeline self-test: does the publishing plumbing of this repo work?

<!-- AI-GENERATED-NOTE -->
> [!NOTE]
> This is an AI-generated research report. All text and code in this report was created by an LLM (Large Language Model). For more information on how these reports are created, see the [main research repository](https://github.com/rdslw/risercz).
<!-- /AI-GENERATED-NOTE -->

A minimal first research project whose subject is the repository itself. It exists to verify, end to end, that the automation copied from [simonw/research](https://github.com/simonw/research) works on this repo with a `master` default branch.

**Live demo (proves Pages deployment):** https://rdslw.github.io/risercz/pipeline-selftest/demo.html

## What the pipeline is supposed to do on every push to master

1. `cog -r -P README.md` regenerates the root README index: one dated entry per project folder, sorted by the first commit that touched each folder's `README.md`.
2. For any folder without a `_summary.md`, the cog script pipes that folder's README through `llm -m github/gpt-4.1` (GitHub Models, authenticated by the workflow's ephemeral `GITHUB_TOKEN` with `models: read` permission) and caches the result as `_summary.md`.
3. The same script injects an "AI-generated report" note after the first H1 of every project README that doesn't opt out with a `not-ai-generated` marker.
4. A bot commit pushes the regenerated files back to master; `paths-ignore` on README/`_summary.md` files prevents the commit from retriggering the workflow.
5. `build-github-pages.sh` runs any per-folder `github-pages.sh` hooks, rsyncs the repo into `_site/`, renders the root README to `index.html` via the GitHub Markdown API, and deploys `_site/` to GitHub Pages.

## Verification checklist

Each item is confirmed by an observable artifact:

| Check | Evidence |
|---|---|
| Folder indexed with correct date | This project appears in the [root README](https://github.com/rdslw/risercz#readme) with its first-commit date in UTC |
| Summary generated via GitHub Models | `_summary.md` exists in this folder and was committed by `github-actions[bot]` |
| AI note injected | The note block appears right below the H1 above |
| Pages deploy works | https://rdslw.github.io/risercz/ renders the index |
| Per-project files served | The [demo page](https://rdslw.github.io/risercz/pipeline-selftest/demo.html) loads |
| Workflow does not self-retrigger | Exactly one workflow run per human push, plus none for the bot commit |

## Notes on the master-branch adaptation

The upstream repo uses `main`; this repo uses `master`. Two places needed changes: the workflow trigger (`branches: [master]`) and the cog script's project links (`/tree/master/`). Everything else in the pipeline is branch-agnostic because Actions operates on the pushed ref and `git log` follows the checked-out history.
