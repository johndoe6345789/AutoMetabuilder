"""Workflow plugin: send Discord notification."""
import os
import logging
import discord
import asyncio

logger = logging.getLogger("autometabuilder.notifications")


async def _send_discord_notification_async(message: str, token: str, channel_id: str):
    """Send Discord notification asynchronously."""
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
        raise


def run(runtime, inputs):
    """
    Send a notification to Discord.
    
    Inputs:
        message: The message to send
        token: Optional Discord bot token (defaults to DISCORD_BOT_TOKEN env var)
        channel_id: Optional channel ID (defaults to DISCORD_CHANNEL_ID env var)
        
    Returns:
        dict: Contains success status and any error message
    """
    message = inputs.get("message", "")
    token = inputs.get("token") or os.environ.get("DISCORD_BOT_TOKEN")
    channel_id = inputs.get("channel_id") or os.environ.get("DISCORD_CHANNEL_ID")
    
    if not token or not channel_id:
        logger.warning("Discord notification skipped: DISCORD_BOT_TOKEN or DISCORD_CHANNEL_ID missing.")
        return {
            "success": False,
            "skipped": True,
            "error": "DISCORD_BOT_TOKEN or DISCORD_CHANNEL_ID missing"
        }
    
    try:
        asyncio.run(_send_discord_notification_async(message, token, channel_id))
        return {"success": True, "message": "Discord notification sent"}
    except Exception as e:
        logger.error(f"Error running Discord notification: {e}")
        return {"success": False, "error": str(e)}
