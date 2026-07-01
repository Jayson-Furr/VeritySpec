from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Callable

from . import __version__
from .diffing import diff_to_text, diff_workspaces
from .explain import ISSUE_EXPLANATIONS, explain_issue
from .generators import (
    generate_accessibility_report,
    generate_asyncapi,
    generate_cli_reference,
    generate_compliance_matrix,
    generate_coverage_dashboard,
    generate_deployment_report,
    generate_evidence_report,
    generate_openapi,
    generate_observability_report,
    generate_pack_capability_index,
    generate_product_impact_report,
    generate_python_models,
    generate_roadmap_report,
    generate_schema_bundle,
    generate_security_report,
    generate_typescript,
    generate_validation_report,
    generated_at_value,
    write_generated,
)
from .graph import build_graph, graph_to_text
from .importers.prismspec import import_prismspec
from .issues import (
    dedupe_issues,
    has_errors,
    issue_count,
    print_github_annotations,
    print_issues,
    should_fail,
)
from .migrations import (
    migrate_workspace,
    migration_capabilities,
    migration_capabilities_to_text,
    migration_report_to_text,
)
from .pack_validation import list_pack_summaries, validate_packs
from .packs import load_pack_registry
from .profiles import PROFILE_CHOICES, profile_issues, resolve_profile
from .readiness import evaluate_readiness
from .validation import lint_workspace, validate_workspace
from .versions import CURRENT_SPEC_VERSION
from .workspace import DEFAULT_PACKS, load_workspace


EXIT_SUCCESS = 0
EXIT_CONTRACT_FAILED = 1
EXIT_USAGE_ERROR = 2
EXIT_INTERNAL_ERROR = 3
PACK_ID_PATTERN = re.compile(r"^verity(?:\.pack)?\.[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
KIND_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
INIT_TEMPLATE_CHOICES = ("basic", "api", "cli", "events", "security")


def load_context(path: str, pack_paths: list[str] | None = None):
    workspace = load_workspace(path)
    cli_pack_paths = [str(Path(pack_path).resolve()) for pack_path in pack_paths or []]
    external_paths = workspace.pack_paths + cli_pack_paths
    registry = load_pack_registry(workspace.pack_ids, external_paths, workspace.base_path)
    return workspace, registry


def issue_exit(issues) -> int:
    return EXIT_CONTRACT_FAILED if should_fail(issues) else EXIT_SUCCESS


def issue_exit_with_fail_on(issues, fail_on: str) -> int:
    return EXIT_CONTRACT_FAILED if should_fail(issues, fail_on) else EXIT_SUCCESS


def print_issue_summary(label: str, issues) -> None:
    errors = issue_count(issues, "error")
    warnings = issue_count(issues, "warning")
    if errors == 0 and warnings == 0:
        print(f"{label} passed.")
    else:
        print(f"{label} completed with {errors} error(s), {warnings} warning(s).")


def issue_result(command_name: str, issues, profile: dict | None = None) -> dict:
    errors = issue_count(issues, "error")
    warnings = issue_count(issues, "warning")
    result = {
        "command": command_name,
        "passed": errors == 0,
        "summary": {
            "errors": errors,
            "warnings": warnings,
            "issues": errors + warnings,
        },
        "issues": [issue.to_dict() for issue in issues],
    }
    if profile is not None:
        result["profile"] = profile
    return result


def print_issue_result(
    label: str,
    command_name: str,
    issues,
    output_format: str,
    profile: dict | None = None,
) -> None:
    if output_format == "json":
        print(json.dumps(issue_result(command_name, issues, profile), indent=2))
        return
    print_issues(issues, sys.stdout)
    print_issue_summary(label, issues)


def maybe_print_github_annotations(args: argparse.Namespace, issues) -> None:
    if getattr(args, "github_annotations", False):
        print_github_annotations(issues, sys.stderr)


def init_product(name: str, owner: str, references: list[dict] | None = None) -> dict:
    return {
        "id": "product.example",
        "kind": "product",
        "name": name,
        "description": "A starter VeritySpec product contract.",
        "status": "ready",
        "owner": owner,
        "version": "0.1.0",
        "references": references or [],
    }


def init_schema_object(record_id: str, name: str, owner: str, json_schema: dict) -> dict:
    return {
        "id": record_id,
        "kind": "schema.object",
        "name": name,
        "description": f"{name} schema.",
        "status": "ready",
        "owner": owner,
        "jsonSchema": json_schema,
        "references": [],
    }


def starter_list_schema(property_name: str, item_required: list[str], item_properties: dict) -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [property_name],
        "properties": {
            property_name: {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": item_required,
                    "properties": item_properties,
                },
            }
        },
    }


