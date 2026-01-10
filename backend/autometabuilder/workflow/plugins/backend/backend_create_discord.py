"""Workflow plugin: create Discord client."""
import os
import logging
import discord

logger = logging.getLogger("autometabuilder")


def run(runtime, inputs):
    """
    Initialize Discord Client (without starting the connection).
    
    Note: Discord client needs to be started asynchronously. This plugin
    just stores the token and intents configuration for later use by
    notification plugins.
    
    Inputs:
        token: Optional Discord bot token (defaults to DISCORD_BOT_TOKEN env var)
        
    Returns:
        dict: Contains initialization status and configuration
    """
    token = inputs.get("token") or os.environ.get("DISCORD_BOT_TOKEN")
    
    if not token:
        logger.warning("Discord client not initialized: DISCORD_BOT_TOKEN missing.")
        runtime.context["discord_token"] = None
        return {"result": None, "initialized": False, "error": "DISCORD_BOT_TOKEN missing"}
    
    # Store token and intents configuration in context
    # Discord client must be created per-use due to its async nature
    runtime.context["discord_token"] = token
    runtime.context["discord_intents"] = discord.Intents.default()
    
    logger.info("Discord configuration initialized successfully.")
    return {"result": token, "initialized": True}
