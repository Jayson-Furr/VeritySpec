from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, TextIO


def parse_field_path(value: str | None) -> list[str | int]:
    if not value:
        return []

    parts: list[str | int] = []
    token = ""
    index_token = ""
    in_index = False

    for char in value:
        if in_index:
            if char == "]":
                if index_token.isdigit():
                    parts.append(int(index_token))
                elif index_token:
                    parts.append(index_token)
                index_token = ""
                in_index = False
            else:
                index_token += char
            continue

        if char == ".":
            if token:
                parts.append(token)
                token = ""
            continue
        if char == "[":
            if token:
                parts.append(token)
                token = ""
            in_index = True
            continue
        token += char

    if token:
        parts.append(token)
    if index_token:
        parts.append(index_token)
    return parts


def json_pointer(parts: list[str | int]) -> str | None:
    if not parts:
        return None
    escaped = [str(part).replace("~", "~0").replace("/", "~1") for part in parts]
    return "/" + "/".join(escaped)


def parse_issue_location(location: str | None) -> dict[str, object] | None:
    if not location:
        return None

    base_location = location
    field_path = None
    last_colon = location.rfind(":")
    last_separator = max(location.rfind("/"), location.rfind("\\"))
    if last_colon > last_separator:
        base_location, field_path = location.rsplit(":", 1)

    path = base_location
    fragment = None
    record_index = None
    if "#" in base_location:
        path, fragment = base_location.split("#", 1)
        if fragment.startswith("records/"):
            maybe_index = fragment.removeprefix("records/")
            if maybe_index.isdigit():
                record_index = int(maybe_index)

    details: dict[str, object] = {"path": path}
    if fragment:
        details["fragment"] = fragment
    if record_index is not None:
        details["recordIndex"] = record_index
    if field_path:
        parts = parse_field_path(field_path)
        details["fieldPath"] = field_path
        if parts:
            details["fieldParts"] = parts
            pointer = json_pointer(parts)
            if pointer:
                details["jsonPointer"] = pointer
    return details


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    message: str
    location: Optional[str] = None
    record_id: Optional[str] = None

    def to_dict(self) -> dict:
        data = {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
        }
        if self.location:
            data["location"] = self.location
            details = parse_issue_location(self.location)
            if details:
                data["locationDetails"] = details
        if self.record_id:
            data["recordId"] = self.record_id
        return data

    def format(self) -> str:
        parts = [self.severity.upper(), self.code]
        if self.record_id:
            parts.append(self.record_id)
        if self.location:
            parts.append(self.location)
        return f"{' '.join(parts)}: {self.message}"


def format_issue_path(path: Iterable[object] | str | None) -> str:
    if path is None:
        return ""
    if isinstance(path, str):
        return path

    result = ""
    for part in path:
        if isinstance(part, int):
            result = f"{result}[{part}]"
        elif result:
            result = f"{result}.{part}"
        else:
            result = str(part)
    return result


def location_at(base_location: str | None, path: Iterable[object] | str | None) -> str | None:
    formatted = format_issue_path(path)
    if not formatted:
        return base_location
    if not base_location:
        return formatted
    return f"{base_location}:{formatted}"


def issue_count(issues: Iterable[Issue], severity: str) -> int:
    return sum(1 for issue in issues if issue.severity == severity)


def warning_count(issues: Iterable[Issue]) -> int:
    return issue_count(issues, "warning")


def has_errors(issues: Iterable[Issue]) -> bool:
    return any(issue.severity == "error" for issue in issues)


def should_fail(issues: Iterable[Issue], fail_on: str = "error") -> bool:
    materialized = list(issues)
    if fail_on == "warning":
        return any(issue.severity in {"error", "warning"} for issue in materialized)
    return has_errors(materialized)


def apply_strict(issues: Iterable[Issue]) -> list[Issue]:
    return [
        Issue("error", issue.code, issue.message, issue.location, issue.record_id)
        if issue.severity == "warning"
        else issue
        for issue in issues
    ]


def dedupe_issues(issues: Iterable[Issue]) -> list[Issue]:
    seen: set[tuple[str, str, str, Optional[str], Optional[str]]] = set()
    result: list[Issue] = []
    for issue in issues:
        key = (issue.severity, issue.code, issue.message, issue.location, issue.record_id)
        if key in seen:
            continue
        seen.add(key)
        result.append(issue)
    return result


def print_issues(issues: Iterable[Issue], out: TextIO) -> None:
    for issue in issues:
        print(issue.format(), file=out)
