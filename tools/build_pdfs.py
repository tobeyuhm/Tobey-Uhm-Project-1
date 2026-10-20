"""Render the three Brightspace PDFs from the repository Markdown (content-equivalent copies).

    pip install markdown        # documentation tool only
    python tools/build_pdfs.py  # needs Microsoft Edge (Windows) or set BROWSER to a Chrome/Edge path

Writes docs/Research-Evolution.pdf, docs/Decision-Memo.pdf, docs/Validation-and-AI-Use.pdf.
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BROWSER = os.environ.get("BROWSER", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
JOBS = {
    "research-evolution.md": "Research-Evolution.pdf",
    "decision-memo.md": "Decision-Memo.pdf",
    "validation-and-ai-use.md": "Validation-and-AI-Use.pdf",
}
CSS = """
@page { size: Letter; margin: 0.55in; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 9.6pt; line-height: 1.32; color: #111; }
h1 { font-size: 15pt; margin: 0 0 6pt; } h2 { font-size: 12pt; margin: 10pt 0 4pt; } h3 { font-size: 10.5pt; margin: 8pt 0 3pt; }
table { border-collapse: collapse; width: 100%; margin: 4pt 0 6pt; font-size: 8.3pt; page-break-inside: auto; }
th, td { border: 1px solid #999; padding: 2pt 4pt; vertical-align: top; } th { background: #eee; }
code, pre { font-family: Consolas, monospace; font-size: 8.3pt; } pre { background: #f5f5f5; padding: 4pt; white-space: pre-wrap; }
p, li { margin: 2pt 0; } hr { border: 0; border-top: 1px solid #bbb; margin: 8pt 0; }
"""


def main() -> None:
    for src, dst in JOBS.items():
        text = (DOCS / src).read_text(encoding="utf-8")
        body = markdown.markdown(text, extensions=["tables", "fenced_code"])
        html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as handle:
            handle.write(html)
            tmp = handle.name
        out = DOCS / dst
        subprocess.run([BROWSER, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={out}", Path(tmp).as_uri()], check=True, capture_output=True)
        os.unlink(tmp)
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
