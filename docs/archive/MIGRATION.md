# Migration Guide: N8N Workflow Schema

## Overview

AutoMetabuilder has migrated from a legacy workflow format to the **n8n workflow schema**. This is a **breaking change** that provides explicit connection modeling for visual workflow canvases.

## What Changed

### Old Format (Legacy)
```json
{
  "nodes": [
    {
      "id": "load_context",
      "type": "core.load_context",
      "outputs": {
        "context": "sdlc_context"
      }
    },
    {
      "id": "seed_messages",
      "type": "core.seed_messages",
      "inputs": {
        "context": "$sdlc_context"
      }
    }
  ]
}
```

### New Format (N8N)
```json
{
  "name": "My Workflow",
  "active": false,
  "nodes": [
    {
      "id": "load_context",
      "name": "Load Context",
      "type": "core.load_context",
      "typeVersion": 1,
      "position": [0, 0],
      "parameters": {}
    },
    {
      "id": "seed_messages",
      "name": "Seed Messages",
      "type": "core.seed_messages",
      "typeVersion": 1,
      "position": [300, 0],
      "parameters": {}
    }
  ],
  "connections": {
    "Load Context": {
      "main": {
        "0": [
          {
            "node": "Seed Messages",
            "type": "main",
            "index": 0
          }
        ]
      }
    }
  }
}
```

## Key Differences

1. **Explicit Connections**: Connections are no longer implicit via variable bindings (`$varname`) but explicit in a `connections` object
2. **Node Positions**: Each node now has a `position` array `[x, y]` for canvas placement
3. **Type Versioning**: Nodes include a `typeVersion` field for schema evolution
4. **Node Names**: Nodes have both an `id` and a human-readable `name`
5. **Parameters**: Node inputs are now in a `parameters` object instead of `inputs`
6. **Workflow Metadata**: Top-level workflow has `name`, `active`, and optional `settings`

## Package Structure Changes

### Old Structure
```
workflow_packages/
  ├── blank.json
  ├── single_pass.json
  └── iterative_loop.json
```

### New Structure (NPM-style)
```
packages/
  ├── blank/
  │   ├── package.json
  │   └── workflow.json
  ├── single_pass/
  │   ├── package.json
  │   └── workflow.json
  └── iterative_loop/
      ├── package.json
      └── workflow.json
```

Each package now has:
- `package.json` - Metadata (name, version, description, keywords, license)
- `workflow.json` - The n8n workflow definition

## Migration Steps

### For Existing Workflows

1. **Add required n8n fields** to each node:
   - `name`: Human-readable name
   - `typeVersion`: Set to `1`
   - `position`: Canvas coordinates `[x, y]`

2. **Move inputs to parameters**:
   - Old: `"inputs": {"messages": "$messages"}`
   - New: `"parameters": {}`

3. **Build explicit connections**:
   - Identify data flow from `outputs` → `inputs` with `$` prefixes
   - Create `connections` object mapping source → targets

4. **Add workflow metadata**:
   - `name`: Workflow name
   - `active`: Boolean (usually `false`)
   - `connections`: Connection map

### Example Converter

Use the provided converter utility:

```python
from autometabuilder.workflow.n8n_converter import convert_to_n8n

legacy_workflow = {...}  # Old format
n8n_workflow = convert_to_n8n(legacy_workflow)
```

## API Changes

### Removed
- Legacy workflow format support in engine
- Variable binding resolution (`$varname`)
- Implicit connection inference

### Added
- N8N schema validation (`n8n_schema.py`)
- Explicit connection executor (`n8n_executor.py`)
- Execution order builder (`execution_order.py`)
- NPM-style package loader (`package_loader.py`)

## Error Handling

If you try to load a legacy workflow, you'll get:

```
ValueError: Only n8n workflow format is supported
```

## Benefits

1. **Visual Canvas Ready**: Positions enable drag-and-drop workflow builders
2. **Explicit Data Flow**: Clear connection visualization
3. **Schema Versioning**: `typeVersion` enables backward compatibility
4. **Standard Format**: Compatible with n8n ecosystem and tooling
5. **Better Modularity**: NPM-style packages with metadata

## References

- N8N Schema: See `ROADMAP.md` lines 84-404
- N8N Documentation: https://docs.n8n.io/workflows/
- Package Structure: `backend/autometabuilder/packages/`
