"""Workflow plugin: create Slack client."""
import os
import logging
from slack_sdk import WebClient

logger = logging.getLogger("autometabuilder")


def run(runtime, inputs):
    """
    Initialize Slack WebClient.
    
    Inputs:
        token: Optional Slack bot token (defaults to SLACK_BOT_TOKEN env var)
        
    Returns:
        dict: Contains the Slack client in result and initialized status
    """
    token = inputs.get("token") or os.environ.get("SLACK_BOT_TOKEN")
    
    if not token:
        logger.warning("Slack client not initialized: SLACK_BOT_TOKEN missing.")
        runtime.context["slack_client"] = None
        return {"result": None, "initialized": False, "error": "SLACK_BOT_TOKEN missing"}
    
    # Create Slack client
    client = WebClient(token=token)
    
    # Store in context for other plugins to use
    runtime.context["slack_client"] = client
    
    logger.info("Slack client initialized successfully.")
    return {"result": client, "initialized": True}
