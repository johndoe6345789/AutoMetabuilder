# End-to-End Testing for AutoMetabuilder Backend

This document explains how to run and understand the E2E tests for the AutoMetabuilder backend after the migration to workflows.

## Overview

The E2E tests verify that the backend API works correctly after the major migration to workflow-based architecture. These tests use Flask's test client to verify API endpoints without needing to start an actual server.

## Test File

**Location**: `backend/tests/test_backend_e2e.py`

## Running the Tests

### Run All E2E Tests

```bash
PYTHONPATH=backend pytest backend/tests/test_backend_e2e.py -v
```

### Run Specific Test Class

```bash
# Test workflow endpoints only
PYTHONPATH=backend pytest backend/tests/test_backend_e2e.py::TestWorkflowEndpoints -v

# Test navigation and translation endpoints
PYTHONPATH=backend pytest backend/tests/test_backend_e2e.py::TestNavigationAndTranslation -v
```

### Run Single Test

```bash
PYTHONPATH=backend pytest backend/tests/test_backend_e2e.py::TestWorkflowEndpoints::test_workflow_graph -v
```

## Test Coverage

### TestWorkflowEndpoints
Tests workflow-related API endpoints:
- `test_workflow_graph` - GET /api/workflow/graph
- `test_workflow_plugins` - GET /api/workflow/plugins  
- `test_workflow_packages` - GET /api/workflow/packages

### TestNavigationAndTranslation
Tests navigation and i18n endpoints:
- `test_navigation` - GET /api/navigation
- `test_translation_options` - GET /api/translation-options

### TestBasicFunctionality
Basic functionality tests:
- `test_json_response_format` - Verifies JSON response format

## What Makes These Tests E2E

These tests verify the **complete workflow system** from end to end:

1. **Workflow Package Loading** - Tests load the `web_server_json_routes` workflow package
2. **Workflow Execution** - Executes the complete workflow to build the Flask app
3. **Route Registration** - Routes are registered via the `web.register_routes` plugin
4. **API Handler Plugins** - Each route calls a specific plugin handler
5. **Data Layer** - Plugins use the data access layer
6. **Response Validation** - Full request/response cycle is tested

This validates the entire architecture works together.

## Key Features Tested

### JSON-Based Route Definitions
Routes are defined declaratively in workflow JSON:
```json
{
  "type": "web.register_routes",
  "parameters": {
    "routes": [
      {
        "path": "/api/navigation",
        "handler": "web.api_navigation"
      }
    ]
  }
}
```

### Automatic Plugin Discovery
Plugins are discovered automatically by scanning `package.json` files:
- No manual plugin map maintenance
- 135+ plugins discovered automatically
- Plugins can be added without registration

### Workflow-Based Server
The Flask server is built through workflow execution:
- Logging configuration
- Environment loading
- App creation
- Route registration
- All configured via JSON workflow

## Expected Output

### Successful Run
```
============================= test session starts ==============================
...
backend/tests/test_backend_e2e.py::TestWorkflowEndpoints::test_workflow_graph PASSED
backend/tests/test_backend_e2e.py::TestWorkflowEndpoints::test_workflow_plugins PASSED
backend/tests/test_backend_e2e.py::TestWorkflowEndpoints::test_workflow_packages PASSED
backend/tests/test_backend_e2e.py::TestNavigationAndTranslation::test_navigation PASSED
backend/tests/test_backend_e2e.py::TestNavigationAndTranslation::test_translation_options PASSED
backend/tests/test_backend_e2e.py::TestBasicFunctionality::test_json_response_format PASSED
============================== 6 passed in 1.27s ===============================
```

### Test Failures
If tests fail, check:
1. **Plugin errors** - Some plugins may fail to load (this is expected, they're logged as warnings)
2. **Missing files** - metadata.json or other files may not exist (tests handle this gracefully)
3. **Import errors** - Ensure PYTHONPATH is set correctly

## Common Issues

### Plugin Registration Warnings
You may see warnings like:
```
ERROR Failed to register plugin utils.map_list: No module named 'value_helpers'
```

These are expected and don't affect the tests. These plugins have import issues but aren't needed for the web server functionality.

### Metadata Not Found
Some endpoints may return 500 if `metadata.json` doesn't exist. Tests handle this gracefully as these files are optional.

## Dependencies

The tests require:
```bash
pip install pytest flask requests pyyaml python-dotenv
```

Or use the full project dependencies:
```bash
pip install -r requirements.txt  # if exists
# or
pip install pytest flask PyGithub openai python-dotenv tenacity slack-sdk discord.py
```

## Test Architecture

### Fixtures

**`flask_app` fixture**:
- Loads `web_server_json_routes` workflow package
- Removes `start_server` node to prevent blocking
- Executes workflow to build Flask app
- Returns configured Flask app

**`client` fixture**:
- Creates Flask test client
- Used to make test requests
- No actual server needed

### Workflow Used

The tests use the **web_server_json_routes** workflow package, which demonstrates:
- JSON-based route definitions
- Plugin-based request handlers  
- Workflow-driven server configuration

Location: `backend/autometabuilder/packages/web_server_json_routes/`

## Comparison with Other Tests

### vs test_ajax_contracts.py
- **test_ajax_contracts.py**: Uses old route structure with Python blueprints
- **test_backend_e2e.py**: Uses new JSON route structure

### vs Integration Tests
- Integration tests focus on individual plugins
- E2E tests verify the complete workflow system

## Continuous Integration

These tests should be run as part of CI/CD:

```yaml
# Example GitHub Actions
- name: Run E2E Tests
  run: |
    PYTHONPATH=backend pytest backend/tests/test_backend_e2e.py -v
```

## Future Enhancements

Potential additions to E2E tests:
- [ ] Test POST/PUT/DELETE endpoints
- [ ] Test error handling and validation
- [ ] Test authentication/authorization
- [ ] Test with real database
- [ ] Performance/load testing
- [ ] Test all workflow packages

## Related Documentation

- **PACKAGE_JSON_GUIDE.md** - Understanding package.json files
- **MIGRATION_SUMMARY.md** - Details of the workflow migration
- **backend/tests/README.md** - Overview of all tests

## Questions?

If tests fail unexpectedly:
1. Check the test output for specific error messages
2. Verify PYTHONPATH is set: `PYTHONPATH=backend`
3. Ensure dependencies are installed
4. Check that workflow packages exist: `ls backend/autometabuilder/packages/`
5. Verify plugins can be discovered: `PYTHONPATH=backend python3 -c "from autometabuilder.workflow.plugin_registry import scan_plugins; print(len(scan_plugins()))"`

The E2E tests confirm that the backend works correctly after the major migration to workflows!
