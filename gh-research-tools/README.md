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


## Should Showboat always manage notes?

For research projects here, the best default is **yes, use Showboat for the evidence trail**, but **do not replace `notes.md` with Showboat**. Treat `notes.md` as the human running log required by this repo and `proof.md` as the executable, replayable appendix.

Recommended always-on approach:

1. Create `notes.md` immediately and append short working notes as usual.
2. Initialize `proof.md` with `showboat init` as soon as the work involves commands, source checks, downloads, screenshots, or transformations that a reviewer may want to replay.
3. Mirror important milestones in both places: concise reasoning in `notes.md`, exact commands and outputs in `proof.md`.
4. Use `showboat note` for source annotations, hypotheses, caveats, and why a command is being run.
5. Use `showboat exec` for commands whose output matters to the conclusion.
6. Use `showboat verify` near the end only for deterministic sections; for live web observations, record the date and avoid treating drift as a failure.
7. Summarize the conclusions in `README.md`, linking or referring to `proof.md` only when the transcript adds review value.

When not to use Showboat for every single action:

- Very noisy exploratory commands that have no bearing on the final conclusion.
- Commands containing secrets, cookies, tokens, private URLs, or personally sensitive data.
- Live network checks whose changing output would make `verify` misleading unless deliberately documented as a snapshot.
- Large binary generation or full repository checkouts that should not be committed.

A practical policy is: **write every important claim to `README.md`, every important decision to `notes.md`, and every important reproducible command to `proof.md`**.

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


## Pattern 6: issue and pull request archaeology

Use this when researching project history, review discussions, or why a design decision happened.

```bash
showboat note proof.md "Collect the issue title, timeline metadata, and rendered discussion cues."
showboat exec proof.md bash 'python3 - <<"PY"
import json, urllib.request
url="https://api.github.com/repos/simonw/showboat/issues?state=all&per_page=5"
with urllib.request.urlopen(url) as r:
    for issue in json.load(r):
        print(issue["number"], issue["state"], issue["title"])
PY'
showboat exec proof.md bash 'rodney start --local && rodney open https://github.com/simonw/showboat/issues && rodney waitstable && rodney text "main"'
showboat exec proof.md bash 'rodney stop'
```

Why it helps: GitHub APIs provide structured records, while Rodney can capture rendered labels, filters, and UI context that may not be obvious from raw JSON.

## Pattern 7: repository checkout without committing the checkout

Use this when you need to inspect or patch a third-party repository during research, while obeying the repo rule not to commit full fetched code.

```bash
showboat note proof.md "Clone to a temporary directory, inspect, and save only our diff artifact."
tmp=$(mktemp -d)
showboat exec proof.md bash "git clone --depth 1 https://github.com/simonw/showboat '$tmp/showboat' && git -C '$tmp/showboat' status --short"
# If you modify the temporary checkout, save just the patch into the research folder:
showboat exec proof.md bash "git -C '$tmp/showboat' diff > third-party-showboat.diff"
```

Why it helps: the final commit can include `third-party-showboat.diff` and explanatory notes without accidentally vendoring someone else's repository.

## Pattern 8: Python data extraction with uv or uvx

Use this when the research needs Python dependencies, ad-hoc parsing, or repeatable scripts. Prefer `uvx` for one-off tools and `uv run` with inline dependency metadata for scripts that should remain reproducible.

```bash
showboat note proof.md "Run Python with dependencies without creating an untracked virtualenv in the research folder."
showboat exec proof.md bash 'uvx --from sqlite-utils sqlite-utils --version'
mkdir -p scripts
cat > scripts/fetch_repo.py <<'PY'
# /// script
# dependencies = ["httpx"]
# ///
import httpx
repo = httpx.get("https://api.github.com/repos/simonw/showboat", timeout=20).json()
print(repo["full_name"], repo["description"])
PY
showboat exec proof.md bash 'uv run scripts/fetch_repo.py'
```

Why it helps: `uvx` avoids permanent installs for command-line utilities, while `uv run` makes script dependencies explicit and avoids committing `.venv/` or generated package caches.

## Pattern 9: evidence bundle with screenshots plus extracted text

Use this when the visual state matters but reviewers also need searchable text.

```bash
showboat note proof.md "Capture both a screenshot and the text used for the finding."
showboat exec proof.md bash 'mkdir -p screenshots extracts'
showboat exec proof.md bash 'rodney start --local && rodney open https://example.com && rodney waitstable'
showboat exec proof.md bash 'rodney screenshot -w 1440 -h 1000 screenshots/source.png'
showboat exec proof.md bash 'rodney text body > extracts/source.txt && head -40 extracts/source.txt'
showboat image proof.md '![Source page screenshot](screenshots/source.png)'
showboat exec proof.md bash 'rodney stop'
```

Why it helps: screenshots preserve layout and chart-like evidence, while text extracts make the source easier to quote, diff, summarize, and search.

## Suggested user instructions for future research projects

A user can ask the agent to use these tools explicitly. Good prompts:

- "Create a research folder and use Showboat to record a proof transcript of key commands."
- "Use Rodney for any JavaScript-rendered pages, screenshots, or accessibility-tree checks."
- "If you inspect a third-party repository, do not commit the clone; commit only notes, the report, scripts, and any relevant diff files."
- "End with a README summary and include a Showboat `verify` result if the transcript is deterministic."
- "For UI research, include Rodney screenshots and cite them in the report."


## Using uv and uvx for Python during research

If Python is used, prefer `uv`/`uvx` over ad-hoc global installs:

- Use `uvx tool-name ...` for one-off Python CLIs, especially when the tool itself is the thing being exercised or when no script should be committed.
- Use `uv run script.py` for committed research scripts, with inline script dependency metadata so future agents can re-run the script without guessing requirements.
- Keep dependency caches, virtual environments, and downloaded packages out of the research commit. Do not commit `.venv/`, `.cache/`, or generated lockfiles unless the lockfile is intentionally part of the research artifact.
- Capture `uv`/`uvx` commands with `showboat exec` when their output supports a claim in the final report.
- If network-dependent dependency installation is required, call that out in `README.md` and in the Showboat note before the command.

Minimal script pattern:

```python
# /// script
# dependencies = ["httpx"]
# ///
import httpx
print(httpx.get("https://example.com", timeout=20).status_code)
```

Run and record it with:

```bash
showboat exec proof.md bash 'uv run scripts/check_source.py'
```

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
