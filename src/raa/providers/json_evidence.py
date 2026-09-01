from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from raa.core.models import Evidence, EvidenceKind


def load_evidence(path: Path) -> tuple[Evidence, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Evidence JSON must contain a list of evidence objects.")
    return tuple(
        Evidence(
            evidence_id=item["evidence_id"],
            area=item["area"],
            summary=item["summary"],
            source_name=item["source_name"],
            source_url=item["source_url"],
            retrieved_at=datetime.fromisoformat(item["retrieved_at"].replace("Z", "+00:00")),
            kind=EvidenceKind(item.get("kind", EvidenceKind.FACT)),
            value=item.get("value"),
            unit=item.get("unit"),
        )
        for item in payload
    )

