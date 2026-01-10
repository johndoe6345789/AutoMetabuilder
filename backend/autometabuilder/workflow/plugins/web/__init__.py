"""Web workflow plugins: Enable web operations in declarative workflows.

These plugins provide workflow-based access to web data operations, enabling
declarative workflows to interact with web-related functionality.

Purpose:
These plugins wrap data access functions from autometabuilder.web.data to make
them available as workflow nodes. This enables:
- Declarative workflow definitions for web operations
- Visual workflow editing with web data access
- Composable web operations in n8n workflows
- Automated web data processing pipelines

Available Plugins (24 total):

Environment Management:
- web.get_env_vars - Load environment variables
- web.persist_env_vars - Save environment variables

File I/O:
- web.read_json - Read JSON files
- web.get_recent_logs - Get recent log entries
- web.load_messages - Load translation messages

Translation Management:
- web.list_translations - List available translations
- web.load_translation - Load a translation
- web.create_translation - Create new translation
- web.update_translation - Update translation
- web.delete_translation - Delete translation
- web.get_ui_messages - Get UI messages with fallback
- web.write_messages_dir - Write messages to directory

Navigation & Metadata:
- web.get_navigation_items - Get navigation menu items

Prompt Management:
- web.get_prompt_content - Read prompt content
- web.write_prompt - Write prompt content
- web.build_prompt_yaml - Build YAML prompt

Workflow Operations:
- web.get_workflow_content - Read workflow JSON
- web.write_workflow - Write workflow JSON
- web.load_workflow_packages - Load workflow packages
- web.summarize_workflow_packages - Summarize packages

Flask Server Setup:
- web.create_flask_app - Create Flask application
- web.register_blueprint - Register Flask blueprints
- web.start_server - Start Flask server
- web.build_context - Build API context

Relationship with Web Module:
These workflow plugins complement (not replace) the web module:
- Web module (autometabuilder.web): HTTP server for frontend UI
- Workflow plugins: Enable web operations inside workflows
- Both use the same data functions from web.data/

Example Usage:
```json
{
  "nodes": [
    {
      "id": "load_env",
      "type": "web.get_env_vars",
      "name": "Load Environment"
    },
    {
      "id": "load_prompt",
      "type": "web.get_prompt_content",
      "name": "Load Prompt"
    }
  ]
}
```

See docs/archive/WEB_PLUGIN_MIGRATION.md for migration details and examples.
"""