def init_template(template: str, name: str, owner: str) -> tuple[list[str], dict[str, dict]]:
    if template == "api":
        return (
            ["verity.core", "verity.pack.api"],
            {
                "product.json": init_product(
                    name,
                    owner,
                    [{"type": "exposes", "target": "api.example.list"}],
                ),
                "schema.example-list.json": init_schema_object(
                    "schema.example_list",
                    "Example List",
                    owner,
                    starter_list_schema(
                        "items",
                        ["id", "name"],
                        {"id": {"type": "string"}, "name": {"type": "string"}},
                    ),
                ),
                "api.example-list.json": {
                    "id": "api.example.list",
                    "kind": "api.endpoint",
                    "name": "List Examples",
                    "description": "Lists example resources.",
                    "status": "ready",
                    "owner": owner,
                    "method": "GET",
                    "path": "/examples",
                    "summary": "List example resources.",
                    "responses": [
                        {
                            "statusCode": 200,
                            "description": "Example resources returned.",
                            "schema": "schema.example_list",
                        }
                    ],
                    "references": [],
                },
            },
        )
    if template == "cli":
        return (
            ["verity.core", "verity.pack.cli"],
            {
                "product.json": init_product(
                    name,
                    owner,
                    [{"type": "ships", "target": "cli.example.list"}],
                ),
                "schema.example-list.json": init_schema_object(
                    "schema.example_list",
                    "Example List",
                    owner,
                    starter_list_schema(
                        "items",
                        ["id", "name"],
                        {"id": {"type": "string"}, "name": {"type": "string"}},
                    ),
                ),
                "cli.example-list.json": {
                    "id": "cli.example.list",
                    "kind": "cli.command",
                    "name": "List Examples",
                    "description": "Lists example resources.",
                    "status": "ready",
                    "owner": owner,
                    "command": "example list",
                    "options": [
                        {
                            "name": "--json",
                            "type": "boolean",
                            "description": "Emit JSON output.",
                        }
                    ],
                    "outputSchema": "schema.example_list",
                    "exitCodes": [
                        {"code": 0, "description": "Examples were listed."},
                        {"code": 1, "description": "The command failed."},
                    ],
                    "references": [],
                },
            },
        )
    if template == "events":
        return (
            ["verity.core", "verity.pack.events"],
            {
                "product.json": init_product(
                    name,
                    owner,
                    [{"type": "emits", "target": "event.example.created"}],
                ),
                "schema.example.json": init_schema_object(
                    "schema.example",
                    "Example Event",
                    owner,
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["id", "createdAt"],
                        "properties": {
                            "id": {"type": "string"},
                            "createdAt": {"type": "string", "format": "date-time"},
                        },
                    },
                ),
                "event.example-created.json": {
                    "id": "event.example.created",
                    "kind": "event.message",
                    "name": "Example Created",
                    "description": "Published after an example resource is created.",
                    "status": "ready",
                    "owner": owner,
                    "topic": "example.created",
                    "payloadSchema": "schema.example",
                    "references": [],
                },
            },
        )
    if template == "security":
        return (
            ["verity.core", "verity.pack.api", "verity.pack.security"],
            {
                "product.json": init_product(
                    name,
                    owner,
                    [
                        {"type": "exposes", "target": "api.example.get"},
                        {"type": "securedBy", "target": "security.control.example_access"},
                    ],
                ),
                "schema.example.json": init_schema_object(
                    "schema.example",
                    "Example Resource",
                    owner,
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["id", "name"],
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                        },
                    },
                ),
                "api.example-get.json": {
                    "id": "api.example.get",
                    "kind": "api.endpoint",
                    "name": "Get Example",
                    "description": "Returns an example resource after access-control checks.",
                    "status": "ready",
                    "owner": owner,
                    "method": "GET",
                    "path": "/examples/{exampleId}",
                    "summary": "Get an example resource.",
                    "parameters": [
                        {
                            "name": "exampleId",
                            "in": "path",
                            "required": True,
                            "description": "Example resource identifier.",
                            "schema": {"type": "string"},
                        }
                    ],
                    "responses": [
                        {
                            "statusCode": 200,
                            "description": "Example resource returned.",
                            "schema": "schema.example",
                        },
                        {"statusCode": 403, "description": "Caller is not authorized."},
                    ],
                    "references": [],
                },
                "security.example-access.json": {
                    "id": "security.control.example_access",
                    "kind": "security.control",
                    "name": "Example Access Control",
                    "description": "Requires example resource access to be limited to authorized callers.",
                    "status": "ready",
                    "owner": owner,
                    "category": "authorization",
                    "controlType": "preventive",
                    "riskLevel": "high",
                    "objective": "Prevent unauthorized access to example resources.",
                    "coverage": "verified",
                    "verification": {
                        "method": "automated-test",
                        "evidence": "tests/security/test_example_access.py::test_authorized_callers_only",
                    },
                    "references": [
                        {"type": "appliesTo", "target": "api.example.get"},
                        {"type": "appliesTo", "target": "schema.example"},
                    ],
                },
            },
        )
    return (
        DEFAULT_PACKS,
        {
            "product.json": init_product(name, owner),
        },
    )


def cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.path).resolve()
    config_path = target / "verityspec.json"
    records_path = target / "records"
    product_name = args.name or "Example Product"
    packs, records = init_template(args.template, product_name, args.owner)

    if config_path.exists() and not args.force:
        print(f"Workspace already exists: {config_path}", file=sys.stderr)
        return EXIT_USAGE_ERROR
    if records_path.exists() and any(records_path.glob("*.json")) and not args.force:
        print(f"Record directory already contains JSON records: {records_path}", file=sys.stderr)
        return EXIT_USAGE_ERROR

    target.mkdir(parents=True, exist_ok=True)
    records_path.mkdir(exist_ok=True)

    config = {
        "workspace": args.name or target.name,
        "specVersion": CURRENT_SPEC_VERSION,
        "packs": packs,
        "packPaths": [],
        "records": ["records/*.json"],
    }
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    for file_name, record in records.items():
        (records_path / file_name).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"Created VeritySpec {args.template} workspace at {target}")
    return EXIT_SUCCESS


def title_from_identifier(value: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[._-]+", value) if part)


def default_pack_kind(pack_id: str) -> str:
    suffix = pack_id.removeprefix("verity.pack.").removeprefix("verity.")
    return f"{suffix}.example"


def schema_file_name(kind: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", kind).strip("-").lower() + ".schema.json"


def starter_pack_schema(kind: str, title: str) -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "type": "object",
        "additionalProperties": False,
        "required": ["id", "kind", "name", "status", "owner", "description"],
        "properties": {
            "id": {
                "type": "string",
                "pattern": "^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$",
            },
            "kind": {
                "type": "string",
                "const": kind,
            },
            "name": {
                "type": "string",
                "minLength": 1,
            },
            "description": {
                "type": "string",
                "minLength": 1,
            },
            "status": {
                "type": "string",
                "enum": ["draft", "review", "ready", "deprecated", "removed"],
            },
            "owner": {
                "type": "string",
                "minLength": 1,
            },
            "references": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["type", "target"],
                    "properties": {
                        "type": {"type": "string"},
                        "target": {"type": "string"},
                        "required": {"type": "boolean", "default": True},
                    },
                },
                "default": [],
            },
        },
    }


