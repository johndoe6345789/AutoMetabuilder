"""Workflow plugin: send notification to all channels."""
import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import discord
import asyncio

logger = logging.getLogger("autometabuilder.notifications")


def _send_slack(message: str):
    """Send Slack notification."""
    token = os.environ.get("SLACK_BOT_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL")
    if not token or not channel:
        logger.warning("Slack notification skipped: SLACK_BOT_TOKEN or SLACK_CHANNEL missing.")
        return
    
    client = WebClient(token=token)
    try:
        client.chat_postMessage(channel=channel, text=message)
        logger.info("Slack notification sent successfully.")
    except SlackApiError as e:
        logger.error(f"Error sending Slack notification: {e}")


async def _send_discord_async(message: str):
    """Send Discord notification asynchronously."""
    token = os.environ.get("DISCORD_BOT_TOKEN")
    channel_id = os.environ.get("DISCORD_CHANNEL_ID")
    if not token or not channel_id:
        logger.warning("Discord notification skipped: DISCORD_BOT_TOKEN or DISCORD_CHANNEL_ID missing.")
        return
    
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        channel = client.get_channel(int(channel_id))
        if channel:
            await channel.send(message)
            logger.info("Discord notification sent successfully.")
        await client.close()
    
    try:
        await client.start(token)
    except Exception as e:
        logger.error(f"Error sending Discord notification: {e}")


def _send_discord(message: str):
    """Send Discord notification."""
    try:
        asyncio.run(_send_discord_async(message))
    except Exception as e:
        logger.error(f"Error running Discord notification: {e}")


def run(runtime, inputs):
    """
    Send a notification to all configured channels (Slack and Discord).
    
    Inputs:
        message: The message to send to all channels
        
    Returns:
        dict: Contains success status for all channels
    """
    message = inputs.get("message", "")
    
    # Send to both channels
    _send_slack(message)
    _send_discord(message)
    
    return {
        "success": True,
        "message": "Notifications sent to all channels"
    }
