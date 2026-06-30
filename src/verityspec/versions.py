from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .issues import Issue

if TYPE_CHECKING:
    from .workspace import Workspace


CURRENT_SPEC_VERSION = "v0.1.0"
VERSION_PATTERN = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")


@dataclass(frozen=True)
class SpecVersion:
    id: str
    status: str
    description: str


SUPPORTED_SPEC_VERSIONS: dict[str, SpecVersion] = {
    CURRENT_SPEC_VERSION: SpecVersion(
        id=CURRENT_SPEC_VERSION,
        status="current",
        description="Initial executable VeritySpec workspace format.",
    )
}


def normalize_spec_version(value: object) -> Optional[str]:
    if not isinstance(value, str):
        return None
    match = VERSION_PATTERN.match(value.strip())
    if not match:
        return None
    major, minor, patch = match.groups()
    return f"v{int(major)}.{int(minor)}.{int(patch)}"


def parse_spec_version(value: object) -> Optional[tuple[int, int, int]]:
    normalized = normalize_spec_version(value)
    if normalized is None:
        return None
    major, minor, patch = normalized[1:].split(".")
    return int(major), int(minor), int(patch)


def compare_spec_versions(left: str, right: str) -> int:
    left_parts = parse_spec_version(left)
    right_parts = parse_spec_version(right)
    if left_parts is None or right_parts is None:
        raise ValueError("Cannot compare invalid VeritySpec versions.")
    if left_parts < right_parts:
        return -1
    if left_parts > right_parts:
        return 1
    return 0


def classify_spec_version(value: object) -> str:
    if value is None:
        return "missing"
    normalized = normalize_spec_version(value)
    if normalized is None:
        return "invalid"
    if normalized in SUPPORTED_SPEC_VERSIONS:
        return "supported"
    if compare_spec_versions(normalized, CURRENT_SPEC_VERSION) > 0:
        return "future"
    return "unsupported"


def validate_workspace_version(workspace: Workspace) -> list[Issue]:
    value = workspace.config.get("specVersion")
    classification = classify_spec_version(value)
    location = str(workspace.config_path or workspace.base_path)

    if classification == "supported":
        return []
    if classification == "missing":
        return [
            Issue(
                "error",
                "workspace.version.missing",
                f"Workspace is missing specVersion. Current supported version is {CURRENT_SPEC_VERSION}.",
                location,
            )
        ]
    if classification == "invalid":
        return [
            Issue(
                "error",
                "workspace.version.invalid",
                f"Workspace specVersion must use vMAJOR.MINOR.PATCH format. Current supported version is {CURRENT_SPEC_VERSION}.",
                location,
            )
        ]
    if classification == "future":
        return [
            Issue(
                "error",
                "workspace.version.future",
                (
                    f"Workspace specVersion '{value}' is newer than this VeritySpec release supports. "
                    f"Install a newer VeritySpec CLI or migrate the workspace intentionally."
                ),
                location,
            )
        ]
    return [
        Issue(
            "error",
            "workspace.version.unsupported",
            (
                f"Workspace specVersion '{value}' is not supported by this VeritySpec release. "
                f"Run `verity migrate` to produce a {CURRENT_SPEC_VERSION} workspace."
            ),
            location,
        )
    ]
