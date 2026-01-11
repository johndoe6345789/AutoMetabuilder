"""Tests for trigger-based workflow execution."""
import pytest

from autometabuilder.workflow.execution_order import build_execution_order


def test_execution_order_without_trigger():
    """Test that execution order works without triggers (backward compatible)."""
    nodes = [
        {"id": "node-1", "name": "Start"},
        {"id": "node-2", "name": "Process"},
        {"id": "node-3", "name": "End"}
    ]
    connections = {
        "Start": {
            "main": {
                "0": [{"node": "Process", "type": "main", "index": 0}]
            }
        },
        "Process": {
            "main": {
                "0": [{"node": "End", "type": "main", "index": 0}]
            }
        }
    }
    
    order = build_execution_order(nodes, connections)
    
    # Start should be first (no inputs)
    assert order[0] == "Start"
    # Process and End should follow
    assert "Process" in order
    assert "End" in order


def test_execution_order_with_trigger():
    """Test that execution order respects trigger start node."""
    nodes = [
        {"id": "node-1", "name": "Start"},
        {"id": "node-2", "name": "Process"},
        {"id": "node-3", "name": "End"}
    ]
    connections = {}
    
    # Specify to start from Process node
    order = build_execution_order(nodes, connections, start_node_id="node-2")
    
    # Process should be first (specified by trigger)
    assert order[0] == "Process"
    # Start and End should follow
    assert "Start" in order
    assert "End" in order


def test_execution_order_with_invalid_trigger_node():
    """Test that invalid trigger node ID falls back to default behavior."""
    nodes = [
        {"id": "node-1", "name": "Start"},
        {"id": "node-2", "name": "Process"}
    ]
    connections = {
        "Start": {
            "main": {
                "0": [{"node": "Process", "type": "main", "index": 0}]
            }
        }
    }
    
    # Try to start from non-existent node
    order = build_execution_order(nodes, connections, start_node_id="node-999")
    
    # Should fall back to default (Start has no inputs)
    assert order[0] == "Start"


def test_execution_order_with_trigger_mid_workflow():
    """Test trigger can start from middle of workflow graph."""
    nodes = [
        {"id": "load", "name": "Load Data"},
        {"id": "transform", "name": "Transform"},
        {"id": "save", "name": "Save"}
    ]
    connections = {
        "Load Data": {
            "main": {
                "0": [{"node": "Transform", "type": "main", "index": 0}]
            }
        },
        "Transform": {
            "main": {
                "0": [{"node": "Save", "type": "main", "index": 0}]
            }
        }
    }
    
    # Start from Transform (middle of workflow)
    order = build_execution_order(nodes, connections, start_node_id="transform")
    
    # Transform should be first
    assert order[0] == "Transform"
    # Load Data and Save should be in the order
    assert "Load Data" in order
    assert "Save" in order
