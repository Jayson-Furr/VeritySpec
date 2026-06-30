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


def issue_count(issues: Iterable[Issue], severity: str) -> int:
    return sum(1 for issue in issues if issue.severity == severity)


def has_errors(issues: Iterable[Issue]) -> bool:
    return any(issue.severity == "error" for issue in issues)


def apply_strict(issues: Iterable[Issue]) -> list[Issue]:
    return [
        Issue("error", issue.code, issue.message, issue.location, issue.record_id)
        if issue.severity == "warning"
        else issue
        for issue in issues
    ]


def print_issues(issues: Iterable[Issue], out: TextIO) -> None:
    for issue in issues:
        print(issue.format(), file=out)

