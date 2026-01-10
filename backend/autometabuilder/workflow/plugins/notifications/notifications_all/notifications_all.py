"""Workflow plugin: send notification to all channels."""
import os
import logging
import asyncio

logger = logging.getLogger("autometabuilder.notifications")


def _send_slack(client, message: str, channel: str):
    """Send Slack notification using provided client."""
    if not client or not channel:
        logger.warning("Slack notification skipped: client or channel missing.")
        return
    
    try:
        from slack_sdk.errors import SlackApiError
        client.chat_postMessage(channel=channel, text=message)
        logger.info("Slack notification sent successfully.")
    except SlackApiError as e:
        logger.error(f"Error sending Slack notification: {e}")


async def _send_discord_async(message: str, token: str, intents, channel_id: str):
    """Send Discord notification asynchronously."""
    import discord
    
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


def _send_discord(message: str, token: str, intents, channel_id: str):
    """Send Discord notification."""
    if not token or not channel_id:
        logger.warning("Discord notification skipped: token or channel_id missing.")
        return
    
    try:
        asyncio.run(_send_discord_async(message, token, intents, channel_id))
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
    
    # Get Slack client from runtime context
    slack_client = runtime.context.get("slack_client")
    slack_channel = os.environ.get("SLACK_CHANNEL")
    
    # Get Discord config from runtime context
    discord_token = runtime.context.get("discord_token")
    discord_intents = runtime.context.get("discord_intents")
    discord_channel_id = os.environ.get("DISCORD_CHANNEL_ID")
    
    # Send to both channels
    _send_slack(slack_client, message, slack_channel)
    _send_discord(message, discord_token, discord_intents, discord_channel_id)
    
    return {
        "success": True,
        "message": "Notifications sent to all channels"
    }
