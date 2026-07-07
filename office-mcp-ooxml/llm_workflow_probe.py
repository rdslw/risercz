"""Probe local-LLM-style workflows over the generated P&L artifacts.

This does not call an LLM. It models the tool side of an LLM agent loop:
1. read structured/markdown content from user-provided DOCX/XLSX,
2. extract the key business answer an LLM would need,
3. perform a small review edit/comment to an XLSX.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, "/tmp/office-mcp-ooxml-work/python-office-mcp-server")
from office_server import OfficeServer

BASE = Path(__file__).parent
ART = BASE / "artifacts"
OUT = BASE / "llm_probe_results.json"

server = OfficeServer()
results = {"python_office_mcp_server": {}, "go_ooxml": {}}

# Python MCP-style operations: one tool gives markdown/JSON for LLM context and can patch/comment.
for name in ["python_pl.docx", "python_pl.xlsx", "go_pl.docx", "go_pl.xlsx"]:
    path = ART / name
    entry = {}
    entry["markdown_preview"] = server.tool_office_read(str(path), output_format="markdown")[:1200]
    entry["structure"] = server.tool_office_inspect(str(path), what="structure")
    if name.endswith(".xlsx"):
        entry["formulas_preview"] = str(server.tool_office_read(str(path), output_format="json", include_formulas=True))[:1200]
    results["python_office_mcp_server"][name] = entry

patch_src = ART / "python_pl.xlsx"
patch_dst = ART / "llm_python_review.xlsx"
shutil.copy2(patch_src, patch_dst)
results["python_office_mcp_server"]["edit_test"] = {
    "patch": server.tool_office_patch(
        str(patch_dst),
        changes=[{"target": "B11", "value": "LLM review: prioritize Q3 attach-rate plan and cloud cost guardrails."}],
        output_path=str(patch_dst),
        mode="best_effort",
    ),
    "comment": server.tool_office_comment(
        str(patch_dst),
        operation="add",
        target="F9",
        text="LLM review: confirm EBITDA formula after pipeline refresh.",
        author="local-llm-probe",
        output_path=str(patch_dst),
    ),
}

# Go-side local LLM workflow result is produced by go_analyze.go; store a concise interpretation here.
go_text = (BASE / "go_ooxml_analysis.txt").read_text()
results["go_ooxml"]["summary"] = {
    "probe_output": go_text,
    "llm_tooling_implication": (
        "Go can open and traverse DOCX/XLSX, but the agent must supply custom code "
        "for every extraction, summary, edit, and formatting operation; no MCP/JSON/Markdown "
        "tool contract is available out of the box."
    ),
}

OUT.write_text(json.dumps(results, indent=2, default=str) + "\n")
print(json.dumps(results, indent=2, default=str)[:6000])
