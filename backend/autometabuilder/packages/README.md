# Workflow Packages

This directory contains workflow packages in NPM-style format. Each package is a self-contained workflow with metadata.

## Structure

Each package is a directory containing:

### package.json
Metadata about the workflow package:
```json
{
  "name": "package-name",
  "version": "1.0.0",
  "description": "Human-readable description",
  "author": "AutoMetabuilder",
  "license": "MIT",
  "keywords": ["tag1", "tag2"],
  "main": "workflow.json",
  "metadata": {
    "label": "translation.key",
    "description": "translation.key",
    "tags": ["category"],
    "icon": "icon-name",
    "category": "templates"
  }
}
```

### workflow.json
The N8N workflow definition:
```json
{
  "name": "Workflow Name",
  "active": false,
  "nodes": [...],
  "connections": {...}
}
```

## Available Packages

### Workflow Templates
- **blank**: Empty workflow canvas starter
- **single_pass**: Single AI request + tool execution
- **iterative_loop**: Looping AI agent with tool calls
- **contextual_iterative_loop**: Context loading + iterative loop
- **plan_execute_summarize**: Planning workflow with summary
- **testing_triangle**: Lint + unit + UI test pipeline
- **repo_scan_context**: Repository file scanning
- **game_tick_loop**: Game engine tick simulation

### Plugin Testing Packages
These packages test the correctness of workflow plugins using the `test.*` assertion plugins:

- **logic_plugins_test**: Tests for logic plugins (and, or, equals, gt, lt, gte, lte, xor, in)
- **math_plugins_test**: Tests for math plugins (add, multiply, subtract, divide, min, max)
- **string_plugins_test**: Tests for string plugins (concat, upper, lower, split, length)
- **list_plugins_test**: Tests for list plugins (concat, length, slice, find)
- **dict_plugins_test**: Tests for dict plugins (get, set, keys, merge)

## Creating New Packages

1. Create a directory: `mkdir packages/my-workflow`
2. Add `package.json` with metadata
3. Add `workflow.json` with N8N schema
4. Ensure workflow has required fields:
   - nodes with id, name, type, typeVersion, position
   - connections mapping
   - workflow name

## Loading Packages

Packages are loaded via `load_workflow_packages()` in `web/data/workflow.py`:

```python
from autometabuilder.data import load_workflow_packages

packages = load_workflow_packages()
```

Each package is validated and includes both metadata and workflow definition.
