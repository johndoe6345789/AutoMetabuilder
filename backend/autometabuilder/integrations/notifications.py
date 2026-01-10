import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import discord
import asyncio

logger = logging.getLogger("autometabuilder.notifications")

def send_slack_notification(message: str):
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

async def send_discord_notification_async(message: str):
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

def send_discord_notification(message: str):
    try:
        asyncio.run(send_discord_notification_async(message))
    except Exception as e:
        logger.error(f"Error running Discord notification: {e}")

def notify_all(message: str):
    send_slack_notification(message)
    send_discord_notification(message)
