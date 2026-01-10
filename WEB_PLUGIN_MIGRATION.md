# Web to Workflow Plugins Migration

## Overview

This document describes the migration of web data access functions and Flask server setup from `autometabuilder/web/data` to workflow plugins in `autometabuilder/workflow/plugins/web`.

## Migration Summary

**Total Plugins Created:** 24  
**Plugin Map Updated:** 91 → 115 total plugins  
**New Plugin Category:** `web.*`

## Why This Migration?

This migration follows the established pattern of converting core backend functionality into reusable workflow plugins, enabling:

1. **Declarative Configuration**: Web operations can be composed in workflow definitions
2. **Visual Workflow Editing**: Operations can be visualized and edited graphically
3. **Composability**: Web plugins can be combined with other workflow plugins
4. **Testability**: Individual operations are isolated and testable
5. **Consistency**: All backend operations follow the same plugin architecture

## Plugin Categories

### 1. Environment Management (2 plugins)

| Plugin | Source | Description |
|--------|--------|-------------|
| `web.get_env_vars` | `web/data/env.py` | Load environment variables from .env file |
| `web.persist_env_vars` | `web/data/env.py` | Write environment variables to .env file |

### 2. File I/O Operations (3 plugins)

| Plugin | Source | Description |
|--------|--------|-------------|
| `web.read_json` | `web/data/json_utils.py` | Read and parse JSON files |
| `web.get_recent_logs` | `web/data/logs.py` | Retrieve recent log entries |
| `web.load_messages` | `web/data/messages_io.py` | Load translation messages from path |

### 3. Translation Management (8 plugins)

| Plugin | Source | Description |
|--------|--------|-------------|
| `web.list_translations` | `web/data/translations.py` | List all available translations |
| `web.load_translation` | `web/data/translations.py` | Load a specific language translation |
| `web.create_translation` | `web/data/translations.py` | Create a new translation |
| `web.update_translation` | `web/data/translations.py` | Update existing translation |
| `web.delete_translation` | `web/data/translations.py` | Delete a translation |
| `web.get_ui_messages` | `web/data/translations.py` | Get UI messages with fallback |
| `web.write_messages_dir` | `web/data/messages_io.py` | Write messages to directory structure |

### 4. Navigation & Metadata (2 plugins)

| Plugin | Source | Description |
|--------|--------|-------------|
| `web.get_navigation_items` | `web/data/navigation.py` | Get navigation menu items |

### 5. Prompt Management (3 plugins)

| Plugin | Source | Description |
|--------|--------|-------------|
| `web.get_prompt_content` | `web/data/prompt.py` | Read prompt content from file |
| `web.write_prompt` | `web/data/prompt.py` | Write prompt content to file |
| `web.build_prompt_yaml` | `web/data/prompt.py` | Build YAML prompt from components |

### 6. Workflow Operations (4 plugins)

| Plugin | Source | Description |
|--------|--------|-------------|
| `web.get_workflow_content` | `web/data/workflow.py` | Read workflow JSON content |
| `web.write_workflow` | `web/data/workflow.py` | Write workflow JSON content |
| `web.load_workflow_packages` | `web/data/workflow.py` | Load all workflow packages |
| `web.summarize_workflow_packages` | `web/data/workflow.py` | Create package summaries |

### 7. Flask Server Setup (4 plugins)

| Plugin | Source | Description |
|--------|--------|-------------|
| `web.create_flask_app` | New | Create and configure Flask app |
| `web.register_blueprint` | New | Register Flask blueprints |
| `web.start_server` | `web/server.py` | Start Flask web server |
| `web.build_context` | `web/routes/context.py` | Build complete API context |

## Usage Examples

### Example 1: Loading Environment Variables

```json
{
  "id": "load_env",
  "type": "web.get_env_vars",
  "name": "Load Environment Variables",
  "parameters": {}
}
```

**Output:**
```json
{
  "result": {
    "OPENAI_API_KEY": "sk-...",
    "GITHUB_TOKEN": "ghp_...",
    "LOG_LEVEL": "INFO"
  }
}
```

### Example 2: Building Prompt YAML

```json
{
  "id": "build_prompt",
  "type": "web.build_prompt_yaml",
  "name": "Build Prompt",
  "parameters": {
    "system_content": "You are a helpful coding assistant",
    "user_content": "Help me write clean code",
    "model": "openai/gpt-4o"
  }
}
```

**Output:**
```yaml
messages:
  - role: system
    content: >-
      You are a helpful coding assistant
  - role: user
    content: >-
      Help me write clean code
model: openai/gpt-4o
```

### Example 3: Setting Up Flask Server

