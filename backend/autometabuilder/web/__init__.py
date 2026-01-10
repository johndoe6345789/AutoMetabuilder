"""Web module: Flask HTTP server and REST API backend.

This module provides the HTTP/REST API backend for the AutoMetabuilder frontend.
It serves the Next.js web UI by handling HTTP requests and managing web application state.

Key Components:
- server.py: Flask application setup and entry point
- routes/: HTTP endpoint handlers (6 blueprints, ~20 endpoints)
- data/: Data access functions shared with workflow plugins
- run_state.py: Bot execution state management
- workflow_graph.py: Workflow visualization for UI

Relationship with Workflow Plugins:
The web module and workflow plugins in workflow/plugins/web/ serve different purposes:
- Web module: External HTTP interface (frontend <-> backend)
- Workflow plugins: Internal workflow operations (workflow automation)

Both systems coexist and complement each other:
- Flask routes call data functions to serve HTTP responses
- Workflow plugins call the same data functions for workflow operations
- Data functions in web/data/ provide shared business logic

This module CANNOT be replaced by workflow plugins because:
1. Workflow plugins cannot run HTTP servers
2. Workflow plugins cannot handle web requests
3. Workflow plugins cannot serve as REST API backends
4. The frontend requires HTTP endpoints to function

See WEB_MODULE_ANALYSIS.md for detailed architecture documentation.
"""
