#!/usr/bin/env python3
"""Tool to validate all workflow JSON files against the N8N schema."""
import json
import sys
from pathlib import Path
from typing import List, Tuple

# Import the schema module - try direct import first (when installed via poetry)
# If that fails, add parent directory to path (for direct script execution)
try:
    from autometabuilder.workflow.n8n_schema import N8NWorkflow
except ImportError:
    backend_dir = Path(__file__).resolve().parent.parent.parent
    sys.path.insert(0, str(backend_dir))
    from autometabuilder.workflow.n8n_schema import N8NWorkflow


def find_workflow_files(base_path: Path) -> List[Path]:
    """Find all workflow.json files in the packages directory."""
    packages_dir = base_path / "packages"
    if not packages_dir.exists():
        return []
    
    workflow_files = []
    for workflow_file in packages_dir.rglob("workflow.json"):
        workflow_files.append(workflow_file)
    
    return sorted(workflow_files)


def validate_workflow_file(workflow_path: Path) -> Tuple[bool, str]:
    """
    Validate a single workflow JSON file.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"JSON parsing error: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"
    
    # Basic structure checks
    if not isinstance(workflow_data, dict):
        return False, "Workflow data must be an object"
    
    # Check required fields
    required_fields = ["name", "nodes", "connections"]
    missing_fields = [field for field in required_fields if field not in workflow_data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    # Check name
    if not isinstance(workflow_data["name"], str) or not workflow_data["name"]:
        return False, "Field 'name' must be a non-empty string"
    
    # Check nodes
    if not isinstance(workflow_data["nodes"], list):
        return False, "Field 'nodes' must be an array"
    
    if len(workflow_data["nodes"]) < 1:
        return False, "Field 'nodes' must contain at least 1 node (use a start node for blank workflows)"
    
    # Check connections
    if not isinstance(workflow_data["connections"], dict):
        return False, "Field 'connections' must be an object"
    
    # Full validation
    is_valid = N8NWorkflow.validate(workflow_data)
    if not is_valid:
        return False, "Schema validation failed (check node structure, position, types, etc.)"
    
    return True, ""


def main():
    """Main function to validate all workflow files."""
    # Find the autometabuilder directory by looking for the packages subdirectory
    # This works whether run as a script or via poetry command
    script_dir = Path(__file__).resolve().parent.parent
    
    # Verify we found the right directory
    if not (script_dir / "packages").exists():
        print("Error: Could not locate autometabuilder/packages directory")
        return 1
    
    # Find all workflow files
    workflow_files = find_workflow_files(script_dir)
    
    if not workflow_files:
        print("No workflow.json files found in packages directory.")
        return 1
    
    print(f"Found {len(workflow_files)} workflow file(s) to validate\n")
    
    errors = []
    for workflow_path in workflow_files:
        relative_path = workflow_path.relative_to(script_dir)
        is_valid, error_msg = validate_workflow_file(workflow_path)
        
        if is_valid:
            print(f"✓ {relative_path}")
        else:
            print(f"✗ {relative_path}: {error_msg}")
            errors.append((relative_path, error_msg))
    
    print()
    if errors:
        print(f"Validation failed for {len(errors)} file(s):")
        for path, error in errors:
            print(f"  - {path}: {error}")
        return 1
    else:
        print(f"All {len(workflow_files)} workflow file(s) are valid!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
