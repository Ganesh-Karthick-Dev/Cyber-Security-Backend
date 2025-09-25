from __future__ import annotations

from typing import Any


class ReportGenerator:
    def generate_summary(self, scan_results: dict[str, Any], ai_findings: dict[str, Any]) -> str:
        parts: list[str] = []
        parts.append(f"Scan type: {scan_results.get('type')}")
        parts.append(f"Risk: {ai_findings.get('risk_level')}")
        parts.append(f"Summary: {ai_findings.get('summary')}")
        recs = ai_findings.get("recommendations") or []
        if recs:
            parts.append("Recommendations:")
            for r in recs:
                parts.append(f"- {r}")
        return "\n".join(parts)



