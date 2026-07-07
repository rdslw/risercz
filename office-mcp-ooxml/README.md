# python-office-mcp-server vs go-ooxml for Office P&L workflows

<!-- AI-GENERATED-NOTE -->
> [!NOTE]
> This is an AI-generated research report. All text and code in this report was created by an LLM (Large Language Model). For more information on how these reports are created, see the [main research repository](https://github.com/rdslw/risercz).
<!-- /AI-GENERATED-NOTE -->

## Scope

I fetched and tested:

- `rcarmo/python-office-mcp-server` at commit `d61959f4e3c3d627745f61238257745067675e9d`.
- `rcarmo/go-ooxml` at commit `43eda6edfe45db20da5879ba332ec6a25d598efa`.

The practical test focused on the company use case: frequent creation and analysis of Word (`.docx`) and Excel (`.xlsx`) files for sales and product-management teams.

## What I built

This folder contains small reproducible probes:

- `make_python_docs.py` creates a board-style P&L Word document and Excel workbook using the Python ecosystem used by `python-office-mcp-server`.
- `go_pl_roundtrip.go` creates a similar P&L Word document and Excel workbook using `go-ooxml`.
- `analyze_cross.py` asks `python-office-mcp-server` to read and inspect both the Python-created and Go-created artifacts.
- `go_analyze.go` asks `go-ooxml` to open and summarize both the Python-created and Go-created artifacts.
- `python_office_analysis.json` and `go_ooxml_analysis.txt` capture the cross-analysis output.

Generated sample files are written to `artifacts/` when the probes are run locally; binary Office artifacts are intentionally not committed.

## Installation results

### python-office-mcp-server

Installed successfully in a local virtual environment with:

```bash
python3 -m venv /tmp/office-mcp-ooxml-work/venv
. /tmp/office-mcp-ooxml-work/venv/bin/activate
pip install -e /tmp/office-mcp-ooxml-work/python-office-mcp-server
```

Its installation was straightforward. It exposes a broad MCP-oriented tool surface for reading, inspecting, patching, templating, comments, auditing, tables, images, and Markdown conversions across Office documents.

### go-ooxml

The Go library was usable from a small local module with a `replace` directive pointing to the fetched checkout. The Go toolchain automatically downloaded a newer Go toolchain because the repository requires Go 1.25.6+.

A targeted test command produced mixed results:

```bash
go test ./pkg/document ./pkg/spreadsheet
```

`pkg/document` passed, but `pkg/spreadsheet` failed on fixture-roundtrip tests because it expected `/workspace/testdata/excel/*.xlsx`, which was not present in this environment. That looks like a repository/test-data environment issue rather than proof that the spreadsheet package cannot run.

## Practical creation test

### Python path

The Python path was easiest for producing a richer business artifact quickly:

- Word: headings, bullets, styled tables, narrative commentary, and a risk register.
- Excel: formulas, number formats, freeze panes, filters, styled headers, and a chart.

This was productive because `python-office-mcp-server` builds on mature Python Office packages (`python-docx`, `openpyxl`, `python-pptx`) and already has workflow-level read/inspect/patch abstractions.

### Go path

The Go path successfully created both `.docx` and `.xlsx` files, but the API felt lower-level and less forgiving for business-document generation:

- Word generation of paragraphs and tables worked.
- Excel generation of values and a table worked.
- Styling, formulas, charts, and high-level document workflows required more manual API discovery or were less obvious from the public examples.
- The generated `go_pl.docx` was tiny and readable, but less polished than the Python-generated document.

One notable issue: after adding an Excel table with `go-ooxml`, reading `go_pl.xlsx` back through both tools showed generic table headers (`Column1`, `Column2`, etc.) instead of the headers I had set. That suggests the table creation path may mutate or overwrite header labels in this scenario.

## Cross-analysis test

### python-office-mcp-server reading go-ooxml artifacts

This worked well for both Go-created files:

- It extracted Go-created Word paragraphs and table content.
- It converted the Go-created Word table to Markdown.
- It extracted Go-created Excel rows and sheet data.

The Python server's output is immediately useful to an LLM/MCP workflow because it returns JSON and Markdown-friendly representations.

### go-ooxml reading Python-created artifacts

This also worked for basic structure:

- It opened the Python-created Word document.
- It counted 10 paragraphs and 2 tables.
- It extracted the first rows of both Word tables.
- It opened the Python-created Excel workbook and saw one sheet with the expected dimensions.

However, the Go reader did not surface the same convenient business-level representation. For example, in my simple probe, formula cells without cached values appeared empty through `String()`, whereas `python-office-mcp-server` can explicitly read formulas with `include_formulas=True`.

## Maturity and fit assessment

| Criterion | python-office-mcp-server | go-ooxml |
| --- | --- | --- |
| Install/use speed | Better for a sales/PM automation team; quick Python install and tool calls. | Fine for Go engineers, but requires Go 1.25.6+ and more library-level work. |
| Document creation | Better for rich business docs today via mature Python libraries and Markdown/workflow helpers. | Capable for basic OOXML creation; less ergonomic for complex sales/PM artifacts. |
| Document analysis | Much better out of the box: `office_read`, `office_inspect`, Markdown/JSON, formulas option, auditing tools. | Can open and traverse OOXML, but requires custom code to produce useful summaries. |
| Word support | Practical, higher-level, with extraction, Markdown, placeholders, sections, comments, track changes helpers. | Promising low-level API with paragraphs, tables, comments, track changes, content controls. |
| Excel support | Practical for workbook reads, ranges, formulas, patching, Markdown, and use of `openpyxl`. | Can create/open sheets, cells, tables, styles, comments; table behavior looked rough in the probe. |
| Extensibility | Easier for LLM/MCP workflows and internal automation scripts. | Better if the company wants a Go-native OOXML engine and can invest engineering time. |
| Project posture | README says stable but with zero support/issue tracking, so treat as a useful prototype/toolkit rather than a supported product. | README says in-development and slowly being developed against ECMA-376. |

## Open-source health check

I refreshed both upstream checkouts and queried GitHub on 2026-07-07. The figures below are a point-in-time signal, not a long-term trend.

| Signal | python-office-mcp-server | go-ooxml | Interpretation |
| --- | --- | --- | --- |
| First commit | 2026-03-12 | 2026-01-29 | Both are young projects. |
| Latest commit checked | 2026-07-07 | 2026-02-13 | Python repo is more recently active; Go repo looked dormant since February in the checked branch. |
| First-to-last commit timespan | ~3.8 months | ~0.5 months | Neither has a long maintenance history yet. |
| Commits in last 12 months | 42 | 66 | Go had more burst commits, but concentrated in a short early window. |
| Average commits/month over last 12 months | 3.5 | 5.5 | This flat average hides the burst/dormancy pattern, especially for Go. |
| Different authors | 5 | 1 | Python shows broader authorship metadata; Go is single-author in the local git history. |
| GitHub stars | 24 | 15 | Both have low public adoption signals. |
| Forks | 5 | 1 | Python has slightly more external interest. |
| PRs | 0 total / 0 open | 0 total / 0 open | No visible PR review/community workflow in either repo. |
| License | No GitHub-detected license | MIT | `go-ooxml` is easier to approve legally; Python needs license clarification before business use. |
| Commercial backing/offering | None found | None found | No commercial offering means no obvious vendor lock-in, but also no support SLA or procurement path. |

Health verdict: **neither project has mature open-source governance signals**. `python-office-mcp-server` looks more recently active and has more contributors/stars/forks, but its missing detected license and README statement about zero support are material risks. `go-ooxml` has a clean MIT license, but its short development burst, single-author history, and lack of recent commits make it risky as a business-critical dependency without internal ownership.

The raw probe output is captured in `oss_health.json`.

## Local LLM + user workflow test

I also tested the more realistic workflow where a user asks a local LLM to work on a `.docx` or `.xlsx`, and the LLM needs a tool layer for reading, reasoning, and making edits. The `llm_workflow_probe.py` script models the tool side of that agent loop without calling an LLM.

The simulated tasks were:

1. Read both Python-created and Go-created DOCX/XLSX files into LLM-friendly context.
2. Preserve enough structure for a model to answer business questions about P&L performance and risks.
3. Inspect document structure/sheets.
4. Read formulas where possible.
5. Perform a small review edit and add an Excel comment.

### Results

`python-office-mcp-server` is clearly better for local LLM orchestration:

- It returns Markdown previews for both DOCX and XLSX, which are directly usable in a local model prompt.
- It returns JSON/structure for document sections and workbook sheets.
- It can expose formulas with `include_formulas=True`, which matters for financial-review tasks.
- It can perform an agent-style edit (`office_patch`) and add a review comment (`office_comment`) without writing a custom parser/editor.
- Its tool names and diagnostics are already shaped like an MCP tool contract, so a local LLM can be instructed to call stable operations such as `office_read`, `office_inspect`, `office_patch`, and `office_comment`.

`go-ooxml` can serve a local LLM only if the team builds the missing agent layer around it:

- It can open and traverse DOCX/XLSX files, as shown by `go_analyze.go`.
- It does not provide an out-of-the-box MCP server, JSON/Markdown extraction contract, or LLM-oriented workflow guidance.
- Every LLM action needs custom Go code: summarize tables, expose formulas, patch cells, add comments, preserve formatting, validate edits, and report diagnostics.
- This may be acceptable for a Go platform team building a controlled internal document service, but it is not the faster path for a user-facing local LLM assistant.

Local-LLM verdict: **choose `python-office-mcp-server` unless the product requirement is specifically to build a Go-native Office document engine**. For a user saying “analyze this customer spreadsheet and update the Word report,” the Python MCP tool surface is much closer to what an LLM agent needs.

The raw local-LLM probe output is captured in `llm_probe_results.json`.

## Recommendation

For a tech-company sales and PM team that needs to create and analyze lots of `.docx` and `.xlsx` files, **`python-office-mcp-server` is the better basis point today**.

Reasons:

1. It is easier to use at the workflow level. The unified tools (`office_read`, `office_inspect`, `office_patch`, `office_table`, `office_template`, `office_audit`) map directly to business-document tasks.
2. It analyzes incoming documents more usefully. JSON and Markdown outputs are immediately consumable by automation, review bots, and LLM agents.
3. It creates richer Office artifacts faster because it leans on mature Python libraries.
4. It is better suited for mixed create/analyze workloads rather than pure OOXML library development.

`go-ooxml` is worth tracking or using selectively if the company needs a Go-native OOXML library, lower-level control, or wants to build a new supported engine. But based on this practical test, it is **less mature and less ergonomic** for the requested sales/PM automation use case today.

## Caveats

- I tested only `.docx` and `.xlsx`, not PowerPoint.
- I did not use Microsoft Word or Excel GUI repair validation.
- The Go spreadsheet test failure depended on missing fixture files in this environment.
- The Python project's README explicitly frames it as stable but not actively supported, which is a governance risk for production adoption.
- The probe scripts (`analyze_cross.py`, `llm_workflow_probe.py`) and `go.mod` reference the tool checkouts at `/tmp/office-mcp-ooxml-work/`. They are not self-contained: to re-run them, clone `rcarmo/python-office-mcp-server` and `rcarmo/go-ooxml` to that path first, then install the Python package in a venv. The committed JSON/text output files capture the results of each run.
