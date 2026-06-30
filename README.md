# VeritySpec

Executable product contracts for humans, tools, and agents.

VeritySpec supersedes PrismSpec by changing the project from a broad static
schema catalog into an installable product-specification toolchain. The core
artifact is a workspace that can be validated, linted, checked for readiness,
graphed, diffed, and used to generate implementation and documentation
artifacts.

## Current Scope

This initial implementation provides:

- An installable Python package with the `verity` CLI.
- A small core model: workspace, pack, schema, record, reference graph,
  validation issue, readiness gate, generator, and migration entry point.
- Built-in packs for core product records, APIs, CLIs, and events.
- Structural validation with JSON Schema.
- Semantic validation for duplicate IDs, unknown kinds, missing references,
  deprecated references, and removed references.
- Readiness gates driven by pack metadata.
- Generators for OpenAPI, AsyncAPI, TypeScript types, Python models, schema
  bundles, and CLI reference docs.
- A starter PrismSpec importer that produces a migration report.

## Quick Start

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools
pip install -e .

verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity graph examples/basic
verity generate openapi examples/basic --out build/openapi.json
verity generate asyncapi examples/basic --out build/asyncapi.json
verity generate typescript examples/basic --out build/types.ts
verity generate python-models examples/basic --out build/models.py
verity generate cli-reference examples/basic --out build/cli-reference.md
```

Without installation, run the package directly:

```bash
PYTHONPATH=src python3 -m verityspec validate examples/basic
```

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Workspace Shape

```json
{
  "workspace": "examples.basic",
  "specVersion": "v0.1.0",
  "packs": [
    "verity.core",
    "verity.pack.api",
    "verity.pack.cli",
    "verity.pack.events"
  ],
  "records": [
    "records/*.json"
  ]
}
```

Records are normal JSON files. Every record has an `id`, `kind`, `name`,
`status`, and `owner`, plus fields defined by its pack.

## Supersession

PrismSpec established the initial product-specification vocabulary. VeritySpec
supersedes it with a smaller kernel, a pack-based architecture, executable
validation, readiness gates, graph analysis, diffing, generators, and migration
tooling.

PrismSpec remains the prototype. VeritySpec is the active implementation.
