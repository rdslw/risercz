# Research projects carried out by AI tools

Each directory in this repo is a separate research project carried out by an LLM tool - usually [Claude Code](https://www.claude.com/product/claude-code) or [OpenAI Codex](https://openai.com/codex/). Every single line of text and code was written by an LLM.

This repo follows the approach pioneered by Simon Willison's [simonw/research](https://github.com/simonw/research) - see his post [Code research projects with async coding agents like Claude Code and Codex](https://simonwillison.net/2025/Nov/6/async-code-research/) for details on how this works.

See [HOWTO.md](HOWTO.md) for the workflow and for how to construct research prompts.

Prompts and links to session transcripts are included in [the PRs](https://github.com/rdslw/risercz/pulls?q=is%3Apr+is%3Aclosed) that added each report, or in [the commits](https://github.com/rdslw/risercz/commits/master/).

<!--[[[cog
import os
import re
import subprocess
import pathlib
from datetime import datetime, timezone

# Model to use for generating summaries
MODEL = "github/gpt-4.1"

# Get all subdirectories with their first README commit dates
research_dir = pathlib.Path.cwd()
subdirs_with_dates = []

for d in research_dir.iterdir():
    # Skip hidden dirs and local build/tool output like _site and __pycache__
    # (research folders are kebab-case, never underscore-prefixed)
    if d.is_dir() and not d.name.startswith(('.', '_')):
        readme_path = d / "README.md"
        history_path = str(readme_path.relative_to(research_dir))
        # Get the date of the first commit that touched this project's README
        try:
            result = subprocess.run(
                ['git', 'log', '--follow', '--format=%aI', '--reverse', '--', history_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                # Oldest commit that touched this README
                date_str = result.stdout.strip().splitlines()[0]
                commit_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                subdirs_with_dates.append((d.name, commit_date))
            else:
                # No git history, use README modification time if available
                fallback_path = readme_path if readme_path.exists() else d
                subdirs_with_dates.append((d.name, datetime.fromtimestamp(fallback_path.stat().st_mtime, tz=timezone.utc)))
        except Exception:
            # Fallback to README modification time if available
            fallback_path = readme_path if readme_path.exists() else d
            subdirs_with_dates.append((d.name, datetime.fromtimestamp(fallback_path.stat().st_mtime, tz=timezone.utc)))

# Print the heading with count
print(f"## {len(subdirs_with_dates)} research projects\n")

# Sort by date, most recent first
subdirs_with_dates.sort(key=lambda x: x[1], reverse=True)

for dirname, commit_date in subdirs_with_dates:
    folder_path = research_dir / dirname
    readme_path = folder_path / "README.md"
    summary_path = folder_path / "_summary.md"

    date_formatted = commit_date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M')

    # Get GitHub repo URL
    github_url = None
    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0 and result.stdout.strip():
            origin = result.stdout.strip()
            # Convert SSH URL to HTTPS URL for GitHub
            if origin.startswith('git@github.com:'):
                origin = origin.replace('git@github.com:', 'https://github.com/')
            if origin.endswith('.git'):
                origin = origin[:-4]
            github_url = f"{origin}/tree/master/{dirname}"
    except Exception:
        pass

    # Extract title from first H1 header in README, fallback to dirname
    title = dirname
    if readme_path.exists():
        with open(readme_path, 'r') as f:
            for readme_line in f:
                if readme_line.startswith('# '):
                    title = readme_line[2:].strip()
                    break

    if github_url:
        print(f"### [{title}]({github_url}#readme) ({date_formatted})\n")
    else:
        print(f"### {title} ({date_formatted})\n")

    # Check if summary already exists
    if summary_path.exists():
        # Use cached summary
        with open(summary_path, 'r') as f:
            description = f.read().strip()
            if description:
                print(description)
            else:
                print("*No description available.*")
    elif readme_path.exists():
        # Generate new summary using llm command
        prompt = """Summarize this research project concisely. Write just 1 paragraph (3-5 sentences) followed by an optional short bullet list if there are key findings. Vary your opening - don't start with "This report" or "This research". Include 1-2 links to key tools/projects. Be specific but brief. No emoji."""
        result = subprocess.run(
            ['llm', '-m', MODEL, '-s', prompt],
            stdin=open(readme_path),
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            error_msg = f"LLM command failed for {dirname} with return code {result.returncode}"
            if result.stderr:
                error_msg += f"\nStderr: {result.stderr}"
            raise RuntimeError(error_msg)
        if result.stdout.strip():
            description = result.stdout.strip()
            print(description)
            # Save to cache file
            with open(summary_path, 'w') as f:
                f.write(description + '\n')
        else:
            raise RuntimeError(f"LLM command returned no output for {dirname}")
    else:
        print("*No description available.*")

    print()  # Add blank line between entries

# Add AI-generated note to all project README.md files
# Note: we construct these marker strings via concatenation to avoid the HTML comment close sequence
AI_NOTE_START = "<!-- AI-GENERATED-NOTE --" + ">"
AI_NOTE_END = "<!-- /AI-GENERATED-NOTE --" + ">"
AI_NOTE_CONTENT = """> [!NOTE]
> This is an AI-generated research report. All text and code in this report was created by an LLM (Large Language Model). For more information on how these reports are created, see the [main research repository](https://github.com/rdslw/risercz)."""

NOT_AI_GENERATED = "<!-- not-ai-generated --" + ">"

for dirname, _ in subdirs_with_dates:
    folder_path = research_dir / dirname
    readme_path = folder_path / "README.md"

    if not readme_path.exists():
        continue

    content = readme_path.read_text()

    # Skip files marked as not AI-generated
    if NOT_AI_GENERATED in content:
        continue

    # Check if note already exists
    if AI_NOTE_START in content:
        # Replace existing note
        pattern = re.escape(AI_NOTE_START) + r'.*?' + re.escape(AI_NOTE_END)
        new_note = f"{AI_NOTE_START}\n{AI_NOTE_CONTENT}\n{AI_NOTE_END}"
        new_content = re.sub(pattern, new_note, content, flags=re.DOTALL)
        if new_content != content:
            readme_path.write_text(new_content)
    else:
        # Add note after first heading (# ...)
        lines = content.split('\n')
        new_lines = []
        note_added = False
        for i, line in enumerate(lines):
            new_lines.append(line)
            if not note_added and line.startswith('# '):
                # Add blank line, then note, then blank line
                new_lines.append('')
                new_lines.append(AI_NOTE_START)
                new_lines.append(AI_NOTE_CONTENT)
                new_lines.append(AI_NOTE_END)
                note_added = True

        if note_added:
            readme_path.write_text('\n'.join(new_lines))

]]]-->
## 4 research projects

### [browser-ai-steering](https://github.com/rdslw/risercz/tree/master/browser-ai-steering#readme) (2026-07-06 22:03)

Browser AI steering tools are rapidly evolving to meet the needs of AI agents that must interact with modern websites in both transactional (e.g., banking, e-commerce) and exploratory (API mapping, frontend cloning) contexts. The landscape now balances agent ergonomics, browser fidelity, security posture, and inspection power: tools like [Playwriter](https://github.com/remorses/playwriter) excel at leveraging a real user’s Chrome session for SSO- and extension-dependent flows, while [Wirebrowser](https://github.com/fcavallarin/wirebrowser) specializes in runtime JavaScript and API reverse-engineering. Highly agent-friendly CLIs such as [agent-browser](https://github.com/vercel-labs/agent-browser) and scriptable harnesses like Browser Harness offer flexibility for coding agents, whereas infrastructure-oriented solutions like Steel Browser supply session lifecycle and scaling. The dominant trade-offs are between reproducibility/safety (sterile browser environments with fixed toolsets) and maximum capability (direct access to real user sessions and low-level runtime introspection).

Key Findings:
- **Playwriter + Wirebrowser** is the strongest pairing for maximum capability across both transactional steering and API mapping, provided strict security controls are enforced.
- **Playwright MCP + Wirebrowser** is recommended for enterprise environments that require standardized, isolated browser automation.
- Tools split into those optimized for execution (agent control, repeatability) versus those optimized for understanding (runtime instrumentation, API causality), so combining both is often necessary.
- All tools handling sensitive accounts require human-in-the-loop approval, audit logging, and isolated/dedicated browser profiles for safe use.
- For complex web automation, no single tool covers the full spectrum—purpose-built combinations outperform one-size-fits-all solutions.

### [Rodney and Showboat for research projects](https://github.com/rdslw/risercz/tree/master/rodney-showboat-patterns#readme) (2026-07-06 20:32)

For research workflows requiring both web interaction and reproducible evidence, Rodney and Showboat—two command-line tools from Simon Willison—offer complementary strengths. Rodney ([GitHub](https://github.com/simonw/rodney)) enables persistent browser-driven inspection and extraction from JavaScript-rich or stateful web pages, capturing rendered content, screenshots, accessibility data, and UI workflows that go beyond simple HTML fetches. Showboat ([GitHub](https://github.com/simonw/showboat)) creates executable Markdown transcripts that log commentary, commands, and output side-by-side—making research steps transparent, rerunnable, and easy to verify or review. Integrating Rodney for browser interaction and Showboat for evidence capture transforms ad-hoc investigations into durable, replayable artifacts, enhancing reproducibility and auditability without altering existing folder or note conventions.

**Key Findings:**
- Rodney provides persistent Chrome session control, DOM extraction, visual evidence capture, accessibility tree inspection, and script-friendly assertion checks.
- Showboat offers executable Markdown documents, reproducibility verification, code extraction, in-context images, and error-tolerant logging.
- Using both tools together ensures explorations are browsable, verifiable, and easily reviewed—bridging the gap between loose chat logs and formal proof transcripts.
- Existing research structures (notes, README, scripts) are complemented rather than replaced, with practical folder layouts and clear guidance for evidence management.

### [Passkey Tester](https://github.com/rdslw/risercz/tree/master/passkey-tester#readme) (2026-07-05 19:43)

Passkey Tester is a single-page web tool for evaluating browser password managers and authenticators using WebAuthn passkey registration and authentication flows. Users can test how different platforms handle passkey ceremonies, inspect attestation details, and review metadata stored client-side, without access to private keys. The tool supports configurable authentication requirements and exposes credential data for educational and debugging purposes, but emphasizes that robust attestation validation must occur server-side. For hands-on testing and inspection, the artifact is available at the [GitHub demo](https://rdslw.github.io/risercz/passkey-tester/demo.html).

**Key Features:**
- Tests `navigator.credentials.create` and `navigator.credentials.get` WebAuthn flows.
- Metadata and attestation details are viewable via localStorage—only public outputs are accessible.
- Designed to help developers explore authenticator properties; not intended for production security validation.

### [Pipeline self-test: does the publishing plumbing of this repo work?](https://github.com/rdslw/risercz/tree/master/pipeline-selftest#readme) (2026-07-05 16:01)

Focusing on validating its own automation workflow, this project ensures that the repository's publishing pipeline functions as intended with a `master` default branch. Key adaptations from [simonw/research](https://github.com/simonw/research) were made to support master branch triggers and links. All essential steps—from automated README indexing, AI-generated summaries (using GitHub Models), bot-generated commits, to Pages deployment—are confirmed through observable artifacts, including a live demo page and workflow run logs. The process is designed to avoid redundant workflow retriggers and facilitate clear verification.

**Key findings:**
- End-to-end pipeline functions correctly, verified by live artifacts: README indexing, AI summary generation, note injection, and [GitHub Pages deployment](https://rdslw.github.io/risercz/).
- Adaptation for master branch required only minimal workflow and script changes.
- Automation prevents workflow self-retriggering, ensuring efficiency.

<!--[[[end]]]-->

---

## Updating this README

This README uses [cogapp](https://nedbatchelder.com/code/cog/) to automatically generate project descriptions.

A GitHub Action runs `cog -r -P README.md` on every push to master and commits any changes to the README or new `_summary.md` files, then builds and deploys the GitHub Pages site.

To update locally: `GITHUB_TOKEN=$(gh auth token) uv run --with-requirements requirements.txt cog -r -P README.md`

The script discovers all project subdirectories, sorts them by the first commit that touched each folder's `README.md` (newest first), and for each folder either reuses the cached `_summary.md` or generates a new one with `llm -m github/gpt-4.1`.
To regenerate a specific project's description, delete its `_summary.md` file and run cog again.
