# Workflow JSON Validation

This repository includes a validation tool for workflow JSON files based on the N8N-style workflow schema defined in ROADMAP.md.

## Schema Definition

The workflow JSON schema is defined in [ROADMAP.md](../ROADMAP.md) (lines 84-430). It defines the structure for N8N-style workflows with the following key requirements:

- **Required fields**: `name`, `nodes`, `connections`
- **Nodes**: Must contain at least 1 node with `id`, `name`, `type`, `typeVersion`, and `position`
- **Connections**: Define the flow between nodes
- **Optional fields**: `id`, `active`, `versionId`, `createdAt`, `updatedAt`, `tags`, `meta`, `settings`, `pinData`, `staticData`, `credentials`, `triggers`

## Validation Tool

### Running the Validation Tool

You can validate all workflow JSON files using the following methods:

#### 1. Using Poetry Command (Recommended)

```bash
poetry run validate-workflows
```

#### 2. Direct Python Execution

```bash
cd backend/autometabuilder
python tools/validate_workflows.py
```

#### 3. As Part of CI

The validation is automatically run as part of the CI pipeline. See `.github/workflows/ci.yml` for the configuration.

### What Gets Validated

The tool automatically discovers and validates all `workflow.json` files in the `backend/autometabuilder/packages/` directory.

Currently, there are 19 workflow files being validated:
- backend_bootstrap
- blank
- conditional_logic_demo
- contextual_iterative_loop
- data_processing_demo
- default_app_workflow
- dict_plugins_test
- game_tick_loop
- iterative_loop
- list_plugins_test
- logic_plugins_test
- math_plugins_test
- plan_execute_summarize
- repo_scan_context
- single_pass
- string_plugins_test
- testing_triangle
- web_server_bootstrap
- web_server_json_routes

### Validation Rules

The validator checks:

1. **JSON Syntax**: File must be valid JSON
2. **Required Fields**: Must have `name`, `nodes`, `connections`
3. **Name Field**: Must be a non-empty string
4. **Nodes Array**: Must contain at least 1 node
5. **Node Structure**: Each node must have:
   - `id` (non-empty string)
   - `name` (non-empty string)
   - `type` (non-empty string)
   - `typeVersion` (number >= 1)
   - `position` (array of 2 numbers [x, y])
6. **Connections**: Must be an object/dict
7. **Triggers** (if present): Must be an array of valid trigger objects

### Example Valid Workflow

```json
{
  "name": "Example Workflow",
  "active": false,
  "nodes": [
    {
      "id": "start",
      "name": "Start",
      "type": "core.start",
      "typeVersion": 1,
      "position": [0, 0],
      "parameters": {}
    }
  ],
  "connections": {},
  "triggers": [
    {
      "nodeId": "start",
      "kind": "manual",
      "enabled": true,
      "meta": {
        "description": "Manually triggered workflow"
      }
    }
  ]
}
```

## Testing

The validation tool has its own test suite:

```bash
# Run validation tests
poetry run pytest backend/tests/test_workflow_validation.py -v

# Run all tests including workflow validation
poetry run pytest
```

## Adding New Workflows

When adding new workflow JSON files:

1. Place the `workflow.json` file in a package directory under `backend/autometabuilder/packages/`
2. Ensure it follows the schema defined in ROADMAP.md
3. Run the validation tool to verify: `poetry run validate-workflows`
4. The validation will automatically run in CI when you push your changes

## Common Issues

### Empty Nodes Array

**Error**: `Field 'nodes' must contain at least 1 node`

**Solution**: Add at least one node to the workflow. Even blank templates need a starting node:

```json
{
  "name": "Blank Canvas",
  "nodes": [
    {
      "id": "start",
      "name": "Start",
      "type": "core.start",
      "typeVersion": 1,
      "position": [0, 0],
      "parameters": {}
    }
  ],
  "connections": {}
}
```

### Missing Required Fields

**Error**: `Missing required fields: name, nodes`

**Solution**: Ensure your workflow JSON includes all required top-level fields: `name`, `nodes`, and `connections`.

### Invalid Node Structure

**Error**: `Schema validation failed (check node structure, position, types, etc.)`

**Solution**: Verify each node has all required fields and correct types. Common issues:
- Missing `position` array
- `typeVersion` less than 1
- Empty strings for `id`, `name`, or `type`
- Position not being an array of exactly 2 numbers

## Implementation Details

The validation is implemented in:
- **Validator Module**: `backend/autometabuilder/workflow/n8n_schema.py`
- **Validation Tool**: `backend/autometabuilder/tools/validate_workflows.py`
- **Tests**: `backend/tests/test_workflow_validation.py`
- **Schema Tests**: `backend/tests/test_n8n_schema.py`