A workflow can now configure and start the Flask server:

```json
{
  "nodes": [
    {
      "id": "create_app",
      "type": "web.create_flask_app",
      "name": "Create Flask App",
      "parameters": {
        "name": "autometabuilder",
        "config": {
          "JSON_SORT_KEYS": false
        }
      }
    },
    {
      "id": "register_context",
      "type": "web.register_blueprint",
      "name": "Register Context Routes",
      "parameters": {
        "blueprint_path": "autometabuilder.web.routes.context.context_bp"
      }
    },
    {
      "id": "register_navigation",
      "type": "web.register_blueprint",
      "name": "Register Navigation Routes",
      "parameters": {
        "blueprint_path": "autometabuilder.web.routes.navigation.navigation_bp"
      }
    },
    {
      "id": "start_server",
      "type": "web.start_server",
      "name": "Start Web Server",
      "parameters": {
        "host": "0.0.0.0",
        "port": 8000
      }
    }
  ]
}
```

### Example 4: Translation Management

```json
{
  "nodes": [
    {
      "id": "list_langs",
      "type": "web.list_translations",
      "name": "List Available Languages"
    },
    {
      "id": "load_en",
      "type": "web.load_translation",
      "name": "Load English",
      "parameters": {
        "lang": "en"
      }
    },
    {
      "id": "create_es",
      "type": "web.create_translation",
      "name": "Create Spanish Translation",
      "parameters": {
        "lang": "es"
      }
    }
  ]
}
```

## Plugin Architecture

All web plugins follow the standard workflow plugin pattern:

```python
def run(runtime, inputs):
    """
    Plugin implementation.
    
    Args:
        runtime: WorkflowRuntime instance with context and store
        inputs: Dictionary of input parameters
        
    Returns:
        Dictionary with 'result' key or 'error' key
    """
    # Implementation
    return {"result": value}
```

### Runtime Context

Flask-related plugins use the runtime context to share the Flask app instance:

- `web.create_flask_app` stores app in `runtime.context["flask_app"]`
- `web.register_blueprint` retrieves app from context
- `web.start_server` retrieves app from context

## Testing

A comprehensive test suite has been added in `backend/tests/test_web_plugins.py` with tests for:

- Plugin map registration
- JSON file reading
- Prompt YAML building
- Flask app creation
- Blueprint registration
- UI message loading
- Translation management
- Workflow package operations
- Context building

Run tests with:
```bash
PYTHONPATH=backend poetry run pytest backend/tests/test_web_plugins.py -v
```

## Backward Compatibility

**Important:** This migration adds new workflow plugins but **does not remove** existing web/data modules. The original functions remain in place and continue to work as before. The workflow plugins are thin wrappers that call the existing functions.

This means:
- ✅ Existing code using `autometabuilder.web.data` continues to work
- ✅ Flask routes continue to function normally
- ✅ New workflows can use the plugin system
- ✅ No breaking changes

## Integration with Existing Systems

The web plugins integrate seamlessly with:

1. **Backend Plugins**: Can be combined with `backend.*` plugins in workflows
2. **Core Plugins**: Can work alongside `core.*` AI and tool execution plugins
3. **Data Plugins**: Can use `dict.*`, `list.*`, `string.*` for data manipulation
4. **Control Flow**: Can use `control.*` and `logic.*` for conditional logic

## Future Enhancements

Potential additions to the web plugin category:

1. **Route Handlers**: Create plugins for individual route handlers
2. **Middleware**: Workflow plugins for Flask middleware
3. **Session Management**: Plugins for session operations
4. **Authentication**: Login/logout workflow plugins
5. **WebSocket Support**: Real-time communication plugins
6. **Static File Serving**: Asset management plugins

## Files Changed

### New Files (27)
- `backend/autometabuilder/workflow/plugins/web/__init__.py`
- `backend/autometabuilder/workflow/plugins/web/web_*.py` (24 plugin files)
- `backend/tests/test_web_plugins.py`

### Modified Files (1)
- `backend/autometabuilder/workflow/plugin_map.json` (added 24 entries)

## Conclusion

This migration successfully converts web data access and Flask server operations into workflow plugins, following the established pattern used for backend plugins. The system now has 115 total plugins covering:

- Backend initialization (13 plugins)
- Core AI operations (7 plugins)
- Data manipulation (40 plugins)
- Logic and control flow (11 plugins)
- Testing utilities (5 plugins)
- Tool execution (7 plugins)
- Utility operations (8 plugins)
- **Web operations (24 plugins)** ← New!

This enables fully declarative workflow-based configuration of the entire AutoMetabuilder system, from backend initialization to web server setup.
