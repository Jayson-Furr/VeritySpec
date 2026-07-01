from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .issues import Issue
from .workspace import Record, Workspace, load_workspace


DEPENDENCY_ALIAS_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
DEPENDENCY_REFERENCE_SEPARATOR = "::"


@dataclass(frozen=True)
class WorkspaceDependencyDeclaration:
    id: str
    alias: str
    source: str
    mode: str
    version: str | None
    index: int

    @property
    def field_path(self) -> str:
        return f"dependencies[{self.index}]"


@dataclass(frozen=True)
class ResolvedWorkspaceDependency:
    declaration: WorkspaceDependencyDeclaration
    workspace: Workspace
    records_by_id: dict[str, Record]
    exported_ids: set[str]

    def qualified_id(self, record_id: str) -> str:
        return f"{self.declaration.alias}{DEPENDENCY_REFERENCE_SEPARATOR}{record_id}"


@dataclass(frozen=True)
class WorkspaceDependencyResolution:
    dependencies: list[ResolvedWorkspaceDependency]
    declared_aliases: set[str]
    issues: list[Issue]

    @property
    def by_alias(self) -> dict[str, ResolvedWorkspaceDependency]:
        return {item.declaration.alias: item for item in self.dependencies}


def split_dependency_reference(target: str) -> tuple[str, str] | None:
    if DEPENDENCY_REFERENCE_SEPARATOR not in target:
        return None
    alias, record_id = target.split(DEPENDENCY_REFERENCE_SEPARATOR, 1)
    if not alias or not record_id:
        return None
    return alias, record_id


def workspace_config_location(workspace: Workspace, field_path: str | None = None) -> str:
    base = str(workspace.config_path or workspace.base_path)
    if field_path:
        return f"{base}:{field_path}"
    return base


def parse_workspace_dependency_declarations(
    workspace: Workspace,
) -> tuple[list[WorkspaceDependencyDeclaration], list[Issue]]:
    raw_dependencies = workspace.config.get("dependencies", [])
    if "dependencies" not in workspace.config:
        return [], []

    if not isinstance(raw_dependencies, list):
        return [], [
            Issue(
                "error",
                "workspace.dependencies.invalid",
                "Workspace dependencies must be an array of dependency declarations.",
                workspace_config_location(workspace, "dependencies"),
            )
        ]

    declarations: list[WorkspaceDependencyDeclaration] = []
    issues: list[Issue] = []
    aliases: dict[str, str] = {}

    for index, item in enumerate(raw_dependencies):
        location = workspace_config_location(workspace, f"dependencies[{index}]")
        if not isinstance(item, dict):
            issues.append(
                Issue(
                    "error",
                    "dependency.declaration.invalid",
                    "Workspace dependency declarations must be objects.",
                    location,
                )
            )
            continue

        dependency_id = item.get("id")
        alias = item.get("alias")
        source = item.get("source")
        mode = item.get("mode", "readonly")
        version = item.get("version")

        if not isinstance(dependency_id, str) or not dependency_id:
            issues.append(
                Issue(
                    "error",
                    "dependency.declaration.invalid",
                    "Workspace dependency declarations must include a non-empty string id.",
                    workspace_config_location(workspace, f"dependencies[{index}].id"),
                )
            )
            continue
        if not isinstance(alias, str) or not DEPENDENCY_ALIAS_PATTERN.match(alias):
            issues.append(
                Issue(
                    "error",
                    "dependency.declaration.invalid",
                    (
                        "Workspace dependency aliases must be non-empty strings "
                        "using letters, numbers, underscores, or hyphens."
                    ),
                    workspace_config_location(workspace, f"dependencies[{index}].alias"),
                )
            )
            continue
        if alias in aliases:
            message = (
                f"Workspace dependency alias '{alias}' is already declared at "
                f"{aliases[alias]}."
            )
            issues.append(
                Issue(
                    "error",
                    "dependency.alias.duplicate",
                    message,
                    workspace_config_location(workspace, f"dependencies[{index}].alias"),
                )
            )
            continue
        aliases[alias] = workspace_config_location(workspace, f"dependencies[{index}].alias")

        if not isinstance(source, str) or not source:
            issues.append(
                Issue(
                    "error",
                    "dependency.declaration.invalid",
                    "Workspace dependency declarations must include a non-empty string source.",
                    workspace_config_location(workspace, f"dependencies[{index}].source"),
                )
            )
            continue
        if mode != "readonly":
            issues.append(
                Issue(
                    "error",
                    "dependency.mode.unsupported",
                    "Workspace dependencies currently support mode 'readonly' only.",
                    workspace_config_location(workspace, f"dependencies[{index}].mode"),
                )
            )
            continue
        if version is not None and not isinstance(version, str):
            issues.append(
                Issue(
                    "error",
                    "dependency.declaration.invalid",
                    "Workspace dependency version constraints must be strings when present.",
                    workspace_config_location(workspace, f"dependencies[{index}].version"),
                )
            )
            continue

        declarations.append(
            WorkspaceDependencyDeclaration(
                id=dependency_id,
                alias=alias,
                source=source,
                mode=mode,
                version=version,
                index=index,
            )
        )

    return declarations, issues


