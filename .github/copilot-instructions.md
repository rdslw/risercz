# Copilot code review instructions

This repo collects self-contained AI-agent research projects, one folder per
project (conventions in AGENTS.md). Merged folders are published verbatim to
GitHub Pages at https://rdslw.github.io/risercz/, so HTML demos run on the
public web.

When reviewing pull requests:

- Prioritize security bugs in HTML/JS demos: XSS and DOM injection (raw
  interpolation into `innerHTML`/attributes), unsafe handling of URL/query/
  `localStorage` data, committed secrets or tokens, and unpinned or untrusted
  external scripts.
- Check cross-browser and cross-platform behavior of demos: current Chrome,
  Firefox and Safari, on both desktop and mobile (touch input, small
  viewports, iOS Safari quirks). Flag APIs with poor support unless the code
  feature-detects and degrades gracefully.
- Verify that claims in a project's README.md are backed by the code or data
  in the same folder.
- Do not nitpick wording or style in notes.md (a working log) or README.md
  prose; comment on report text only for factual or technical errors.
- Flag any file that looks like a full copy of an external repo — AGENTS.md
  requires diffs only, never fetched-code copies.
- Check for serious bugs and logical flaws.
