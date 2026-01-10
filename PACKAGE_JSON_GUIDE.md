# Package.json Files in AutoMetabuilder

This document explains the purpose and location of package.json files throughout the AutoMetabuilder project to make them easy to find and understand.

## Overview

AutoMetabuilder uses `package.json` files in two main contexts:

1. **Workflow Plugin Packages** - Define individual workflow plugins
2. **Workflow Template Packages** - Define complete workflow templates

## Workflow Plugin Packages

### Location
```
backend/autometabuilder/workflow/plugins/<category>/<plugin_name>/package.json
```

### Purpose
Each workflow plugin has a `package.json` that defines:
- Plugin name and type
- Entry point (Python file)
- Metadata and categorization

### Structure
```json
{
  "name": "@autometabuilder/plugin_name",
  "version": "1.0.0",
  "description": "Plugin description",
  "main": "plugin_file.py",
  "author": "AutoMetabuilder",
  "license": "MIT",
  "keywords": ["category", "keyword"],
  "metadata": {
    "plugin_type": "category.plugin_name",
    "category": "category"
  }
}
```

### Key Fields
- **`name`**: NPM-style package name (e.g., `@autometabuilder/web_api_navigation`)
- **`main`**: Python file containing the `run()` function
- **`metadata.plugin_type`**: The actual plugin identifier used in workflows (e.g., `web.api_navigation`)
- **`metadata.category`**: Plugin category for organization

### Plugin Discovery
Plugins are **automatically discovered** by scanning for package.json files in the plugins directory. No manual registration required!

### Categories
- `backend/` - Backend initialization plugins
- `core/` - Core workflow operations
- `web/` - Web/Flask server plugins
- `control/` - Control flow plugins
- `logic/` - Logical operations
- `math/` - Mathematical operations
- `string/` - String manipulation
- `list/` - List operations
- `dict/` - Dictionary operations
- `convert/` - Type conversion
- `utils/` - Utility functions

### Finding All Plugin package.json Files
```bash
# Find all plugin package.json files
find backend/autometabuilder/workflow/plugins -name "package.json"

# Count plugins by category
find backend/autometabuilder/workflow/plugins -name "package.json" | \
  cut -d'/' -f5 | sort | uniq -c
```

## Workflow Template Packages

### Location
```
backend/autometabuilder/packages/<workflow_name>/package.json
```

### Purpose
Workflow packages define complete, reusable workflow templates that can be selected and executed.

### Structure
```json
{
  "name": "workflow_name",
  "version": "1.0.0",
  "description": "Workflow description",
  "main": "workflow.json",
  "author": "AutoMetabuilder",
  "metadata": {
    "label": "Human Readable Name",
    "tags": ["tag1", "tag2"],
    "icon": "icon_name",
    "category": "templates"
  }
}
```

### Key Fields
- **`name`**: Workflow identifier (used as `id` in the system)
- **`main`**: Workflow JSON file (usually `workflow.json`)
- **`metadata.label`**: Display name in UI
- **`metadata.tags`**: Tags for filtering/searching
- **`metadata.category`**: Organization category

### Available Workflows
```bash
# List all workflow packages
ls -1 backend/autometabuilder/packages/

# Find all workflow package.json files
find backend/autometabuilder/packages -name "package.json" -maxdepth 2
```

## Example: Creating a New Plugin

### 1. Create Plugin Directory
```bash
mkdir -p backend/autometabuilder/workflow/plugins/web/web_my_plugin
```

### 2. Create package.json
```json
{
  "name": "@autometabuilder/web_my_plugin",
  "version": "1.0.0",
  "description": "My custom plugin",
  "main": "web_my_plugin.py",
  "author": "Your Name",
  "license": "MIT",
  "keywords": ["web", "custom"],
  "metadata": {
    "plugin_type": "web.my_plugin",
    "category": "web"
  }
}
```

### 3. Create Plugin Python File
```python
# web_my_plugin.py
def run(runtime, inputs):
    """Plugin implementation."""
    return {"result": "success"}
```

### 4. Use in Workflow
The plugin will be **automatically discovered** and can be used immediately:
```json
{
  "id": "my_node",
  "name": "My Node",
  "type": "web.my_plugin",
  "parameters": {}
}
```

## Example: Creating a New Workflow Package

### 1. Create Workflow Directory
```bash
mkdir -p backend/autometabuilder/packages/my_workflow
```

### 2. Create package.json
```json
{
  "name": "my_workflow",
  "version": "1.0.0",
  "description": "My custom workflow",
  "main": "workflow.json",
  "author": "Your Name",
  "metadata": {
    "label": "My Custom Workflow",
    "tags": ["custom", "example"],
    "icon": "workflow",
    "category": "templates"
  }
}
```

### 3. Create workflow.json
Create an n8n-style workflow JSON with nodes and connections.

## Quick Reference

### Find All package.json Files
```bash
# All package.json in the project
find backend -name "package.json" -type f

# Only plugin packages
find backend/autometabuilder/workflow/plugins -name "package.json"

# Only workflow packages
find backend/autometabuilder/packages -name "package.json" -maxdepth 2

# Count total
find backend -name "package.json" -type f | wc -l
```

### Validate package.json Files
```bash
# Check for valid JSON
find backend -name "package.json" -exec python3 -m json.tool {} \; > /dev/null

# Check for required fields in plugin packages
find backend/autometabuilder/workflow/plugins -name "package.json" -exec \
  python3 -c "import json, sys; \
  data = json.load(open(sys.argv[1])); \
  assert 'metadata' in data and 'plugin_type' in data['metadata'], \
  f'{sys.argv[1]} missing metadata.plugin_type'" {} \;
```

## Key Differences

| Aspect | Plugin Package | Workflow Package |
|--------|---------------|------------------|
| **Location** | `workflow/plugins/<category>/<name>/` | `packages/<name>/` |
| **Purpose** | Single reusable operation | Complete workflow template |
| **Main File** | Python file with `run()` function | workflow.json |
| **Identifier** | `metadata.plugin_type` | `name` field |
| **Discovery** | Automatic scanning | Loaded via `web.load_workflow_packages` |
| **Usage** | Referenced in workflow nodes | Selected as workflow template |

## Notes

- **No manual registration**: Plugins are automatically discovered by scanning
- **package.json is mandatory**: Every plugin and workflow must have one
- **Consistent naming**: Use `@autometabuilder/` prefix for plugin names
- **Plugin type vs name**: `metadata.plugin_type` is used in workflows, not `name`
- **Case sensitivity**: Plugin types are case-sensitive (e.g., `web.api_navigation`)

## Troubleshooting

### Plugin not found
1. Check `package.json` exists
2. Verify `metadata.plugin_type` field is set
3. Ensure Python file has `run()` function
4. Check Python file name matches `main` field (without .py)

### Workflow package not loading
1. Check `package.json` exists in workflow directory
2. Verify `workflow.json` exists
3. Check `main` field points to correct file
4. Validate JSON syntax

## Resources

- Plugin registry: `backend/autometabuilder/workflow/plugin_registry.py`
- Package loader: `backend/autometabuilder/workflow/plugins/web/web_load_workflow_packages/`
- Example plugins: `backend/autometabuilder/workflow/plugins/*/`
- Example workflows: `backend/autometabuilder/packages/*/`
