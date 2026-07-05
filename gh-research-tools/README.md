# Rodney and Showboat for research projects

## Scope

This report evaluates two Simon Willison GitHub tools for use in research projects in this repository:

- [`simonw/rodney`](https://github.com/simonw/rodney): a command-line interface for driving a persistent Chrome browser session.
- [`simonw/showboat`](https://github.com/simonw/showboat): a command-line interface for building executable Markdown documents that combine commentary, commands, output, and images.

The central recommendation: use **Rodney to inspect and interact with web pages** and use **Showboat to preserve a reproducible transcript of what was tried and what happened**. Together they turn research from a loose chat transcript into a browsable, replayable, and reviewable artifact.

## What Rodney contributes

Rodney is useful when the research task involves pages that are not well represented by raw HTML fetches: single-page apps, UI state, charts, authenticated sessions, accessibility trees, screenshots, PDFs, or workflows that require clicking and typing. Its README describes it as a Go CLI that drives a persistent headless Chrome instance through the Rod browser automation library. Each command connects to the same long-running Chrome process, which makes multi-step shell scripting practical.

Capabilities that matter for research:

1. **Persistent browser state.** Start a browser once, then navigate, click, type, inspect, screenshot, and continue from the same page state. This is helpful for exploratory research where each step depends on the previous one.
2. **DOM extraction.** `rodney title`, `rodney text`, `rodney html`, `rodney attr`, `rodney count`, and `rodney js` let an agent pull structured facts out of rendered pages.
3. **Page readiness waits.** `rodney wait`, `waitload`, `waitstable`, and `waitidle` reduce flaky captures from pages that render asynchronously.
4. **Screenshots and PDFs.** `rodney screenshot`, `screenshot-el`, and `pdf` can preserve evidence for visual or document-heavy investigations.
5. **Accessibility inspection.** `ax-tree`, `ax-find`, and `ax-node` expose the browser accessibility tree, useful for UI audits and for finding elements by semantic role.
6. **Script-friendly checks.** Commands such as `exists`, `visible`, and `assert` have distinct exit-code behavior, which supports CI-like smoke checks in a research folder.
7. **Local sessions.** `rodney start --local` stores state in `./.rodney/`, which fits per-project isolation. Do not commit `.rodney/`.

## What Showboat contributes

Showboat is useful when the research task should leave behind evidence that another person or agent can verify. Its README says it creates Markdown documents that mix commentary, executable code blocks, and captured output; a verifier can re-run the code blocks and compare outputs.

Capabilities that matter for research:

1. **Executable notes.** `showboat note` records human commentary; `showboat exec` records commands and their output.
2. **Reproducibility checks.** `showboat verify` re-runs code blocks and reports output drift.
3. **Recoverable workflows.** `showboat extract` emits the commands needed to recreate a document from scratch.
4. **Screenshots in context.** `showboat image` copies an image next to the document and embeds it, so visual evidence appears beside the commands that produced it.
5. **Remote streaming.** `SHOWBOAT_REMOTE_URL` can stream updates to a remote viewer, making long-running research easier to review while it happens.
6. **Error-friendly iteration.** `showboat exec` still appends failing commands; `showboat pop` can remove a mistaken step after inspection.

## How they fit this repository's research workflow

This repository already asks each investigation to create a short slug folder, maintain `notes.md`, and finish with `README.md`. Rodney and Showboat can complement that structure without replacing it:

- `notes.md`: lightweight running log of decisions, dead ends, and sources.
- `README.md`: final synthesized report.
- `demo.md` or `proof.md` created by Showboat: reproducible command transcript and evidence trail.
- Screenshots/PDFs under the same folder only when they are small enough and directly useful.
- `.rodney/`: local browser state, uncommitted.

Recommended file layout:

```text
my-research-slug/
  notes.md
  README.md
  proof.md              # optional Showboat transcript
  screenshots/          # optional small evidence images
  scripts/              # optional reusable helpers
```

## Pattern 1: rendered-page evidence capture

Use this when a source page is JavaScript-heavy or visual.

```bash
cd my-research-slug
showboat init proof.md "Rendered source capture"
showboat note proof.md "Open the target page in an isolated Rodney session."
rodney start --local
showboat exec proof.md bash 'rodney open https://example.com && rodney waitstable && rodney title'
showboat exec proof.md bash 'rodney text h1'
showboat exec proof.md bash 'mkdir -p screenshots && rodney screenshot -w 1280 -h 720 screenshots/example.png'
showboat image proof.md '![Example rendered page](screenshots/example.png)'
rodney stop
```

Why it helps: the final report can cite the observed page title/text, while `proof.md` shows exactly how the browser evidence was captured.

## Pattern 2: source comparison matrix

Use Rodney for dynamic pages and regular CLI tools for APIs or static pages, all recorded through Showboat.

```bash
showboat init proof.md "Compare source claims"
showboat note proof.md "Collect rendered browser title and API metadata for the same project."
showboat exec proof.md bash 'rodney start --local && rodney open https://github.com/simonw/showboat && rodney waitstable && rodney title'
showboat exec proof.md bash 'python3 - <<"PY"
import json, urllib.request
url="https://api.github.com/repos/simonw/showboat"
with urllib.request.urlopen(url) as r:
    data=json.load(r)
print({k:data[k] for k in ["full_name", "description", "stargazers_count", "forks_count"]})
PY'
showboat exec proof.md bash 'rodney stop'
```

Why it helps: dynamic observations and API facts are captured side-by-side instead of being scattered through terminal history.

## Pattern 3: UI smoke test as research artifact

Use this when the research task evaluates whether a tool, demo, or documentation site works.

```bash
cat > smoke.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
fail=0
check() {
  if ! "$@"; then
    echo "FAIL: $*"
    fail=1
  fi
}
rodney start --local
rodney open "https://example.com"
rodney waitstable
check rodney exists "h1"
check rodney visible "h1"
check rodney assert "document.title" "Example Domain"
rodney stop
exit "$fail"
SH
chmod +x smoke.sh
showboat exec proof.md bash './smoke.sh'
```

Why it helps: the report can say not only what was observed, but what repeatable checks passed.

## Pattern 4: accessibility-oriented research

Use this when the research question includes usability, screen-reader structure, or semantic navigation.

```bash
showboat exec proof.md bash 'rodney start --local && rodney open https://example.com && rodney waitstable'
showboat exec proof.md bash 'rodney ax-find --role heading --json'
showboat exec proof.md bash 'rodney ax-find --role link --json'
showboat exec proof.md bash 'rodney stop'
```

Why it helps: screenshots show appearance, while accessibility-tree extracts show what assistive technologies can see.

## Pattern 5: reproducible research packet

At the end of a project, run verification and extract the recreation commands:

```bash
showboat verify proof.md
showboat extract proof.md > recreate-proof.sh
```

Commit `proof.md` if it is valuable and stable. Commit `recreate-proof.sh` only if it adds value as code written during the investigation. Avoid committing browser profiles, caches, full cloned repositories, or bulky generated artifacts.

## Suggested user instructions for future research projects

A user can ask the agent to use these tools explicitly. Good prompts:

- "Create a research folder and use Showboat to record a proof transcript of key commands."
- "Use Rodney for any JavaScript-rendered pages, screenshots, or accessibility-tree checks."
- "If you inspect a third-party repository, do not commit the clone; commit only notes, the report, scripts, and any relevant diff files."
- "End with a README summary and include a Showboat `verify` result if the transcript is deterministic."
- "For UI research, include Rodney screenshots and cite them in the report."

## Practical cautions

- Rodney depends on Chrome or Chromium being installed and reachable, or `ROD_CHROME_BIN` being set.
- Browser sessions may include cookies or local state; use `--local` and keep `.rodney/` out of git.
- Showboat verification is strongest for deterministic commands. Network calls, timestamps, changing GitHub star counts, and live webpages may drift; mark those as live observations or avoid verifying them directly.
- Keep binary artifacts small and purposeful. Prefer text extracts, scripts, and diffs over full fetched repositories.
- Rodney is a browser automation tool, not a source of truth. Pair it with primary sources and record URLs, dates, and commands.

## Bottom line

Use Rodney when research needs a real browser. Use Showboat when research needs durable proof. Used together, they create a strong loop: **observe with Chrome, capture with Markdown, verify with re-execution, summarize in README**.


## Sources checked

- `https://raw.githubusercontent.com/simonw/rodney/main/README.md` on 2026-07-05. Key README claims checked: persistent headless Chrome CLI, same long-running Chrome process, start/open/js/stop architecture, Chrome/Chromium requirement, extraction commands, waits, and screenshots.
- `https://raw.githubusercontent.com/simonw/showboat/main/README.md` on 2026-07-05. Key README claims checked: executable demo documents, commentary plus code/output, `init`, `note`, `exec`, `image`, `pop`, `verify`, and `extract` commands.
- GitHub repository pages for `simonw/rodney`, `simonw/showboat`, and `simonw/research` on 2026-07-05.
