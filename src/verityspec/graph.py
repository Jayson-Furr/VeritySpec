from __future__ import annotations

from .references import extract_reference_edges
from .workspace import Workspace


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
        edge.to_dict()
        for record in workspace.records
        for edge in extract_reference_edges(record)
    ]
    return {"nodes": nodes, "edges": edges}


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

