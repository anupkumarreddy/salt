from __future__ import annotations

from salt.models import Violation
from salt.reporters.html_reporter import render_html


def test_html_report_groups_violations_by_collapsible_file() -> None:
    html = render_html(
        [
            Violation("SV001", "no_casex", "rtl/a.sv", 10, 3, "Usage of 'casex' is not allowed", "error"),
            Violation("SV002", "case_default", "rtl/a.sv", 12, 5, "case missing default", "warning"),
            Violation("STYLE001", "no_tabs", "rtl/b.sv", 1, 1, "Tab found", "warning"),
        ]
    )

    assert html.count("<details>") == 2
    assert "<code>rtl/a.sv</code>" in html
    assert "<code>rtl/b.sv</code>" in html
    assert '<span class="badge">2 total</span>' in html
    assert "<th>File</th>" not in html
    assert "Usage of &#x27;casex&#x27; is not allowed" in html
