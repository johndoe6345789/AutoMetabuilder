"""Tests for workflow JSON validation tool."""
import json
from pathlib import Path

import pytest

from autometabuilder.tools.validate_workflows import (
    find_workflow_files,
    validate_workflow_file,
)


def test_find_workflow_files():
    """Test that workflow files are found."""
    backend_dir = Path(__file__).parent.parent / "autometabuilder"
    workflow_files = find_workflow_files(backend_dir)
    
    assert len(workflow_files) > 0
    assert all(f.name == "workflow.json" for f in workflow_files)
    assert all(f.exists() for f in workflow_files)


def test_validate_all_workflow_files():
    """Test that all workflow files in packages directory are valid."""
    backend_dir = Path(__file__).parent.parent / "autometabuilder"
    workflow_files = find_workflow_files(backend_dir)
    
    errors = []
    for workflow_path in workflow_files:
        try:
            relative_path = workflow_path.relative_to(backend_dir)
        except ValueError:
            # If relative_to fails (e.g., due to symlinks), use the full path
            relative_path = workflow_path
        
        is_valid, error_msg = validate_workflow_file(workflow_path)
        
        if not is_valid:
            errors.append((relative_path, error_msg))
    
    # Report all errors for debugging
    if errors:
        error_report = "\n".join(f"  - {path}: {error}" for path, error in errors)
        pytest.fail(f"Workflow validation failed for {len(errors)} file(s):\n{error_report}")


def test_validate_minimal_valid_workflow(tmp_path):
    """Test validation of a minimal valid workflow."""
    workflow_data = {
        "name": "Test Workflow",
        "nodes": [
            {
                "id": "node-1",
                "name": "Test Node",
                "type": "core.test",
                "typeVersion": 1,
                "position": [0, 0]
            }
        ],
        "connections": {}
    }
    
    workflow_file = tmp_path / "workflow.json"
    workflow_file.write_text(json.dumps(workflow_data))
    
    is_valid, error_msg = validate_workflow_file(workflow_file)
    assert is_valid, f"Validation failed: {error_msg}"


def test_validate_workflow_with_missing_name(tmp_path):
    """Test validation of workflow missing required 'name' field."""
    workflow_data = {
        "nodes": [
            {
                "id": "node-1",
                "name": "Test Node",
                "type": "core.test",
                "typeVersion": 1,
                "position": [0, 0]
            }
        ],
        "connections": {}
    }
    
    workflow_file = tmp_path / "workflow.json"
    workflow_file.write_text(json.dumps(workflow_data))
    
    is_valid, error_msg = validate_workflow_file(workflow_file)
    assert not is_valid
    assert "name" in error_msg.lower()


def test_validate_workflow_with_empty_nodes(tmp_path):
    """Test validation of workflow with empty nodes array."""
    workflow_data = {
        "name": "Empty Workflow",
        "nodes": [],
        "connections": {}
    }
    
    workflow_file = tmp_path / "workflow.json"
    workflow_file.write_text(json.dumps(workflow_data))
    
    is_valid, error_msg = validate_workflow_file(workflow_file)
    assert not is_valid
    assert "nodes" in error_msg.lower()
    assert "at least 1" in error_msg.lower()


def test_validate_workflow_with_invalid_json(tmp_path):
    """Test validation of file with invalid JSON."""
    workflow_file = tmp_path / "workflow.json"
    workflow_file.write_text("{ invalid json }")
    
    is_valid, error_msg = validate_workflow_file(workflow_file)
    assert not is_valid
    assert "json" in error_msg.lower()


def test_validate_workflow_with_invalid_node(tmp_path):
    """Test validation of workflow with invalid node structure."""
    workflow_data = {
        "name": "Test Workflow",
        "nodes": [
            {
                "id": "node-1",
                # Missing required fields: name, type, typeVersion, position
            }
        ],
        "connections": {}
    }
    
    workflow_file = tmp_path / "workflow.json"
    workflow_file.write_text(json.dumps(workflow_data))
    
    is_valid, error_msg = validate_workflow_file(workflow_file)
    assert not is_valid


def test_validate_workflow_with_triggers(tmp_path):
    """Test validation of workflow with triggers array."""
    workflow_data = {
        "name": "Test Workflow with Triggers",
        "nodes": [
            {
                "id": "webhook-1",
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [0, 0]
            }
        ],
        "connections": {},
        "triggers": [
            {
                "nodeId": "webhook-1",
                "kind": "webhook",
                "enabled": True,
                "meta": {
                    "path": "/api/test"
                }
            }
        ]
    }
    
    workflow_file = tmp_path / "workflow.json"
    workflow_file.write_text(json.dumps(workflow_data))
    
    is_valid, error_msg = validate_workflow_file(workflow_file)
    assert is_valid, f"Validation failed: {error_msg}"