def exported_record_ids(workspace: Workspace) -> tuple[set[str], list[Issue]]:
    raw_exports = workspace.config.get("exports", [])
    if "exports" not in workspace.config:
        return set(), []
    if not isinstance(raw_exports, list) or not all(
        isinstance(item, str) for item in raw_exports
    ):
        return set(), [
            Issue(
                "error",
                "dependency.exports.invalid",
                "Dependency workspace exports must be an array of record ID strings.",
                workspace_config_location(workspace, "exports"),
            )
        ]
    return set(raw_exports), []


def resolve_source_path(workspace: Workspace, source: str) -> Path:
    source_path = Path(source)
    if source_path.is_absolute():
        return source_path
    return (workspace.base_path / source_path).resolve()


def parse_simple_version(value: str | None) -> tuple[int, int, int] | None:
    if not isinstance(value, str):
        return None
    match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)$", value.strip())
    if not match:
        return None
    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch)


def version_satisfies(resolved: str | None, constraint: str | None) -> bool:
    if constraint is None:
        return True
    if resolved is None:
        return False
    if constraint.startswith("^"):
        resolved_parts = parse_simple_version(resolved)
        constraint_parts = parse_simple_version(constraint[1:])
        if resolved_parts is None or constraint_parts is None:
            return resolved == constraint
        return (
            resolved_parts[0] == constraint_parts[0]
            and resolved_parts >= constraint_parts
        )
    return resolved.lstrip("v") == constraint.lstrip("v")


def resolve_workspace_dependencies(workspace: Workspace) -> WorkspaceDependencyResolution:
    declarations, issues = parse_workspace_dependency_declarations(workspace)
    declared_aliases = {declaration.alias for declaration in declarations}
    resolved: list[ResolvedWorkspaceDependency] = []

    for declaration in declarations:
        source_path = resolve_source_path(workspace, declaration.source)
        source_location = workspace_config_location(workspace, f"{declaration.field_path}.source")
        if not source_path.exists():
            issues.append(
                Issue(
                    "error",
                    "dependency.source.missing",
                    f"Workspace dependency source '{declaration.source}' does not exist.",
                    source_location,
                )
            )
            continue

        try:
            dependency_workspace = load_workspace(source_path)
        except Exception as exc:  # pragma: no cover - exact parser errors vary
            issues.append(
                Issue(
                    "error",
                    "dependency.load.failed",
                    f"Workspace dependency '{declaration.alias}' failed to load: {exc}",
                    source_location,
                )
            )
            continue

        actual_workspace_id = dependency_workspace.config.get("workspace")
        if actual_workspace_id != declaration.id:
            issues.append(
                Issue(
                    "error",
                    "dependency.id.mismatch",
                    (
                        f"Workspace dependency '{declaration.alias}' expected workspace "
                        f"'{declaration.id}' but loaded '{actual_workspace_id}'."
                    ),
                    workspace_config_location(workspace, f"{declaration.field_path}.id"),
                )
            )
            continue

        actual_version = dependency_workspace.config.get("version")
        if declaration.version is not None:
            if not isinstance(actual_version, str):
                message = (
                    f"Workspace dependency '{declaration.alias}' declares a version "
                    "constraint but the dependency workspace has no version."
                )
                issues.append(
                    Issue(
                        "error",
                        "dependency.version.missing",
                        message,
                        workspace_config_location(workspace, f"{declaration.field_path}.version"),
                    )
                )
                continue
            if not version_satisfies(actual_version, declaration.version):
                issues.append(
                    Issue(
                        "error",
                        "dependency.version.unsatisfied",
                        (
                            f"Workspace dependency '{declaration.alias}' requires version "
                            f"'{declaration.version}' but resolved '{actual_version}'."
                        ),
                        workspace_config_location(workspace, f"{declaration.field_path}.version"),
                    )
                )
                continue

        exports, export_issues = exported_record_ids(dependency_workspace)
        issues.extend(export_issues)
        records_by_id = {
            record.id: record
            for record in dependency_workspace.records
            if record.id
        }
        resolved.append(
            ResolvedWorkspaceDependency(
                declaration=declaration,
                workspace=dependency_workspace,
                records_by_id=records_by_id,
                exported_ids=exports,
            )
        )

    return WorkspaceDependencyResolution(
        dependencies=resolved,
        declared_aliases=declared_aliases,
        issues=issues,
    )
