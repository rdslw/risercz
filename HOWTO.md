# Howto

How to run research projects in this repo. Agent-facing instructions live in [AGENTS.md](AGENTS.md) (which `CLAUDE.md` points at, so Claude Code and Codex read the same rules).

## Workflow

1. **Think of a question** — best if it has an empirically checkable answer (benchmark, "does X do Y?", "is X safe against Y?", "can X be built?").
2. **Launch an async agent** against `rdslw/risercz`:
   - **Claude**: Claude app / [claude.ai/code](https://claude.ai/code) → new session on this repo, in an environment with network access enabled → paste prompt.
   - **Codex**: ChatGPT app → Codex → this repo, environment with internet access on → paste prompt.
3. **Walk away.** The agent follows AGENTS.md: creates a folder, keeps `notes.md` as it works, writes a `README.md` report, files a PR.
4. **Review the PR** (GitHub mobile app is enough): read the report's README first, skim `notes.md` for the trail. If wrong or incomplete, send follow-up prompts to the same session.
5. **Keep provenance in the PR description**: the original prompt as a `>` blockquote plus a link to the session transcript. Claude Code adds `Claude-Session:` links automatically; paste the Codex task link manually.
6. **Merge.** CI does the rest: generates a cached `_summary.md` via GitHub Models, rebuilds the README index, injects the AI-generated-note disclaimer into the project README, and deploys everything to <https://rdslw.github.io/risercz/>. No manual steps.

Treat the reports as unreviewed AI output: useful, linkable, never blindly trusted.

## How to construct a prompt

Three ingredients, written conversationally:

1. **Objective** — the question to answer or thing to build. Deliberately underspecify when you want to test the agent's own research ability ("...compared to other popular libraries").
2. **Output format** — what should end up in the folder: a report with a comparison table, charts, JSON results, a working demo, a test suite proving the claim.
3. **Starting pointers** — URLs to fetch first, tools to try (`uvx foo --help`), commands to run, repos to check out. The more precise the pointers, the less the agent flails.

Add constraints when they matter: "test against a local server", "must run offline", "include failing cases too".

## Example prompts

Each example links to the project in [simonw/research](https://github.com/simonw/research) that a prompt like it produced.

1. **Library benchmark, deliberately open-ended** — "Create a performance benchmark and feature comparison report on PyPI cmarkgfm compared to other popular Python markdown libraries." → [python-markdown-comparison](https://github.com/simonw/research/tree/main/python-markdown-comparison)
2. **Strategy benchmark** — "Benchmark five different ways of implementing tags in SQLite (JSON arrays, JSON + lookup table, many-to-many tables, FTS5, LIKE queries) with 100k rows. Report timings per query type, storage size, and a recommendation table." → [sqlite-tags-benchmark](https://github.com/simonw/research/tree/main/sqlite-tags-benchmark)
3. **Security parity investigation** — "Datasette runs untrusted SQL safely against SQLite using read-only connections and time limits. Investigate whether DuckDB can be configured to be equally safe. Write a hardened wrapper module and tests that prove each escape route is blocked." → [datasette-duckdb-safety](https://github.com/simonw/research/tree/main/datasette-duckdb-safety)
4. **Browser security experiment with pointers** — "Fetch <url-to-notes> to /tmp with curl. Run `uvx rodney --help` to learn Rodney. Then run robust experiments against a local `python -m http.server` to test whether JavaScript inside a sandboxed iframe can remove or modify a CSP meta tag and escape its restrictions." → [test-csp-iframe-escape](https://github.com/simonw/research/tree/main/test-csp-iframe-escape)
5. **Empirical infrastructure test** — "Do SQLite databases in WAL mode work correctly when two Docker containers share the same volume? Write scripts that run concurrent readers and writers across containers and report whether locking and mmap actually work." → [sqlite-wal-docker-containers](https://github.com/simonw/research/tree/main/sqlite-wal-docker-containers)
6. **Ecosystem survey** — "Research the current options for safely sandboxing untrusted JavaScript in Node.js: built-in vm, worker_threads, the Permission Model, isolated-vm, vm2, quickjs-emscripten. Build small proof-of-concept escapes/defenses for each and end with a recommendation." → [javascript-sandboxing-research](https://github.com/simonw/research/tree/main/javascript-sandboxing-research)
7. **Web page performance audit** — "Audit the performance of <article URL>. Capture network logs with a headless browser, break down bytes by content vs ads/tracking, and report the overhead-to-content ratio with supporting data files." → [pcgamer-audit](https://github.com/simonw/research/tree/main/pcgamer-audit)
8. **Data transformation for exploration** — "Take Anthropic's published system prompt history and turn it into a git repository where each prompt revision is a commit with the original date, so git log/diff/blame can be used to explore how the prompts evolved." → [extract-system-prompts](https://github.com/simonw/research/tree/main/extract-system-prompts)
9. **Feasibility spike** — "Figure out how to run a Python ASGI application entirely in the browser using Pyodide and a service worker, with no backend server. Prove it with a working FastAPI demo published on this repo's GitHub Pages." → [pyodide-asgi-browser](https://github.com/simonw/research/tree/main/pyodide-asgi-browser)
10. **Small tool with tests** — "Build a Python library + CLI that converts PDF pages to JPEGs using Rust's pdfium-render via PyO3, self-contained in a wheel with no external dependencies. Include tests and a usage README." → [pdf-to-image-converter](https://github.com/simonw/research/tree/main/pdf-to-image-converter)
11. **New library teardown** — "Investigate the newly released pydantic-monty sandboxed Python interpreter: what subset of Python works, how do resource limits behave, can sandboxed code reach the host? Write experiments that document the boundaries." → [monty-investigation](https://github.com/simonw/research/tree/main/monty-investigation)
12. **Working demo of a modern technique** — "Demonstrate modern token-less CSRF protection using Sec-Fetch-Site headers: build a vulnerable FastAPI 'bank' app and a protected version, plus an attacker page, and show with screenshots which attacks succeed and fail." → [csrf-protection-demo](https://github.com/simonw/research/tree/main/csrf-protection-demo)
