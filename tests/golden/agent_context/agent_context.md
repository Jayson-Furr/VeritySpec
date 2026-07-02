# VeritySpec Agent Context

- Generated: `<generatedAt>`
- VeritySpec: `<verityVersion>`
- Workspace: `examples.product_delivery`
- Workspace path: `<workspacePath>`
- Spec version: `v0.2.0`
- Target: `agent-context.exporter.implementation_bundle`

> This generated context is a bounded product-contract handoff for humans, tools, and AI coding agents. It does not replace `AGENTS.md`, tests, readiness checks, or implementation evidence.

## Summary

| Metric | Count |
|---|---:|
| Relevant records | 18 |
| Graph links | 25 |
| Deprecated or removed records | 0 |

## Target Exporter

| Field | Value |
|---|---|
| ID | agent-context.exporter.implementation_bundle |
| Kind | agent-context.exporter |
| Name | Implementation Agent Context Exporter |
| Status | ready |
| Owner | tooling |
| Exporter type | markdown |
| Output path | build/agent-context.md |
| Included kinds | product.scope, release.process, readiness.profile, evidence.requirement |
| Privacy policy | Do not include secrets, credentials, or private customer data in exported context. |
| Redaction policy | Exclude environment-specific secrets and unpublished commercial terms. |

## Relevant Records

| ID | Kind | Status | Owner | Description |
|---|---|---|---|---|
| agent-context.exporter.implementation_bundle | agent-context.exporter | ready | tooling | Exports scoped product-delivery context for AI agents working in the repository. |
| archive.policy.retained_source | archive.policy | ready | maintenance | Defines source, release, and generated-artifact archival expectations for the repository. |
| commercial.posture.private_alpha | commercial.posture | ready | product | Captures proprietary private-alpha posture without asserting external marketplace, legal, or privacy compliance. |
| decision.record.github_manages_workflow | decision.record | ready | program | Records the operating decision that GitHub manages workflow while VeritySpec manages truth. |
| decommission.policy.sunset | decommission.policy | ready | maintenance | Defines the handoff and archival path if the toolkit is replaced or retired. |
| editor.surface.readiness_dashboard | editor.surface | ready | tooling | Represents an editor or dashboard surface for reviewing product-delivery readiness and evidence gaps. |
| evidence.requirement.local_ci | evidence.requirement | ready | release | Requires recorded local or hosted CI evidence before a private alpha release is treated as ready. |
| generator.capability.agent_context | generator.capability | ready | tooling | Generates bounded implementation context from product-delivery and readiness records. |
| maintenance.policy.active | maintenance.policy | ready | maintenance | Defines dependency, compatibility, and update expectations while the toolkit is actively maintained. |
| operations.model.maintained_toolkit | operations.model | ready | operations | Defines lightweight operational ownership for a maintained engine-tooling repository. |
| product.product_delivery_toolkit | product | ready | platform | An example repository that uses VeritySpec as its product-contract source of truth. |
| product.scope.engine_toolkit_delivery | product.scope | ready | product | Defines the source-of-truth scope for an engine toolkit repository managed through VeritySpec records and GitHub workflow artifacts. |
| project-management.model.github_native | project-management.model | ready | program | Uses GitHub Issues, Projects, Milestones, Actions, and pull requests for workflow while VeritySpec records hold product truth. |
| readiness.profile.private_alpha | readiness.profile | ready | release | Defines internal readiness checks for a private alpha engine-tooling repository. |
| release.process.tagged_alpha | release.process | ready | release | Defines branch, tag, approval, and artifact rules for private alpha releases. |
| scanner.capability.workspace_contracts | scanner.capability | ready | tooling | Scans VeritySpec workspace records to find missing product-delivery coverage. |
| support.policy.private_alpha | support.policy | ready | support | Defines support expectations for private alpha users and maintainers. |
| validation.runner.local_ci | validation.runner | ready | tooling | Runs local validation, lint, readiness, graph, and generation checks when hosted CI is unavailable. |

## Graph Links

| Source | Relationship | Target | Field |
|---|---|---|---|
| agent-context.exporter.implementation_bundle | describesScope | product.scope.engine_toolkit_delivery | references[0].target |
| agent-context.exporter.implementation_bundle | usesGenerator | generator.capability.agent_context | references[2].target |
| agent-context.exporter.implementation_bundle | usesReadinessProfile | readiness.profile.private_alpha | references[1].target |
| decommission.policy.sunset | usesArchivePolicy | archive.policy.retained_source | references[0].target |
| editor.surface.readiness_dashboard | runsValidation | validation.runner.local_ci | references[0].target |
| generator.capability.agent_context | generatesForScope | product.scope.engine_toolkit_delivery | references[0].target |
| maintenance.policy.active | usesArchivePolicy | archive.policy.retained_source | references[0].target |
| maintenance.policy.active | usesDecommissionPolicy | decommission.policy.sunset | references[1].target |
| operations.model.maintained_toolkit | supportedBy | support.policy.private_alpha | references[0].target |
| product.product_delivery_toolkit | hasProductScope | product.scope.engine_toolkit_delivery | references[0].target |
| product.scope.engine_toolkit_delivery | hasArchivePolicy | archive.policy.retained_source | references[7].target |
| product.scope.engine_toolkit_delivery | hasCommercialPosture | commercial.posture.private_alpha | references[0].target |
| product.scope.engine_toolkit_delivery | hasDecommissionPolicy | decommission.policy.sunset | references[8].target |
| product.scope.engine_toolkit_delivery | hasMaintenancePolicy | maintenance.policy.active | references[6].target |
| product.scope.engine_toolkit_delivery | hasReadinessProfile | readiness.profile.private_alpha | references[2].target |
| product.scope.engine_toolkit_delivery | hasSupportPolicy | support.policy.private_alpha | references[5].target |
| product.scope.engine_toolkit_delivery | managedBy | project-management.model.github_native | references[1].target |
| product.scope.engine_toolkit_delivery | usesOperationsModel | operations.model.maintained_toolkit | references[4].target |
| product.scope.engine_toolkit_delivery | usesReleaseProcess | release.process.tagged_alpha | references[3].target |
| project-management.model.github_native | recordsDecision | decision.record.github_manages_workflow | references[0].target |
| readiness.profile.private_alpha | requiresEvidence | evidence.requirement.local_ci | references[0].target |
| release.process.tagged_alpha | requiresEvidence | evidence.requirement.local_ci | references[1].target |
| release.process.tagged_alpha | usesReadinessProfile | readiness.profile.private_alpha | references[0].target |
| scanner.capability.workspace_contracts | scansScope | product.scope.engine_toolkit_delivery | references[0].target |
| validation.runner.local_ci | runsScanner | scanner.capability.workspace_contracts | references[0].target |

## Generated Artifacts

- `build/agent-context.md`

## Deprecated Or Removed Records

- none

## Safety Boundaries

- This generated context does not prove implementation correctness.
- This generated context does not replace tests, readiness checks, or evidence records.
- This generated context does not make legal, commercial, privacy, marketplace, or certification claims.
- This generated context does not authorize agents to bypass repository process.
- AGENTS.md remains the canonical repository entry point for agent operating rules.

## Verification Commands

- `verity validate <workspacePath>`
- `verity lint <workspacePath> --strict`
- `verity readiness <workspacePath> --strict`
- `verity graph <workspacePath>`
- `verity generate agent-context <workspacePath> --record agent-context.exporter.implementation_bundle --format markdown --out build/agent-context.md`
