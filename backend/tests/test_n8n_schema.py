"""Tests for n8n workflow schema validation."""
import pytest

from autometabuilder.workflow.n8n_schema import N8NNode, N8NPosition, N8NTrigger, N8NWorkflow


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


def test_n8n_trigger_validation():
    """Test trigger validation."""
    valid_trigger = {
        "nodeId": "webhook-node-1",
        "kind": "webhook",
        "enabled": True,
        "meta": {
            "path": "/api/webhook",
            "method": "POST"
        }
    }
    assert N8NTrigger.validate(valid_trigger)
    
    # Minimal valid trigger
    minimal_trigger = {
        "nodeId": "schedule-node",
        "kind": "schedule"
    }
    assert N8NTrigger.validate(minimal_trigger)
    
    # Test all valid kinds
    for kind in ["webhook", "schedule", "queue", "email", "poll", "manual", "other"]:
        trigger = {"nodeId": "node-1", "kind": kind}
        assert N8NTrigger.validate(trigger)
    
    # Missing required fields
    assert not N8NTrigger.validate({})
    assert not N8NTrigger.validate({"nodeId": "node-1"})
    assert not N8NTrigger.validate({"kind": "webhook"})
    
    # Invalid nodeId
    invalid_trigger = valid_trigger.copy()
    invalid_trigger["nodeId"] = ""
    assert not N8NTrigger.validate(invalid_trigger)
    
    invalid_trigger = valid_trigger.copy()
    invalid_trigger["nodeId"] = 123
    assert not N8NTrigger.validate(invalid_trigger)
    
    # Invalid kind
    invalid_trigger = valid_trigger.copy()
    invalid_trigger["kind"] = "invalid_kind"
    assert not N8NTrigger.validate(invalid_trigger)
    
    # Invalid enabled
    invalid_trigger = valid_trigger.copy()
    invalid_trigger["enabled"] = "true"
    assert not N8NTrigger.validate(invalid_trigger)
    
    # Invalid meta
    invalid_trigger = valid_trigger.copy()
    invalid_trigger["meta"] = "not a dict"
    assert not N8NTrigger.validate(invalid_trigger)


def test_n8n_workflow_with_triggers():
    """Test workflow validation with triggers array."""
    valid_workflow_with_triggers = {
        "name": "Webhook Workflow",
        "nodes": [
            {
                "id": "webhook-1",
                "name": "Webhook Trigger",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [0, 0]
            },
            {
                "id": "process-1",
                "name": "Process Data",
                "type": "n8n-nodes-base.function",
                "typeVersion": 1,
                "position": [300, 0]
            }
        ],
        "connections": {},
        "triggers": [
            {
                "nodeId": "webhook-1",
                "kind": "webhook",
                "enabled": True,
                "meta": {
                    "path": "/api/webhook",
                    "method": "POST"
                }
            }
        ]
    }
    assert N8NWorkflow.validate(valid_workflow_with_triggers)
    
    # Empty triggers array is valid
    workflow_empty_triggers = valid_workflow_with_triggers.copy()
    workflow_empty_triggers["triggers"] = []
    assert N8NWorkflow.validate(workflow_empty_triggers)
    
    # Workflow without triggers is valid (optional field)
    workflow_no_triggers = valid_workflow_with_triggers.copy()
    del workflow_no_triggers["triggers"]
    assert N8NWorkflow.validate(workflow_no_triggers)
    
    # Invalid triggers array (not a list)
    invalid_workflow = valid_workflow_with_triggers.copy()
    invalid_workflow["triggers"] = "not a list"
    assert not N8NWorkflow.validate(invalid_workflow)
    
    # Invalid trigger in array
    invalid_workflow = valid_workflow_with_triggers.copy()
    invalid_workflow["triggers"] = [{"nodeId": "node-1"}]  # missing kind
    assert not N8NWorkflow.validate(invalid_workflow)
    
    # Multiple triggers
    workflow_multiple_triggers = valid_workflow_with_triggers.copy()
    workflow_multiple_triggers["triggers"] = [
        {"nodeId": "webhook-1", "kind": "webhook"},
        {"nodeId": "schedule-1", "kind": "schedule"},
        {"nodeId": "email-1", "kind": "email", "enabled": False}
    ]
    assert N8NWorkflow.validate(workflow_multiple_triggers)
