"""Workflow plugin: send Slack notification."""
import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger("autometabuilder.notifications")


def run(runtime, inputs):
    """
    Send a notification to Slack.
    
    Inputs:
        message: The message to send
        token: Optional Slack bot token (defaults to SLACK_BOT_TOKEN env var)
        channel: Optional channel (defaults to SLACK_CHANNEL env var)
        
    Returns:
        dict: Contains success status and any error message
    """
    message = inputs.get("message", "")
    token = inputs.get("token") or os.environ.get("SLACK_BOT_TOKEN")
    channel = inputs.get("channel") or os.environ.get("SLACK_CHANNEL")
    
    if not token or not channel:
        logger.warning("Slack notification skipped: SLACK_BOT_TOKEN or SLACK_CHANNEL missing.")
        return {
            "success": False,
            "skipped": True,
            "error": "SLACK_BOT_TOKEN or SLACK_CHANNEL missing"
        }
    
    client = WebClient(token=token)
    try:
        client.chat_postMessage(channel=channel, text=message)
        logger.info("Slack notification sent successfully.")
        return {"success": True, "message": "Slack notification sent"}
    except SlackApiError as e:
        logger.error(f"Error sending Slack notification: {e}")
        return {"success": False, "error": str(e)}
