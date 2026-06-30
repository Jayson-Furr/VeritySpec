from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from .versions import CURRENT_SPEC_VERSION


WORKSPACE_FILE_NAMES = ("verityspec.json", "verity.json")
DEFAULT_RECORD_GLOBS = ["records/**/*.json"]
DEFAULT_PACKS = [
    "verity.core",
    "verity.pack.api",
    "verity.pack.cli",
    "verity.pack.events",
]


@dataclass(frozen=True)
class Record:
    data: dict[str, Any]
    path: Path
    index: Optional[int] = None

    @property
    def id(self) -> Optional[str]:
        value = self.data.get("id")
        return value if isinstance(value, str) else None

    @property
    def kind(self) -> Optional[str]:
        value = self.data.get("kind")
        return value if isinstance(value, str) else None

    @property
    def location(self) -> str:
        if self.index is None:
            return str(self.path)
        return f"{self.path}#records/{self.index}"


@dataclass(frozen=True)
class Workspace:
    base_path: Path
    config_path: Optional[Path]
    config: dict[str, Any]
    records: list[Record]

    @property
    def pack_ids(self) -> list[str]:
        packs = self.config.get("packs", DEFAULT_PACKS)
        if not isinstance(packs, list):
            return DEFAULT_PACKS
        return [pack for pack in packs if isinstance(pack, str)]

    @property
    def pack_paths(self) -> list[str]:
        paths = self.config.get("packPaths", [])
        if not isinstance(paths, list):
            return []
        return [path for path in paths if isinstance(path, str)]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def find_workspace_file(path: Path) -> Optional[Path]:
    for name in WORKSPACE_FILE_NAMES:
        candidate = path / name
        if candidate.exists():
            return candidate
    return None


def default_config(base_path: Path) -> dict[str, Any]:
    return {
        "workspace": base_path.name,
        "specVersion": CURRENT_SPEC_VERSION,
        "packs": DEFAULT_PACKS,
        "records": DEFAULT_RECORD_GLOBS,
    }


def load_workspace(path: str | Path) -> Workspace:
    requested = Path(path).resolve()
    if requested.is_file():
        if requested.name in WORKSPACE_FILE_NAMES:
            config_path = requested
            base_path = requested.parent
            config = load_json(config_path)
        else:
            config_path = None
            base_path = requested.parent
            config = default_config(base_path)
            config["records"] = [requested.name]
    else:
        base_path = requested
        config_path = find_workspace_file(base_path)
        config = load_json(config_path) if config_path else default_config(base_path)

    records = load_records(base_path, config)
    return Workspace(base_path=base_path, config_path=config_path, config=config, records=records)


def load_records(base_path: Path, config: dict[str, Any]) -> list[Record]:
    patterns = config.get("records", DEFAULT_RECORD_GLOBS)
    if not isinstance(patterns, list):
        patterns = DEFAULT_RECORD_GLOBS

    record_paths: list[Path] = []
    for pattern in patterns:
        if not isinstance(pattern, str):
            continue
        for path in sorted(base_path.glob(pattern)):
            if path.is_file() and path.name not in WORKSPACE_FILE_NAMES:
                record_paths.append(path)

    unique_paths = list(dict.fromkeys(record_paths))
    records: list[Record] = []
    for path in unique_paths:
        payload = load_json(path)
        if isinstance(payload, dict) and isinstance(payload.get("records"), list):
            for index, item in enumerate(payload["records"]):
                if isinstance(item, dict):
                    records.append(Record(item, path, index=index))
        elif isinstance(payload, list):
            for index, item in enumerate(payload):
                if isinstance(item, dict):
                    records.append(Record(item, path, index=index))
        elif isinstance(payload, dict):
            records.append(Record(payload, path))
    return records
