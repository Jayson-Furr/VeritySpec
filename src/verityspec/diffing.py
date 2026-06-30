from __future__ import annotations

import json
from typing import Any

from .workspace import Workspace


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def diff_workspaces(old: Workspace, new: Workspace) -> dict:
    old_by_id = {record.id: record.data for record in old.records if record.id}
    new_by_id = {record.id: record.data for record in new.records if record.id}

    old_ids = set(old_by_id)
    new_ids = set(new_by_id)

    changed = []
    for record_id in sorted(old_ids & new_ids):
        if canonical_json(old_by_id[record_id]) != canonical_json(new_by_id[record_id]):
            changed.append(record_id)

    return {
        "versions": {
            "old": old.config.get("specVersion"),
            "new": new.config.get("specVersion"),
            "changed": old.config.get("specVersion") != new.config.get("specVersion"),
        },
        "packs": {
            "added": sorted(set(new.pack_ids) - set(old.pack_ids)),
            "removed": sorted(set(old.pack_ids) - set(new.pack_ids)),
        },
        "added": sorted(new_ids - old_ids),
        "removed": sorted(old_ids - new_ids),
        "changed": changed,
    }


def diff_to_text(diff: dict) -> str:
    lines = [
        f"Spec version: {diff.get('versions', {}).get('old')} -> {diff.get('versions', {}).get('new')}",
        "Packs added:",
    ]
    lines.extend(f"  {item}" for item in diff.get("packs", {}).get("added", []))
    lines.append("Packs removed:")
    lines.extend(f"  {item}" for item in diff.get("packs", {}).get("removed", []))
    lines.append("Added:")
    lines.extend(f"  {item}" for item in diff["added"])
    lines.append("Removed:")
    lines.extend(f"  {item}" for item in diff["removed"])
    lines.append("Changed:")
    lines.extend(f"  {item}" for item in diff["changed"])
    return "\n".join(lines)
