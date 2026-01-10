from autometabuilder.workflow.workflow_graph import build_workflow_graph


def test_build_workflow_graph_structure():
    graph = build_workflow_graph()
    assert isinstance(graph.get("nodes"), list), "nodes list should be present"
    assert isinstance(graph.get("edges"), list), "edges list should be present"
    counts = graph.get("count", {})
    assert counts.get("nodes", 0) >= 5, "Expect at least the top-level nodes to exist"
    assert counts.get("edges", 0) > 0, "Edges should exist between workflow nodes"

    node_ids = {node["id"] for node in graph["nodes"]}
    for edge in graph["edges"]:
        assert edge["from"] in node_ids, f"Edge source {edge['from']} not in node IDs"
        assert edge["to"] in node_ids, f"Edge target {edge['to']} not in node IDs"
        # N8N format uses 'type' instead of 'var'
        assert "type" in edge or "var" in edge, "edges should have connection type or variable"
