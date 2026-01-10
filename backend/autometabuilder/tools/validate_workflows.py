#!/usr/bin/env python3
"""Tool to validate all workflow JSON files against the N8N schema."""
import json
import sys
from pathlib import Path
from typing import List, Tuple

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError:
    print("Error: jsonschema library not found. Install with: poetry add jsonschema")
    sys.exit(1)


def load_schema() -> dict:
    """Load the N8N workflow JSON schema."""
    schema_path = Path(__file__).resolve().parent.parent / "schema" / "n8n-workflow.schema.json"
    
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found at: {schema_path}")
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_workflow_files(base_path: Path) -> List[Path]:
    """Find all workflow.json files in the packages directory."""
    packages_dir = base_path / "packages"
    if not packages_dir.exists():
        return []
    
    workflow_files = []
    for workflow_file in packages_dir.rglob("workflow.json"):
        workflow_files.append(workflow_file)
    
    return sorted(workflow_files)


def validate_workflow_file(workflow_path: Path, schema: dict) -> Tuple[bool, str]:
    """
    Validate a single workflow JSON file against the schema.
    
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
    
    # Validate against schema
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(workflow_data))
    
    if errors:
        # Return the first error with a clear message
        error = errors[0]
        error_path = ".".join(str(p) for p in error.path) if error.path else "root"
        return False, f"{error.message} (at {error_path})"
    
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
    
    # Load the schema
    try:
        schema = load_schema()
    except Exception as e:
        print(f"Error loading schema: {e}")
        return 1
    
    # Find all workflow files
    workflow_files = find_workflow_files(script_dir)
    
    if not workflow_files:
        print("No workflow.json files found in packages directory.")
        return 1
    
    print(f"Found {len(workflow_files)} workflow file(s) to validate\n")
    
    errors = []
    for workflow_path in workflow_files:
        try:
            relative_path = workflow_path.relative_to(script_dir)
        except ValueError:
            # If relative_to fails, use the full path
            relative_path = workflow_path
        
        is_valid, error_msg = validate_workflow_file(workflow_path, schema)
        
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
