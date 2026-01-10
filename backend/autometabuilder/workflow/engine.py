"""Workflow engine runner."""
from .workflow_adapter import WorkflowAdapter, is_n8n_workflow


class WorkflowEngine:
    """Run workflow configs through a node executor."""
    def __init__(self, workflow_config, node_executor, logger, runtime=None, plugin_registry=None):
        self.workflow_config = workflow_config or {}
        self.node_executor = node_executor
        self.logger = logger
        self.runtime = runtime
        self.plugin_registry = plugin_registry
        
        # Create adapter if we have runtime and plugin registry
        if runtime and plugin_registry:
            self.adapter = WorkflowAdapter(node_executor, runtime, plugin_registry)
        else:
            self.adapter = None

    def execute(self):
        """Execute the workflow config."""
        # Use adapter if available and workflow is n8n format
        if self.adapter and is_n8n_workflow(self.workflow_config):
            self.adapter.execute(self.workflow_config)
            return
        
        # Fallback to legacy execution
        nodes = self.workflow_config.get("nodes")
        if not isinstance(nodes, list):
            self.logger.error("Workflow config missing nodes list.")
            return
        self.node_executor.execute_nodes(nodes)
