from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, TextIO


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
