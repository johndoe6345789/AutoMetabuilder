# AutoMetabuilder Test Suite

## Running Tests

Run all tests:
```bash
pytest backend/tests/
```

Run specific test files:
```bash
pytest backend/tests/test_main.py
pytest backend/tests/test_workflow_plugins.py
```

Run with verbose output:
```bash
pytest backend/tests/ -v
```

## Test Structure

### Core Tests (Always Passing)
- `test_main.py` - Tests for main utility functions
- `test_metadata.py` - Tests for metadata loading
- `test_n8n_schema.py` - Tests for N8N workflow schema validation
- `test_roadmap.py` - Tests for roadmap utilities
- `test_workflow_plugins.py` - Tests for workflow plugin system (logic, math, string, list, dict plugins)
- `test_unit_testing_plugins.py` - Tests for testing framework plugins

### Integration Tests (Require Dependencies)
- `test_ajax_contracts.py` - Tests for API endpoints (requires Flask and workflow execution)
- `test_web_plugins.py` - Tests for web-specific plugins (requires Flask)
- `test_workflow_graph.py` - Tests for workflow graph building

## Known Issues

### Missing Optional Dependencies
Some tests require optional dependencies that may not be installed:
- `flask` - Required for web server functionality
- `github` (PyGithub) - Required for GitHub integration
- `openai` - Required for AI request plugins
- `python-dotenv` - Required for environment loading
- `tenacity` - Required for retry logic

To install all dependencies:
```bash
pip install flask PyGithub openai python-dotenv tenacity
```

### Workflow-Based Architecture
The system has been refactored to use a workflow-based architecture. Some plugins that were previously static imports now need to be invoked through the workflow system:

1. **Server Setup**: The Flask server is no longer a static module but is built dynamically through workflow execution (see `packages/web_server_bootstrap/workflow.json`)

2. **Plugin Imports**: Some plugins have import path issues that need fixing:
   - `web.build_context` references old route structure
   - Various plugins may reference `autometabuilder.workflow.plugins.*_helpers` modules

3. **Test Adaptation**: Tests should use the workflow execution model where appropriate (principle: "if in doubt, use the workflow")

## Test Philosophy

**Primary Principle**: When in doubt, use the workflow.

The workflow system is the primary interface for the application. Tests should:
1. Execute workflows to build/configure components
2. Use workflow plugins for data access
3. Avoid direct imports of implementation details where possible

## Current Status

- ✅ 36 core tests passing
- ⚠️ 11 tests require dependencies or refactoring
- 📝 Test suite documented and configured with `conftest.py`
