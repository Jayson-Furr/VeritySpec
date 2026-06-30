from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable

from . import __version__
from .diffing import diff_to_text, diff_workspaces
from .generators import (
    generate_asyncapi,
    generate_cli_reference,
    generate_openapi,
    generate_python_models,
    generate_schema_bundle,
    generate_typescript,
    generate_validation_report,
    write_generated,
)
from .graph import build_graph, graph_to_text
from .importers.prismspec import import_prismspec
from .issues import has_errors, issue_count, print_issues
from .packs import load_pack_registry
from .readiness import evaluate_readiness
from .validation import lint_workspace, validate_workspace
from .workspace import DEFAULT_PACKS, load_workspace


EXIT_SUCCESS = 0
EXIT_CONTRACT_FAILED = 1
EXIT_USAGE_ERROR = 2
EXIT_INTERNAL_ERROR = 3


def load_context(path: str):
    workspace = load_workspace(path)
    registry = load_pack_registry(workspace.pack_ids)
    return workspace, registry


def issue_exit(issues) -> int:
    return EXIT_CONTRACT_FAILED if has_errors(issues) else EXIT_SUCCESS


def print_issue_summary(label: str, issues) -> None:
    errors = issue_count(issues, "error")
    warnings = issue_count(issues, "warning")
    if errors == 0 and warnings == 0:
        print(f"{label} passed.")
    else:
        print(f"{label} completed with {errors} error(s), {warnings} warning(s).")


def issue_result(command_name: str, issues) -> dict:
    errors = issue_count(issues, "error")
    warnings = issue_count(issues, "warning")
    return {
        "command": command_name,
        "passed": errors == 0,
        "summary": {
            "errors": errors,
            "warnings": warnings,
            "issues": errors + warnings,
        },
        "issues": [issue.to_dict() for issue in issues],
    }


def print_issue_result(label: str, command_name: str, issues, output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(issue_result(command_name, issues), indent=2))
        return
    print_issues(issues, sys.stdout)
    print_issue_summary(label, issues)


def cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.path).resolve()
    target.mkdir(parents=True, exist_ok=True)
    config_path = target / "verityspec.json"
    records_path = target / "records"
    records_path.mkdir(exist_ok=True)

    if config_path.exists() and not args.force:
        print(f"Workspace already exists: {config_path}", file=sys.stderr)
        return EXIT_USAGE_ERROR

    config = {
        "workspace": args.name or target.name,
        "specVersion": "v0.1.0",
        "packs": DEFAULT_PACKS,
        "records": ["records/*.json"],
    }
    product = {
        "id": "product.example",
        "kind": "product",
        "name": args.name or "Example Product",
        "description": "Describe the product contract.",
        "status": "draft",
        "owner": args.owner,
        "version": "0.1.0",
        "references": [],
    }
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    (records_path / "product.json").write_text(json.dumps(product, indent=2) + "\n", encoding="utf-8")
    print(f"Created VeritySpec workspace at {target}")
    return EXIT_SUCCESS


def cmd_validate(args: argparse.Namespace) -> int:
    workspace, registry = load_context(args.workspace)
    issues = validate_workspace(workspace, registry, strict=args.strict)
    print_issue_result("Validation", "validate", issues, args.format)
    return issue_exit(issues)


def cmd_lint(args: argparse.Namespace) -> int:
    workspace, registry = load_context(args.workspace)
    issues = lint_workspace(workspace, registry, strict=args.strict)
    print_issue_result("Lint", "lint", issues, args.format)
    return issue_exit(issues)


def cmd_readiness(args: argparse.Namespace) -> int:
    workspace, registry = load_context(args.workspace)
    validation_issues = validate_workspace(workspace, registry, strict=args.strict)
    readiness_issues = evaluate_readiness(workspace, registry, strict=args.strict)
    issues = validation_issues + readiness_issues
    print_issue_result("Readiness", "readiness", issues, args.format)
    return issue_exit(issues)


def cmd_graph(args: argparse.Namespace) -> int:
    workspace, _registry = load_context(args.workspace)
    graph = build_graph(workspace)
    if args.format == "json":
        print(json.dumps(graph, indent=2))
    else:
        print(graph_to_text(graph))
    return EXIT_SUCCESS


def cmd_diff(args: argparse.Namespace) -> int:
    old = load_workspace(args.old)
    new = load_workspace(args.new)
    diff = diff_workspaces(old, new)
    if args.format == "json":
        print(json.dumps(diff, indent=2))
    else:
        print(diff_to_text(diff))
    return EXIT_SUCCESS


def cmd_generate(args: argparse.Namespace) -> int:
    workspace, registry = load_context(args.workspace)
    if args.artifact == "validation-report":
        issues = validate_workspace(workspace, registry, strict=args.strict)
        report = generate_validation_report(workspace, registry, issues)
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="verity", description="VeritySpec product-contract CLI.")
    parser.add_argument("--version", action="version", version=f"verity {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a VeritySpec workspace.")
    init_parser.add_argument("path")
    init_parser.add_argument("--name")
    init_parser.add_argument("--owner", default="unknown")
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=cmd_init)

    validate_parser = subparsers.add_parser("validate", help="Validate a workspace.")
    validate_parser.add_argument("workspace")
    validate_parser.add_argument("--strict", action="store_true")
    validate_parser.add_argument("--format", choices=["text", "json"], default="text")
    validate_parser.set_defaults(func=cmd_validate)

    lint_parser = subparsers.add_parser("lint", help="Lint a workspace.")
    lint_parser.add_argument("workspace")
    lint_parser.add_argument("--strict", action="store_true")
    lint_parser.add_argument("--format", choices=["text", "json"], default="text")
    lint_parser.set_defaults(func=cmd_lint)

    readiness_parser = subparsers.add_parser("readiness", help="Evaluate release readiness gates.")
    readiness_parser.add_argument("workspace")
    readiness_parser.add_argument("--strict", action="store_true")
    readiness_parser.add_argument("--format", choices=["text", "json"], default="text")
    readiness_parser.set_defaults(func=cmd_readiness)

    graph_parser = subparsers.add_parser("graph", help="Print the workspace reference graph.")
    graph_parser.add_argument("workspace")
    graph_parser.add_argument("--format", choices=["text", "json"], default="text")
    graph_parser.set_defaults(func=cmd_graph)

    diff_parser = subparsers.add_parser("diff", help="Diff two workspaces.")
    diff_parser.add_argument("old")
    diff_parser.add_argument("new")
    diff_parser.add_argument("--format", choices=["text", "json"], default="text")
    diff_parser.set_defaults(func=cmd_diff)

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
        ],
    )
    generate_parser.add_argument("workspace")
    generate_parser.add_argument("--out")
    generate_parser.add_argument("--strict", action="store_true")
    generate_parser.set_defaults(func=cmd_generate)

    import_parser = subparsers.add_parser("import", help="Import a predecessor specification.")
    import_parser.add_argument("provider", choices=["prismspec"])
    import_parser.add_argument("source")
    import_parser.add_argument("--out", required=True)
    import_parser.set_defaults(func=cmd_import)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_INTERNAL_ERROR
