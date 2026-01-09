"""Workflow engine runner."""


class WorkflowEngine:
    """Run workflow configs through a node executor."""
    def __init__(self, workflow_config, node_executor, logger):
        self.workflow_config = workflow_config or {}
        self.node_executor = node_executor
        self.logger = logger

    def execute(self):
        """Execute the workflow config."""
        nodes = self.workflow_config.get("nodes")
        if not isinstance(nodes, list):
            self.logger.error("Workflow config missing nodes list.")
            return
        self.node_executor.execute_nodes(nodes)
