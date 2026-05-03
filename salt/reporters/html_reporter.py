from __future__ import annotations

from collections import Counter
from html import escape

from salt.models import Violation


def render_html(violations: list[Violation]) -> str:
    severity_counts = Counter(violation.severity for violation in violations)
    rows = "\n".join(_render_row(violation) for violation in violations)
    if not rows:
        rows = '<tr><td colspan="7" class="empty">No violations found</td></tr>'

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
    table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
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
    <table>
      <thead>
        <tr>
          <th>File</th>
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
  </main>
</body>
</html>"""


def _render_row(violation: Violation) -> str:
    severity = escape(violation.severity)
    return (
        "        <tr>"
        f"<td><code>{escape(violation.file)}</code></td>"
        f"<td>{violation.line}</td>"
        f"<td>{violation.column}</td>"
        f'<td class="severity-{severity}">{severity}</td>'
        f"<td><code>{escape(violation.rule_id)}</code></td>"
        f"<td>{escape(violation.rule_name)}</td>"
        f"<td>{escape(violation.message)}</td>"
        "</tr>"
    )
