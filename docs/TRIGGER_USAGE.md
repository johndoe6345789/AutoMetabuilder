# Workflow Trigger Usage Guide

## Overview

As of the latest implementation, the AutoMetabuilder workflow engine now supports workflow triggers. Triggers allow you to explicitly define the entry point of a workflow, making workflow execution more predictable and enabling future support for event-driven workflows.

## What Are Triggers?

Triggers define how and when a workflow should be executed. They specify:
- **Entry Point**: Which node should start the workflow execution
- **Kind**: The type of trigger (manual, webhook, schedule, etc.)
- **Status**: Whether the trigger is enabled or disabled
- **Metadata**: Additional configuration specific to the trigger type

## Current Implementation Status

### ✅ Implemented
- Trigger schema validation (validates trigger structure in workflow JSON)
- Manual trigger support (workflows can specify which node to start from)
- Backward compatibility (workflows without triggers work as before)
- Trigger-based entry point selection

### 🚧 Planned
- Webhook trigger handling
- Schedule trigger execution (cron-based)
- Queue trigger processing
- Email trigger monitoring
- Poll trigger execution

## Using Triggers

### Basic Trigger Definition

Add a `triggers` array to your workflow JSON:

```json
{
  "name": "My Workflow",
  "nodes": [...],
  "connections": {...},
  "triggers": [
    {
      "nodeId": "start_node",
      "kind": "manual",
      "enabled": true,
      "meta": {
        "description": "Manually triggered workflow execution"
      }
    }
  ]
}
```

### Trigger Fields

- **nodeId** (required): The ID of the node where execution should start
- **kind** (required): One of: `manual`, `webhook`, `schedule`, `queue`, `email`, `poll`, `other`
- **enabled** (optional, default: `true`): Whether this trigger is active
- **meta** (optional): Additional metadata for the trigger

### Trigger Kinds

#### Manual Triggers (Currently Supported)
Used for workflows that are manually initiated via CLI or API:

```json
{
  "nodeId": "load_context",
  "kind": "manual",
  "enabled": true,
  "meta": {
    "description": "Start workflow from Load Context node"
  }
}
```

#### Future Trigger Types

**Webhook Triggers** (Planned):
```json
{
  "nodeId": "handle_github_event",
  "kind": "webhook",
  "enabled": true,
  "meta": {
    "path": "/webhooks/github",
    "method": "POST",
    "event_types": ["pull_request", "issues"]
  }
}
```

**Schedule Triggers** (Planned):
```json
{
  "nodeId": "daily_report",
  "kind": "schedule",
  "enabled": true,
  "meta": {
    "cron": "0 9 * * *",
    "timezone": "UTC",
    "description": "Daily report generation at 9 AM UTC"
  }
}
```

## How Triggers Affect Execution

### With Triggers

When a workflow has triggers defined:

1. The execution engine looks for enabled triggers
2. For manual execution, it finds the first enabled `manual` trigger
3. The workflow starts executing from the node specified in the trigger's `nodeId`
4. Execution proceeds according to the connection graph

### Without Triggers (Backward Compatible)

When a workflow has no triggers:

1. The execution engine uses the default behavior
2. Execution starts from nodes with no incoming connections
3. Nodes are executed in topological order based on the connection graph

## Example Workflow

Here's a complete example of a workflow using a manual trigger:

```json
{
  "name": "Data Processing Workflow",
  "active": false,
  "nodes": [
    {
      "id": "load_data",
      "name": "Load Data",
      "type": "backend.load_data",
      "typeVersion": 1,
      "position": [0, 0],
      "parameters": {}
    },
    {
      "id": "transform_data",
      "name": "Transform Data",
      "type": "backend.transform_data",
      "typeVersion": 1,
      "position": [300, 0],
      "parameters": {}
    },
    {
      "id": "save_results",
      "name": "Save Results",
      "type": "backend.save_results",
      "typeVersion": 1,
      "position": [600, 0],
      "parameters": {}
    }
  ],
  "connections": {
    "Load Data": {
      "main": {
        "0": [
          {
            "node": "Transform Data",
            "type": "main",
            "index": 0
          }
        ]
      }
    },
    "Transform Data": {
      "main": {
        "0": [
          {
            "node": "Save Results",
            "type": "main",
            "index": 0
          }
        ]
      }
    }
  },
  "triggers": [
    {
      "nodeId": "load_data",
      "kind": "manual",
      "enabled": true,
      "meta": {
        "description": "Manually triggered data processing workflow"
      }
    }
  ]
}
```

## Multiple Triggers

You can define multiple triggers in a workflow:

