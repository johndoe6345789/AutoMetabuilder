# Workflow Triggers Documentation

## Overview

Workflow triggers define how and when a workflow should be executed. They are part of the n8n workflow schema and provide a standardized way to specify workflow entry points.

## Trigger Schema

According to `n8n_schema.py`, triggers have the following structure:

```json
{
  "nodeId": "node_id",           // ID of the node to start execution from
  "kind": "manual|webhook|...",  // Type of trigger
  "enabled": true,               // Whether trigger is active
  "meta": {                      // Optional metadata
    "description": "..."
  }
}
```

### Trigger Kinds

Valid trigger types defined in `N8NTrigger.VALID_KINDS`:
- **manual**: Manually initiated workflow (CLI, API call)
- **webhook**: HTTP webhook endpoint
- **schedule**: Cron/scheduled execution
- **queue**: Message queue trigger
- **email**: Email-based trigger
- **poll**: Polling-based trigger
- **other**: Custom trigger types

## Current Usage

### Example: Single Pass Workflow

The `single_pass` workflow package demonstrates trigger usage:

```json
{
  "name": "Single Pass",
  "nodes": [...],
  "connections": {...},
  "triggers": [
    {
      "nodeId": "load_context",
      "kind": "manual",
      "enabled": true,
      "meta": {
        "description": "Manually triggered single-pass workflow execution"
      }
    }
  ]
}
```

## Potential Use Cases for Different Trigger Types

### 1. Manual Triggers
**Current Implementation**: Default for most workflows
- CLI-initiated workflows
- API-triggered workflows
- Development/testing workflows

### 2. Webhook Triggers (Future)
**Use Cases**:
- GitHub webhook integration (PR creation, issue updates)
- Slack command integration
- Discord bot commands
- External service integrations

**Example Configuration**:
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

### 3. Schedule Triggers (Future)
**Use Cases**:
- Daily roadmap analysis
- Weekly progress reports
- Periodic issue cleanup
- Automated dependency updates

**Example Configuration**:
```json
{
  "nodeId": "analyze_roadmap",
  "kind": "schedule",
  "enabled": true,
  "meta": {
    "cron": "0 9 * * *",
    "timezone": "UTC",
    "description": "Daily roadmap analysis at 9 AM UTC"
  }
}
```

### 4. Queue Triggers (Future)
**Use Cases**:
- Task queue processing
- Background job execution
- Async workflow execution
- Load balancing

**Example Configuration**:
```json
{
  "nodeId": "process_task",
  "kind": "queue",
  "enabled": true,
  "meta": {
    "queue_name": "workflow_tasks",
    "concurrency": 5
  }
}
```

### 5. Email Triggers (Future)
**Use Cases**:
- Email-based task creation
- Support ticket workflows
- Email monitoring

**Example Configuration**:
```json
{
  "nodeId": "process_email",
  "kind": "email",
  "enabled": true,
  "meta": {
    "filter": "subject:contains('[Task]')",
    "folder": "inbox"
  }
}
```

### 6. Poll Triggers (Future)
**Use Cases**:
- Monitoring external APIs
- Checking for file changes
- Detecting state changes

**Example Configuration**:
```json
{
  "nodeId": "check_api_status",
  "kind": "poll",
  "enabled": true,
  "meta": {
    "interval": "5m",
    "endpoint": "https://api.example.com/status"
  }
}
```

## Implementation Status

### ✅ Implemented
- Trigger schema validation (`N8NTrigger.validate()`)
- Trigger array validation in workflows
- Manual trigger support (default execution)

### 🚧 Partially Implemented
- Trigger metadata storage
- Trigger-based entry point selection

### ❌ Not Yet Implemented
- Webhook trigger handling
- Schedule trigger execution
- Queue trigger processing
- Email trigger monitoring
- Poll trigger execution
- Trigger event routing

## Recommendations for Better Trigger Utilization

### 1. Add Trigger Execution Logic

Create a `TriggerManager` class in the workflow engine:

```python
class TriggerManager:
    """Manage workflow trigger execution."""
    
    def get_enabled_triggers(self, workflow):
        """Return list of enabled triggers."""
        return [t for t in workflow.get("triggers", []) if t.get("enabled", True)]
    
    def get_start_nodes(self, workflow, trigger_kind=None):
        """Get start node IDs for given trigger kind."""
        triggers = self.get_enabled_triggers(workflow)
        if trigger_kind:
            triggers = [t for t in triggers if t["kind"] == trigger_kind]
        return [t["nodeId"] for t in triggers]
```

### 2. Support Multiple Triggers per Workflow

Current workflows support multiple triggers but execution starts from a fixed point. Enable:
- Trigger-specific entry points
- Parallel trigger execution
- Trigger-specific contexts

### 3. Create Trigger-Specific Workflow Packages

Add workflow packages for different trigger types:
- `webhook_handler/` - HTTP webhook workflows
- `scheduled_tasks/` - Cron-based workflows
- `event_processor/` - Queue-based workflows

### 4. Add Trigger Plugins

Create workflow plugins for trigger management:
- `trigger.register` - Register new triggers
- `trigger.enable` - Enable/disable triggers
- `trigger.list` - List workflow triggers
- `trigger.invoke` - Manually invoke a trigger

### 5. Web UI Integration

Add trigger management to the web interface:
- List all triggers across workflows
- Enable/disable triggers dynamically
- View trigger execution history
- Configure trigger metadata

## Migration Path

For existing workflows without triggers, add default manual trigger:

```json
{
  "triggers": [
    {
      "nodeId": "first_node_id",
      "kind": "manual",
      "enabled": true
    }
  ]
}
```

## Best Practices

1. **Always define triggers** - Make workflow entry points explicit
2. **Use descriptive metadata** - Document trigger purpose and configuration
3. **Start with manual triggers** - Simplest to implement and test
4. **Plan for multiple triggers** - Design workflows to support different entry points
5. **Validate trigger configuration** - Use `N8NTrigger.validate()` before execution
6. **Document trigger requirements** - List prerequisites in workflow package README

## Example: Multi-Trigger Workflow

```json
{
  "name": "CI/CD Pipeline",
  "nodes": [...],
  "connections": {...},
  "triggers": [
    {
      "nodeId": "webhook_handler",
      "kind": "webhook",
      "enabled": true,
      "meta": {
        "description": "Triggered by GitHub PR webhook",
        "path": "/webhooks/github/pr"
      }
    },
    {
      "nodeId": "scheduled_check",
      "kind": "schedule",
      "enabled": true,
      "meta": {
        "description": "Daily scheduled PR review",
        "cron": "0 10 * * *"
      }
    },
    {
      "nodeId": "manual_run",
      "kind": "manual",
      "enabled": true,
      "meta": {
        "description": "Manually triggered pipeline run"
      }
    }
  ]
}
```

## Future Enhancements

1. **Trigger History** - Log all trigger executions
2. **Trigger Metrics** - Track trigger performance
3. **Trigger Dependencies** - Define trigger prerequisites
4. **Trigger Chains** - Link triggers across workflows
5. **Conditional Triggers** - Add trigger conditions
6. **Trigger Testing** - Unit test framework for triggers
