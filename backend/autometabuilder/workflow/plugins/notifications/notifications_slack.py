"""Workflow plugin: send Slack notification."""
import os
import logging

logger = logging.getLogger("autometabuilder.notifications")


def run(runtime, inputs):
    """
    Send a notification to Slack.
    
    Inputs:
        message: The message to send
        channel: Optional channel (defaults to SLACK_CHANNEL env var)
        
    Returns:
        dict: Contains success status and any error message
    """
    message = inputs.get("message", "")
    channel = inputs.get("channel") or os.environ.get("SLACK_CHANNEL")
    
    # Get Slack client from runtime context (initialized by backend.create_slack)
    client = runtime.context.get("slack_client")
    
    if not client:
        logger.warning("Slack notification skipped: Slack client not initialized.")
        return {
            "success": False,
            "skipped": True,
            "error": "Slack client not initialized"
        }
    
    if not channel:
        logger.warning("Slack notification skipped: SLACK_CHANNEL missing.")
        return {
            "success": False,
            "skipped": True,
            "error": "SLACK_CHANNEL missing"
        }
    
    try:
        # Import SlackApiError here to handle errors from the client
        from slack_sdk.errors import SlackApiError
        client.chat_postMessage(channel=channel, text=message)
        logger.info("Slack notification sent successfully.")
        return {"success": True, "message": "Slack notification sent"}
    except SlackApiError as e:
        logger.error(f"Error sending Slack notification: {e}")
        return {"success": False, "error": str(e)}