```json
{
  "triggers": [
    {
      "nodeId": "webhook_handler",
      "kind": "webhook",
      "enabled": true,
      "meta": {
        "description": "Triggered by GitHub webhook",
        "path": "/webhooks/github"
      }
    },
    {
      "nodeId": "scheduled_check",
      "kind": "schedule",
      "enabled": false,
      "meta": {
        "description": "Daily scheduled run (currently disabled)",
        "cron": "0 10 * * *"
      }
    },
    {
      "nodeId": "manual_run",
      "kind": "manual",
      "enabled": true,
      "meta": {
        "description": "Manual execution for testing"
      }
    }
  ]
}
```

**Note**: The current implementation uses the first enabled `manual` trigger for manual execution. Future implementations will support routing based on trigger kind.

## Best Practices

1. **Always Define Triggers**: Make workflow entry points explicit
   - Makes workflows self-documenting
   - Enables future event-driven features
   - Improves workflow maintainability

2. **Use Descriptive Metadata**: Document the purpose of each trigger
   ```json
   "meta": {
     "description": "Processes GitHub PR webhooks for CI/CD pipeline",
     "event_types": ["pull_request"],
     "priority": "high"
   }
   ```

3. **Start Simple**: Begin with manual triggers
   - Manual triggers are the simplest and most tested
   - Easy to debug and understand
   - Can be extended to other trigger types later

4. **Validate Before Deployment**: Use the validation tool
   ```bash
   poetry run validate-workflows
   ```

5. **Test Trigger-Based Execution**: Ensure your workflow works correctly
   - Test with triggers enabled
   - Test with triggers disabled (backward compatibility)
   - Verify the correct entry point is used

## Migration from Triggerless Workflows

If you have existing workflows without triggers, they will continue to work with default behavior. To add trigger support:

1. Identify the intended entry point node
2. Add a `triggers` array with a manual trigger
3. Set the `nodeId` to your entry point node's ID
4. Validate the workflow
5. Test execution

Example migration:

**Before**:
```json
{
  "name": "My Workflow",
  "nodes": [...],
  "connections": {...}
}
```

**After**:
```json
{
  "name": "My Workflow",
  "nodes": [...],
  "connections": {...},
  "triggers": [
    {
      "nodeId": "first_node_id",
      "kind": "manual",
      "enabled": true,
      "meta": {
        "description": "Manually triggered workflow"
      }
    }
  ]
}
```

## Troubleshooting

### Trigger Not Working

**Problem**: Workflow doesn't start from the expected node

**Solutions**:
- Verify the `nodeId` matches an actual node ID in your workflow (not the node name)
- Check that `enabled` is `true` (or omitted, as true is the default)
- For manual execution, ensure the trigger `kind` is `manual`
- Validate your workflow JSON with `poetry run validate-workflows`

### Invalid Trigger Validation Error

**Problem**: Workflow validation fails with trigger-related errors

**Solutions**:
- Ensure `nodeId` and `kind` are both present (required fields)
- Verify `kind` is one of: `manual`, `webhook`, `schedule`, `queue`, `email`, `poll`, `other`
- Check that `enabled` is a boolean, not a string
- Ensure `meta` is an object (dictionary), not a string or array

### Workflow Ignores Trigger

**Problem**: Workflow executes but doesn't respect the trigger

**Solutions**:
- Check if there are multiple triggers - the first enabled `manual` trigger is used
- Verify the workflow is using the updated execution engine
- Check logs for warnings about trigger configuration

## Technical Details

### Execution Order Algorithm

When a trigger is present:

1. Find the first enabled trigger matching the execution context (currently `manual` for CLI/API execution)
2. Look up the node name by the trigger's `nodeId`
3. Build execution order starting from that node
4. Execute nodes in the determined order

### Code References

- Trigger validation: `backend/autometabuilder/workflow/n8n_schema.py`
- Execution order: `backend/autometabuilder/workflow/execution_order.py`
- Trigger handling: `backend/autometabuilder/workflow/n8n_executor.py`
- Schema definition: `backend/autometabuilder/schema/n8n-workflow.schema.json`

## See Also

- [Workflow Validation Documentation](WORKFLOW_VALIDATION.md)
- [N8N Workflow Schema](../backend/autometabuilder/schema/n8n-workflow.schema.json)
- [Workflow Triggers Roadmap](archive/WORKFLOW_TRIGGERS.md) (archived documentation)

## Future Enhancements

The trigger feature is designed to support future event-driven workflows:

1. **Webhook Triggers**: Respond to HTTP webhooks (GitHub, Slack, etc.)
2. **Scheduled Triggers**: Run workflows on a schedule (cron-based)
3. **Queue Triggers**: Process tasks from message queues
4. **Email Triggers**: React to incoming emails
5. **Poll Triggers**: Periodically check external systems
6. **Conditional Triggers**: Execute based on complex conditions
7. **Trigger Chains**: Link triggers across workflows
8. **Trigger History**: Log and monitor trigger executions

The current manual trigger implementation provides the foundation for these future enhancements.
