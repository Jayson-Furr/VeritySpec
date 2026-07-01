from __future__ import annotations

from .dependencies import resolve_workspace_dependencies, split_dependency_reference
from .references import ReferenceEdge, extract_reference_edges
from .workspace import Workspace


def edge_to_dict(
    edge: ReferenceEdge,
    *,
    source: str | None = None,
    target: str | None = None,
    **extra: object,
) -> dict:
    data = {
        "source": source or edge.source,
        "target": target or edge.target,
        "relationship": edge.relationship,
        "field": edge.field,
    }
    data.update(extra)
    return data


def build_graph(workspace: Workspace) -> dict:
    nodes = [
        {
            "id": record.id,
            "kind": record.kind,
            "name": record.data.get("name"),
            "status": record.data.get("status"),
        }
        for record in workspace.records
        if record.id
    ]
    edges = [
        edge_to_dict(edge)
        for record in workspace.records
        for edge in extract_reference_edges(record)
    ]
    dependency_resolution = resolve_workspace_dependencies(workspace)

    for dependency in dependency_resolution.dependencies:
        for record_id in sorted(dependency.exported_ids):
            record = dependency.records_by_id.get(record_id)
            if record is None:
                continue
            nodes.append(
                {
                    "id": dependency.qualified_id(record_id),
                    "kind": record.kind,
                    "name": record.data.get("name"),
                    "status": record.data.get("status"),
                    "workspaceRole": "dependency",
                    "dependencyAlias": dependency.declaration.alias,
                    "dependencyWorkspace": dependency.declaration.id,
                    "dependencySource": dependency.declaration.source,
                    "exported": True,
                }
            )

            for edge in extract_reference_edges(record):
                dependency_target = split_dependency_reference(edge.target)
                if dependency_target is not None:
                    target_alias, target_id = dependency_target
                    target = f"{target_alias}::{target_id}"
                elif edge.target in dependency.exported_ids:
                    target = dependency.qualified_id(edge.target)
                else:
                    target = edge.target
                edges.append(
                    edge_to_dict(
                        edge,
                        source=dependency.qualified_id(record_id),
                        target=target,
                        workspaceRole="dependency",
                        dependencyAlias=dependency.declaration.alias,
                        dependencyWorkspace=dependency.declaration.id,
                    )
                )

    return {
        "nodes": nodes,
        "edges": edges,
        "dependencies": [
            {
                "id": dependency.declaration.id,
                "alias": dependency.declaration.alias,
                "source": dependency.declaration.source,
                "version": dependency.workspace.config.get("version"),
                "exportedRecords": sorted(dependency.exported_ids),
            }
            for dependency in dependency_resolution.dependencies
        ],
    }


def graph_to_text(graph: dict) -> str:
    lines = ["Nodes:"]
    for node in graph["nodes"]:
        lines.append(f"  {node['id']} ({node['kind']}, {node.get('status')})")
    lines.append("Edges:")
    for edge in graph["edges"]:
        lines.append(
            f"  {edge['source']} --{edge['relationship']}:{edge['field']}--> {edge['target']}"
        )
    return "\n".join(lines)
