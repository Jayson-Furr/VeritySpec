# Contributing

VeritySpec is currently early-stage. Contributions should preserve the central
direction of the project: small executable core, pack-based growth, strict
validation, readiness gates, and generators that are tested against examples.

## Local Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools
pip install -e .
```

## Checks

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m verityspec validate examples/basic
PYTHONPATH=src python3 -m verityspec lint examples/basic --strict
PYTHONPATH=src python3 -m verityspec readiness examples/basic --strict
PYTHONPATH=src python3 -m verityspec validate examples/basic --format json
PYTHONPATH=src python3 -m verityspec generate validation-report examples/basic --out build/validation-report.json
```

## Pack Standard

Every new pack should include:

- Schemas
- Executable examples
- Validation tests
- Readiness gates
- At least one useful generator or report
- Documentation for records and workflow
