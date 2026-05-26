from __future__ import annotations

from collections import Counter
from html import escape

from salt.models import Violation


def render_html(violations: list[Violation]) -> str:
    severity_counts = Counter(violation.severity for violation in violations)
    file_sections = "\n".join(
        _render_file_section(file, file_violations)
        for file, file_violations in _group_by_file(violations).items()
    )
    if not file_sections:
        file_sections = '<div class="empty">No violations found</div>'

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SALT Lint Report</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f8fb;
      --panel: #ffffff;
      --text: #17202a;
      --muted: #617084;
      --border: #d8dee8;
      --error: #b42318;
      --warning: #a15c07;
      --info: #175cd3;
    }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font: 14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 32px 20px;
    }}
    h1 {{
      margin: 0 0 6px;
      font-size: 28px;
      font-weight: 700;
    }}
    .summary {{
      color: var(--muted);
      margin-bottom: 22px;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 12px;
      margin-bottom: 24px;
    }}
    .stat {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px 16px;
    }}
    .stat strong {{
      display: block;
      font-size: 24px;
      line-height: 1.1;
    }}
    .files {{
      display: grid;
      gap: 12px;
    }}
    details {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
    }}
    summary {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 14px 16px;
      cursor: pointer;
      font-weight: 700;
    }}
    summary::marker {{
      color: var(--muted);
    }}
    .file-meta {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: flex-end;
      color: var(--muted);
      font-weight: 600;
      font-size: 12px;
    }}
    .badge {{
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 2px 8px;
      background: #f8fafc;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      border-top: 1px solid var(--border);
    }}
    th, td {{
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #eef2f7;
      font-size: 12px;
      text-transform: uppercase;
      color: var(--muted);
      letter-spacing: .04em;
    }}
    tr:last-child td {{
      border-bottom: 0;
    }}
    code {{
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 12px;
    }}
    .severity-error {{ color: var(--error); font-weight: 700; }}
    .severity-warning {{ color: var(--warning); font-weight: 700; }}
    .severity-info {{ color: var(--info); font-weight: 700; }}
    .empty {{
      color: var(--muted);
      text-align: center;
      padding: 36px 12px;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
    }}
  </style>
</head>
<body>
  <main>
    <h1>SALT Lint Report</h1>
    <div class="summary">{len(violations)} violation(s) found</div>
    <section class="stats" aria-label="Violation summary">
      <div class="stat"><strong>{len(violations)}</strong>Total</div>
      <div class="stat"><strong>{severity_counts.get("error", 0)}</strong>Errors</div>
      <div class="stat"><strong>{severity_counts.get("warning", 0)}</strong>Warnings</div>
      <div class="stat"><strong>{severity_counts.get("info", 0)}</strong>Info</div>
    </section>
    <section class="files" aria-label="Violations by file">
{file_sections}
    </section>
  </main>
</body>
</html>"""


def _group_by_file(violations: list[Violation]) -> dict[str, list[Violation]]:
    grouped: dict[str, list[Violation]] = {}
    for violation in violations:
        grouped.setdefault(violation.file, []).append(violation)
    return grouped


def _render_file_section(file: str, violations: list[Violation]) -> str:
    counts = Counter(violation.severity for violation in violations)
    rows = "\n".join(_render_row(violation) for violation in violations)
    return f"""      <details>
        <summary>
          <code>{escape(file)}</code>
          <span class="file-meta">
            <span class="badge">{len(violations)} total</span>
            <span class="badge severity-error">{counts.get("error", 0)} errors</span>
            <span class="badge severity-warning">{counts.get("warning", 0)} warnings</span>
            <span class="badge severity-info">{counts.get("info", 0)} info</span>
          </span>
        </summary>
        <table>
          <thead>
            <tr>
              <th>Line</th>
              <th>Column</th>
              <th>Severity</th>
              <th>Rule</th>
              <th>Name</th>
              <th>Message</th>
            </tr>
          </thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </details>"""


def _render_row(violation: Violation) -> str:
    severity = escape(violation.severity)
    return (
        "            <tr>"
        f"<td>{violation.line}</td>"
        f"<td>{violation.column}</td>"
        f'<td class="severity-{severity}">{severity}</td>'
        f"<td><code>{escape(violation.rule_id)}</code></td>"
        f"<td>{escape(violation.rule_name)}</td>"
        f"<td>{escape(violation.message)}</td>"
        "</tr>"
    )
