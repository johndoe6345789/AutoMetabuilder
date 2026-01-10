"""Workflow engine package.

This package provides a declarative workflow engine that executes n8n-style workflows.

Core Modules:
    engine.py - Main workflow engine and execution coordinator
    runtime.py - Runtime context and state management
    
Execution:
    n8n_executor.py - N8N workflow format executor
    node_executor.py - Individual node execution
    execution_order.py - Topological sort for node execution order
    loop_executor.py - Loop iteration execution
    
N8N Support:
    n8n_schema.py - N8N workflow schema definitions
    n8n_converter.py - Convert legacy workflows to N8N format
    workflow_adapter.py - Workflow format adapter
    
Plugin System:
    plugin_loader.py - Plugin loading utilities
    plugin_registry.py - Plugin registration and discovery
    plugin_map.json - Plugin name to module path mapping
    plugins/ - Organized workflow plugins by category
    
Utilities:
    input_resolver.py - Input value resolution and variable binding
    value_helpers.py - Value type checking and conversion helpers
    tool_runner.py - Tool execution wrapper
    tool_calls_handler.py - AI tool calls processing
"""