def cmd_pack_init(args: argparse.Namespace) -> int:
    pack_id = args.pack_id
    if not PACK_ID_PATTERN.match(pack_id):
        print(f"Invalid pack id: {pack_id}", file=sys.stderr)
        return EXIT_USAGE_ERROR

    target = Path(args.out).resolve()
    if target.exists() and not target.is_dir():
        print(f"Pack output path is not a directory: {target}", file=sys.stderr)
        return EXIT_USAGE_ERROR
    if target.exists() and any(target.iterdir()) and not args.force:
        print(f"Pack directory is not empty: {target}", file=sys.stderr)
        return EXIT_USAGE_ERROR

    kind = args.kind or default_pack_kind(pack_id)
    if not KIND_PATTERN.match(kind):
        print(f"Invalid starter kind: {kind}", file=sys.stderr)
        return EXIT_USAGE_ERROR
    name = args.name or f"{title_from_identifier(pack_id)} Pack"
    description = args.description or f"{name} extension records."
    schema_path = f"schemas/{schema_file_name(kind)}"
    schema_title = title_from_identifier(kind)
    manifest = {
        "id": pack_id,
        "version": "0.1.0",
        "name": name,
        "description": description,
        "schemas": [
            {
                "kind": kind,
                "path": schema_path,
            }
        ],
        "readinessGates": [
            {
                "id": f"{kind}.release",
                "kind": kind,
                "required": ["owner", "name", "description"],
            }
        ],
        "referenceRules": [
            {
                "sourceKind": "product",
                "relationship": "uses",
                "targetKind": kind,
            }
        ],
        "generators": [
            {
                "id": "schema-bundle",
                "name": "Schema Bundle",
                "description": "Emit a JSON Schema bundle for records loaded by this pack.",
                "artifactType": "schema-bundle",
                "outputFormats": ["json"],
                "recordKinds": [kind],
            }
        ],
    }

    (target / "schemas").mkdir(parents=True, exist_ok=True)
    (target / "pack.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (target / schema_path).write_text(
        json.dumps(starter_pack_schema(kind, schema_title), indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Created VeritySpec pack at {target}")
    return EXIT_SUCCESS


def cmd_validate(args: argparse.Namespace) -> int:
    workspace, registry = load_context(args.workspace, args.pack_path)
    effective = resolve_profile(args.profile, strict=args.strict, fail_on=args.fail_on)
    issues = validate_workspace(workspace, registry, strict=effective.strict)
    issues.extend(profile_issues(workspace, effective.profile))
    print_issue_result("Validation", "validate", issues, args.format, effective.to_dict())
    maybe_print_github_annotations(args, issues)
    return issue_exit_with_fail_on(issues, effective.fail_on)


def cmd_lint(args: argparse.Namespace) -> int:
    workspace, registry = load_context(args.workspace, args.pack_path)
    effective = resolve_profile(args.profile, strict=args.strict, fail_on=args.fail_on)
    issues = lint_workspace(workspace, registry, strict=effective.strict)
    issues.extend(profile_issues(workspace, effective.profile))
    print_issue_result("Lint", "lint", issues, args.format, effective.to_dict())
    maybe_print_github_annotations(args, issues)
    return issue_exit_with_fail_on(issues, effective.fail_on)


def cmd_readiness(args: argparse.Namespace) -> int:
    workspace, registry = load_context(args.workspace, args.pack_path)
    effective = resolve_profile(args.profile, strict=args.strict, fail_on=args.fail_on)
    validation_issues = validate_workspace(workspace, registry, strict=effective.strict)
    readiness_issues = evaluate_readiness(workspace, registry, strict=effective.strict)
    issues = validation_issues + readiness_issues + profile_issues(workspace, effective.profile)
    print_issue_result("Readiness", "readiness", issues, args.format, effective.to_dict())
    maybe_print_github_annotations(args, issues)
    return issue_exit_with_fail_on(issues, effective.fail_on)


def cmd_graph(args: argparse.Namespace) -> int:
    workspace, _registry = load_context(args.workspace)
    graph = build_graph(workspace)
    if args.focus:
        graph = focus_graph(graph, args.focus)
    if args.orphans:
        graph = orphan_graph(graph)
    if args.cycles:
        graph = cycle_graph(graph)
    if args.format == "json":
        print(json.dumps(graph, indent=2))
    else:
        print(graph_to_text(graph))
    return EXIT_SUCCESS


def focus_graph(graph: dict, focus_id: str) -> dict:
    related = {focus_id}
    edges = []
    for edge in graph["edges"]:
        if edge["source"] == focus_id or edge["target"] == focus_id:
            edges.append(edge)
            related.add(edge["source"])
            related.add(edge["target"])
    nodes = [node for node in graph["nodes"] if node["id"] in related]
    return {"nodes": nodes, "edges": edges}


def orphan_graph(graph: dict) -> dict:
    connected = set()
    for edge in graph["edges"]:
        connected.add(edge["source"])
        connected.add(edge["target"])
    nodes = [
        node
        for node in graph["nodes"]
        if node["id"] not in connected and node["kind"] not in {"product", "schema.object"}
    ]
    return {"nodes": nodes, "edges": []}


def cycle_graph(graph: dict) -> dict:
    adjacency: dict[str, list[str]] = {node["id"]: [] for node in graph["nodes"]}
    for edge in graph["edges"]:
        adjacency.setdefault(edge["source"], []).append(edge["target"])
    from .validation import find_cycles

    cycles = find_cycles(adjacency)
    cycle_nodes = {record_id for cycle in cycles for record_id in cycle}
    cycle_edges = [
        edge
        for edge in graph["edges"]
        if edge["source"] in cycle_nodes and edge["target"] in cycle_nodes
    ]
    return {
        "nodes": [node for node in graph["nodes"] if node["id"] in cycle_nodes],
        "edges": cycle_edges,
        "cycles": cycles,
    }


def cmd_diff(args: argparse.Namespace) -> int:
    old = load_workspace(args.old)
    new = load_workspace(args.new)
    diff = diff_workspaces(old, new)
    if args.format == "json":
        print(json.dumps(diff, indent=2))
    else:
        print(diff_to_text(diff))
    return EXIT_SUCCESS


def cmd_migrate(args: argparse.Namespace) -> int:
    if args.list:
        capabilities = migration_capabilities()
        if args.format == "json":
            print(json.dumps(capabilities, indent=2))
        else:
            print(migration_capabilities_to_text(capabilities))
        return EXIT_SUCCESS

    if not args.workspace:
        print("migrate requires a workspace unless --list is used.", file=sys.stderr)
        return EXIT_USAGE_ERROR

    report = migrate_workspace(args.workspace, target_version=args.to, dry_run=args.dry_run)
    if args.report_out:
        Path(args.report_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report_out).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(migration_report_to_text(report))
    return EXIT_CONTRACT_FAILED if report.get("blocked") else EXIT_SUCCESS


def cmd_generate(args: argparse.Namespace) -> int:
    try:
        generated_at = generated_at_value(args.generated_at) if args.generated_at else None
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_USAGE_ERROR

    if args.artifact != "product-impact" and args.comparison_workspace:
        print(
            f"generate {args.artifact} accepts one workspace path.",
            file=sys.stderr,
        )
        return EXIT_USAGE_ERROR

    if args.artifact == "roadmap-report":
        report = generate_roadmap_report(args.workspace, generated_at=generated_at)
        text = write_generated(report, args.out)
        if not args.out:
            print(text, end="" if text.endswith("\n") else "\n")
        else:
            print(f"Generated roadmap-report: {args.out}")
        return EXIT_SUCCESS

    if args.artifact == "product-impact":
        if not args.comparison_workspace:
            print(
                "generate product-impact requires OLD and NEW workspace paths.",
                file=sys.stderr,
            )
            return EXIT_USAGE_ERROR
        old_workspace, old_registry = load_context(args.workspace, args.pack_path)
        new_workspace, new_registry = load_context(args.comparison_workspace, args.pack_path)
        old_issues = validate_workspace(old_workspace, old_registry, strict=args.strict)
        new_issues = validate_workspace(new_workspace, new_registry, strict=args.strict)
        report = generate_product_impact_report(
            old_workspace,
            new_workspace,
            generated_at=generated_at,
        )
        report["validation"] = {
            "old": issue_result("generate.product-impact.old", old_issues),
            "new": issue_result("generate.product-impact.new", new_issues),
        }
        text = write_generated(report, args.out)
        if not args.out:
            print(text, end="" if text.endswith("\n") else "\n")
        else:
            print(f"Generated product-impact: {args.out}")
        return issue_exit(old_issues + new_issues)

    workspace, registry = load_context(args.workspace, args.pack_path)
    if args.artifact == "validation-report":
        issues = validate_workspace(workspace, registry, strict=args.strict)
        report = generate_validation_report(
            workspace,
            registry,
            issues,
            generated_at=generated_at,
        )
        text = write_generated(report, args.out)
        if not args.out:
            print(text, end="" if text.endswith("\n") else "\n")
        else:
            print(f"Generated validation-report: {args.out}")
        return issue_exit(issues)

    issues = validate_workspace(workspace, registry)
    if has_errors(issues):
        print_issues(issues, sys.stdout)
        print_issue_summary("Generation validation", issues)
        return EXIT_CONTRACT_FAILED

    generators: dict[str, Callable[[], str | dict]] = {
        "openapi": lambda: generate_openapi(workspace),
        "asyncapi": lambda: generate_asyncapi(workspace),
        "typescript": lambda: generate_typescript(workspace),
        "python-models": lambda: generate_python_models(workspace),
        "schema-bundle": lambda: generate_schema_bundle(registry),
        "cli-reference": lambda: generate_cli_reference(workspace),
        "security-report": lambda: generate_security_report(workspace, generated_at=generated_at),
        "observability-report": lambda: generate_observability_report(
            workspace,
            generated_at=generated_at,
        ),
        "accessibility-report": lambda: generate_accessibility_report(
            workspace,
            generated_at=generated_at,
        ),
        "compliance-matrix": lambda: generate_compliance_matrix(workspace, generated_at=generated_at),
        "coverage-dashboard": lambda: generate_coverage_dashboard(workspace, generated_at=generated_at),
        "deployment-report": lambda: generate_deployment_report(workspace, generated_at=generated_at),
        "evidence-report": lambda: generate_evidence_report(workspace, generated_at=generated_at),
        "pack-capability-index": lambda: generate_pack_capability_index(
            workspace,
            registry,
            generated_at=generated_at,
        ),
    }
    value = generators[args.artifact]()
    text = write_generated(value, args.out)
    if not args.out:
        print(text, end="" if text.endswith("\n") else "\n")
    else:
        print(f"Generated {args.artifact}: {args.out}")
    return EXIT_SUCCESS


def cmd_import(args: argparse.Namespace) -> int:
    if args.provider == "prismspec":
        report = import_prismspec(args.source, args.out)
        print(json.dumps(report, indent=2))
        return EXIT_SUCCESS
    print(f"Unknown import provider: {args.provider}", file=sys.stderr)
    return EXIT_USAGE_ERROR


def cmd_doctor(args: argparse.Namespace) -> int:
    workspace, registry = load_context(args.workspace, args.pack_path)
    effective = resolve_profile(args.profile, strict=args.strict, fail_on=args.fail_on)
    validation_issues = validate_workspace(workspace, registry, strict=effective.strict)
    lint_issues = lint_workspace(workspace, registry, strict=effective.strict)
    readiness_issues = evaluate_readiness(workspace, registry, strict=effective.strict)
    issues = dedupe_issues(
        validation_issues
        + lint_issues
        + readiness_issues
        + profile_issues(workspace, effective.profile)
    )
    graph = build_graph(workspace)
    result = {
        "command": "doctor",
        "workspace": str(workspace.base_path),
        "packs": workspace.pack_ids,
        "records": len(workspace.records),
        "graph": {
            "nodes": len(graph["nodes"]),
            "edges": len(graph["edges"]),
        },
        "passed": not should_fail(issues, effective.fail_on),
        "summary": {
            "errors": issue_count(issues, "error"),
            "warnings": issue_count(issues, "warning"),
            "issues": len(issues),
        },
        "issues": [issue.to_dict() for issue in issues],
    }
    profile = effective.to_dict()
    if profile is not None:
        result["profile"] = profile
    if args.report_out:
        write_generated(result, args.report_out)
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Workspace: {result['workspace']}")
        print(f"Records: {result['records']}")
        print(f"Graph: {result['graph']['nodes']} node(s), {result['graph']['edges']} edge(s)")
        print_issue_summary("Doctor", issues)
        print_issues(issues, sys.stdout)
    return EXIT_CONTRACT_FAILED if not result["passed"] else EXIT_SUCCESS


def cmd_explain(args: argparse.Namespace) -> int:
    if args.code:
        explanation = explain_issue(args.code)
        if explanation is None:
            print(f"Unknown issue code: {args.code}", file=sys.stderr)
            return EXIT_USAGE_ERROR
        payload = {"code": args.code, **explanation}
        if args.format == "json":
            print(json.dumps(payload, indent=2))
        else:
            print(f"{args.code}: {payload['title']}")
            print(f"Severity: {payload['severity']}")
            print(payload["description"])
            print(f"Resolution: {payload['resolution']}")
        return EXIT_SUCCESS

    payload = {
        "issueCodes": [
            {"code": code, **explanation}
            for code, explanation in sorted(ISSUE_EXPLANATIONS.items())
        ]
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        for item in payload["issueCodes"]:
            print(f"{item['code']} - {item['title']}")
    return EXIT_SUCCESS


def cmd_pack_list(args: argparse.Namespace) -> int:
    packs = list_pack_summaries(args.path)
    if args.format == "json":
        print(json.dumps({"packs": packs}, indent=2))
    else:
        for pack in packs:
            kinds = ", ".join(pack["kinds"]) or "no kinds"
            print(f"{pack['id']} {pack['version']} - {pack['name']} ({kinds})")
    return EXIT_SUCCESS


def cmd_pack_validate(args: argparse.Namespace) -> int:
    issues = validate_packs(args.pack_id, args.path)
    print_issue_result("Pack validation", "pack.validate", issues, args.format)
    return issue_exit(issues)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="verity", description="VeritySpec product-contract CLI.")
    parser.add_argument("--version", action="version", version=f"verity {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_pack_path_argument(command_parser: argparse.ArgumentParser) -> None:
        command_parser.add_argument(
            "--pack-path",
            action="append",
            default=[],
            help="Additional local pack directory or pack.json path.",
        )

    def add_profile_argument(command_parser: argparse.ArgumentParser) -> None:
        command_parser.add_argument(
            "--profile",
            choices=PROFILE_CHOICES,
            help="Apply a product-contract enforcement profile.",
        )

    init_parser = subparsers.add_parser("init", help="Create a VeritySpec workspace.")
    init_parser.add_argument("path")
    init_parser.add_argument("--name")
    init_parser.add_argument("--owner", default="unknown")
    init_parser.add_argument(
        "--template",
        choices=INIT_TEMPLATE_CHOICES,
        default="basic",
        help="Starter workspace template.",
    )
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=cmd_init)

    validate_parser = subparsers.add_parser("validate", help="Validate a workspace.")
    validate_parser.add_argument("workspace")
    validate_parser.add_argument("--strict", action="store_true")
    validate_parser.add_argument("--format", choices=["text", "json"], default="text")
    validate_parser.add_argument("--fail-on", choices=["error", "warning"])
    add_profile_argument(validate_parser)
    validate_parser.add_argument(
        "--github-annotations",
        action="store_true",
        help="Emit GitHub Actions workflow annotations for issues to stderr.",
    )
    add_pack_path_argument(validate_parser)
    validate_parser.set_defaults(func=cmd_validate)

    lint_parser = subparsers.add_parser("lint", help="Lint a workspace.")
    lint_parser.add_argument("workspace")
    lint_parser.add_argument("--strict", action="store_true")
    lint_parser.add_argument("--format", choices=["text", "json"], default="text")
    lint_parser.add_argument("--fail-on", choices=["error", "warning"])
    add_profile_argument(lint_parser)
    lint_parser.add_argument(
        "--github-annotations",
        action="store_true",
        help="Emit GitHub Actions workflow annotations for issues to stderr.",
    )
    add_pack_path_argument(lint_parser)
    lint_parser.set_defaults(func=cmd_lint)

    readiness_parser = subparsers.add_parser("readiness", help="Evaluate release readiness gates.")
    readiness_parser.add_argument("workspace")
    readiness_parser.add_argument("--strict", action="store_true")
    readiness_parser.add_argument("--format", choices=["text", "json"], default="text")
    readiness_parser.add_argument("--fail-on", choices=["error", "warning"])
    add_profile_argument(readiness_parser)
    readiness_parser.add_argument(
        "--github-annotations",
        action="store_true",
        help="Emit GitHub Actions workflow annotations for issues to stderr.",
    )
    add_pack_path_argument(readiness_parser)
    readiness_parser.set_defaults(func=cmd_readiness)

    doctor_parser = subparsers.add_parser("doctor", help="Run diagnostics for a workspace.")
    doctor_parser.add_argument("workspace")
    doctor_parser.add_argument("--strict", action="store_true")
    doctor_parser.add_argument("--format", choices=["text", "json"], default="text")
    doctor_parser.add_argument("--fail-on", choices=["error", "warning"])
    add_profile_argument(doctor_parser)
    doctor_parser.add_argument("--report-out", help="Write the structured doctor report JSON to a file.")
    add_pack_path_argument(doctor_parser)
    doctor_parser.set_defaults(func=cmd_doctor)

    explain_parser = subparsers.add_parser("explain", help="Explain a validation issue code.")
    explain_parser.add_argument("code", nargs="?")
    explain_parser.add_argument("--format", choices=["text", "json"], default="text")
    explain_parser.set_defaults(func=cmd_explain)

    graph_parser = subparsers.add_parser("graph", help="Print the workspace reference graph.")
    graph_parser.add_argument("workspace")
    graph_parser.add_argument("--format", choices=["text", "json"], default="text")
    graph_parser.add_argument("--focus")
    graph_parser.add_argument("--orphans", action="store_true")
    graph_parser.add_argument("--cycles", action="store_true")
    graph_parser.set_defaults(func=cmd_graph)

    diff_parser = subparsers.add_parser("diff", help="Diff two workspaces.")
    diff_parser.add_argument("old")
    diff_parser.add_argument("new")
    diff_parser.add_argument("--format", choices=["text", "json"], default="text")
    diff_parser.set_defaults(func=cmd_diff)

    migrate_parser = subparsers.add_parser("migrate", help="Migrate a workspace to a supported spec version.")
    migrate_parser.add_argument("workspace", nargs="?")
    migrate_parser.add_argument("--list", action="store_true", help="List supported migration versions and steps.")
    migrate_parser.add_argument("--to", default=CURRENT_SPEC_VERSION)
    migrate_parser.add_argument("--dry-run", action="store_true")
    migrate_parser.add_argument("--format", choices=["text", "json"], default="text")
    migrate_parser.add_argument("--report-out")
    migrate_parser.set_defaults(func=cmd_migrate)

    generate_parser = subparsers.add_parser("generate", help="Generate an artifact.")
    generate_parser.add_argument(
        "artifact",
        choices=[
            "openapi",
            "asyncapi",
            "typescript",
            "python-models",
            "schema-bundle",
            "cli-reference",
            "validation-report",
            "security-report",
            "observability-report",
            "accessibility-report",
            "compliance-matrix",
            "coverage-dashboard",
            "deployment-report",
            "evidence-report",
            "pack-capability-index",
            "product-impact",
            "roadmap-report",
        ],
    )
    generate_parser.add_argument("workspace")
    generate_parser.add_argument("comparison_workspace", nargs="?")
    generate_parser.add_argument("--out")
    generate_parser.add_argument("--strict", action="store_true")
    generate_parser.add_argument(
        "--generated-at",
        help="Override generatedAt for JSON report artifacts with an ISO 8601 datetime.",
    )
    add_pack_path_argument(generate_parser)
    generate_parser.set_defaults(func=cmd_generate)

    import_parser = subparsers.add_parser("import", help="Import a predecessor specification.")
    import_parser.add_argument("provider", choices=["prismspec"])
    import_parser.add_argument("source")
    import_parser.add_argument("--out", required=True)
    import_parser.set_defaults(func=cmd_import)

    pack_parser = subparsers.add_parser("pack", help="Inspect and validate VeritySpec packs.")
    pack_subparsers = pack_parser.add_subparsers(dest="pack_command", required=True)

    pack_list_parser = pack_subparsers.add_parser("list", help="List built-in packs.")
    pack_list_parser.add_argument("--format", choices=["text", "json"], default="text")
    pack_list_parser.add_argument("--path", action="append", default=[], help="Local pack directory or pack.json path.")
    pack_list_parser.set_defaults(func=cmd_pack_list)

    pack_validate_parser = pack_subparsers.add_parser("validate", help="Validate built-in packs.")
    pack_validate_parser.add_argument("pack_id", nargs="?")
    pack_validate_parser.add_argument("--format", choices=["text", "json"], default="text")
    pack_validate_parser.add_argument("--path", action="append", default=[], help="Local pack directory or pack.json path.")
    pack_validate_parser.set_defaults(func=cmd_pack_validate)

    pack_init_parser = pack_subparsers.add_parser("init", help="Create a local pack scaffold.")
    pack_init_parser.add_argument("pack_id")
    pack_init_parser.add_argument("--out", required=True, help="Output directory for the pack scaffold.")
    pack_init_parser.add_argument("--kind", help="Starter record kind. Defaults to a kind derived from the pack id.")
    pack_init_parser.add_argument("--name", help="Pack display name.")
    pack_init_parser.add_argument("--description", help="Pack description.")
    pack_init_parser.add_argument("--force", action="store_true", help="Write into a non-empty directory.")
    pack_init_parser.set_defaults(func=cmd_pack_init)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_INTERNAL_ERROR
