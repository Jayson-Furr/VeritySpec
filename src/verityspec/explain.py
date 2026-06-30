from __future__ import annotations


ISSUE_EXPLANATIONS: dict[str, dict[str, str]] = {
    "graph.cycle": {
        "title": "Reference cycle",
        "severity": "warning",
        "description": "A directed reference path loops back to an earlier record.",
        "resolution": "Break the cycle by removing or changing one reference edge.",
    },
    "graph.orphan": {
        "title": "Orphan record",
        "severity": "warning",
        "description": "A non-product, non-schema record has no incoming or outgoing graph references.",
        "resolution": "Reference the record from a product or another record, or remove it.",
    },
    "lint.description.missing": {
        "title": "Missing description",
        "severity": "warning",
        "description": "A record should include a useful human-readable description.",
        "resolution": "Add a non-empty description field.",
    },
    "lint.owner.placeholder": {
        "title": "Placeholder owner",
        "severity": "warning",
        "description": "The owner field uses a placeholder value.",
        "resolution": "Set owner to the team, person, or system responsible for the record.",
    },
    "lint.status.draft": {
        "title": "Draft record",
        "severity": "warning",
        "description": "Draft records are not considered release-ready.",
        "resolution": "Move the record to review or ready once the contract is accepted.",
    },
    "pack.unknown": {
        "title": "Unknown pack",
        "severity": "error",
        "description": "The requested pack ID is not available.",
        "resolution": "Run `verity pack list` and use one of the listed pack IDs.",
    },
    "readiness.required": {
        "title": "Readiness field missing",
        "severity": "warning",
        "description": "A readiness gate requires a field that is missing or empty.",
        "resolution": "Add the required field or adjust the relevant pack readiness gate.",
    },
    "readiness.min_items": {
        "title": "Readiness list too small",
        "severity": "warning",
        "description": "A readiness gate requires a list field to contain at least a minimum number of items.",
        "resolution": "Add the required items to the record.",
    },
    "record.id.duplicate": {
        "title": "Duplicate record ID",
        "severity": "error",
        "description": "Two records use the same ID.",
        "resolution": "Give each record a unique stable ID.",
    },
    "record.id.missing": {
        "title": "Missing record ID",
        "severity": "error",
        "description": "A record does not define a string ID.",
        "resolution": "Add an id field that matches the VeritySpec ID pattern.",
    },
    "record.kind.missing": {
        "title": "Missing record kind",
        "severity": "error",
        "description": "A record does not define a string kind.",
        "resolution": "Add a kind field declared by one of the loaded packs.",
    },
    "record.kind.unknown": {
        "title": "Unknown record kind",
        "severity": "error",
        "description": "A record uses a kind not declared by the loaded packs.",
        "resolution": "Load the pack that declares the kind or change the record kind.",
    },
    "reference.deprecated": {
        "title": "Deprecated reference",
        "severity": "warning",
        "description": "A record references another record marked deprecated.",
        "resolution": "Move the reference to the replacement record or acknowledge it before release.",
    },
    "reference.disallowed": {
        "title": "Disallowed reference relationship",
        "severity": "error",
        "description": "The source kind, relationship, and target kind combination is not allowed by loaded pack rules.",
        "resolution": "Use an allowed relationship or add a pack rule that explicitly permits it.",
    },
    "reference.missing": {
        "title": "Missing reference target",
        "severity": "error",
        "description": "A reference points to a record ID that does not exist in the workspace.",
        "resolution": "Create the target record or update the reference target.",
    },
    "reference.removed": {
        "title": "Removed reference target",
        "severity": "error",
        "description": "A record references another record marked removed.",
        "resolution": "Remove the reference or point it to an active replacement.",
    },
    "schema.unused": {
        "title": "Unused schema",
        "severity": "warning",
        "description": "A schema record has no incoming references.",
        "resolution": "Reference the schema from a record or remove it.",
    },
    "schema.validation": {
        "title": "Schema validation failure",
        "severity": "error",
        "description": "A record does not satisfy the JSON Schema for its kind.",
        "resolution": "Update the record to match its pack schema.",
    },
    "workspace.packPaths.invalid": {
        "title": "Invalid workspace pack paths",
        "severity": "error",
        "description": "A v0.2.0 workspace declares packPaths, but it is not an array of strings.",
        "resolution": "Set packPaths to an array of local pack paths, or [] when no external packs are used.",
    },
    "workspace.packPaths.missing": {
        "title": "Missing workspace pack paths",
        "severity": "error",
        "description": "A v0.2.0 workspace must declare packPaths explicitly.",
        "resolution": "Run `verity migrate` or add `\"packPaths\": []` to verityspec.json.",
    },
    "workspace.version.future": {
        "title": "Future workspace version",
        "severity": "error",
        "description": "The workspace declares a specVersion newer than this VeritySpec CLI supports.",
        "resolution": "Install a newer VeritySpec CLI before validating or migrating the workspace.",
    },
    "workspace.version.invalid": {
        "title": "Invalid workspace version",
        "severity": "error",
        "description": "The workspace specVersion does not use vMAJOR.MINOR.PATCH format.",
        "resolution": "Set specVersion to a supported value such as v0.2.0.",
    },
    "workspace.version.missing": {
        "title": "Missing workspace version",
        "severity": "error",
        "description": "The workspace config does not declare a specVersion.",
        "resolution": "Run `verity migrate` or add a supported specVersion to verityspec.json.",
    },
    "workspace.version.unsupported": {
        "title": "Unsupported workspace version",
        "severity": "error",
        "description": "The workspace declares a version this VeritySpec CLI does not support.",
        "resolution": "Run `verity migrate` to produce a supported workspace version.",
    },
}


def explain_issue(code: str) -> dict[str, str] | None:
    return ISSUE_EXPLANATIONS.get(code)
