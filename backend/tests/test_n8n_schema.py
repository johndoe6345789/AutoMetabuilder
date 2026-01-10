"""Tests for n8n workflow schema validation."""
import pytest

from autometabuilder.workflow.n8n_schema import N8NNode, N8NPosition, N8NWorkflow


def test_n8n_position_validation():
    """Test position validation."""
    assert N8NPosition.validate([0, 0])
    assert N8NPosition.validate([100.5, 200.5])
    assert not N8NPosition.validate([0])
    assert not N8NPosition.validate([0, 0, 0])
    assert not N8NPosition.validate("invalid")
    assert not N8NPosition.validate(None)


def test_n8n_node_validation():
    """Test node validation."""
    valid_node = {
        "id": "node-1",
        "name": "Test Node",
        "type": "core.test",
        "typeVersion": 1,
        "position": [0, 0],
        "parameters": {}
    }
    assert N8NNode.validate(valid_node)
    
    # Missing required fields
    assert not N8NNode.validate({})
    assert not N8NNode.validate({"id": "node-1"})
    
    # Invalid typeVersion
    invalid_node = valid_node.copy()
    invalid_node["typeVersion"] = 0
    assert not N8NNode.validate(invalid_node)
    
    # Invalid position
    invalid_node = valid_node.copy()
    invalid_node["position"] = [0]
    assert not N8NNode.validate(invalid_node)


def test_n8n_workflow_validation():
    """Test workflow validation."""
    valid_workflow = {
        "name": "Test Workflow",
        "nodes": [
            {
                "id": "node-1",
                "name": "Node 1",
                "type": "core.test",
                "typeVersion": 1,
                "position": [0, 0]
            }
        ],
        "connections": {}
    }
    assert N8NWorkflow.validate(valid_workflow)
    
    # Missing required fields
    assert not N8NWorkflow.validate({})
    assert not N8NWorkflow.validate({"name": "Test"})
    
    # Empty nodes array is invalid
    invalid_workflow = valid_workflow.copy()
    invalid_workflow["nodes"] = []
    assert not N8NWorkflow.validate(invalid_workflow)
    
    # Invalid node
    invalid_workflow = valid_workflow.copy()
    invalid_workflow["nodes"] = [{"id": "bad"}]
    assert not N8NWorkflow.validate(invalid_workflow)
