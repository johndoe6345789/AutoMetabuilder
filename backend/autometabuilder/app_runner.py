"""Application runner."""
import logging
import os
from . import load_messages
from .cli_args import parse_args
from .env_loader import load_env
from .github_service import create_github_integration
from .logging_config import configure_logging
from .metadata_loader import load_metadata
from .openai_factory import create_openai_client
from .plugin_loader import load_plugins
from .prompt_loader import load_prompt_yaml
from .tool_map_builder import build_tool_map
from .tool_policy_loader import load_tool_policies
from .tool_registry_loader import load_tool_registry
from .tools_loader import load_tools
from .web.server import start_web_ui
from .workflow_config_loader import load_workflow_config
from .workflow_context_builder import build_workflow_context
from .workflow_engine_builder import build_workflow_engine


def run_app() -> None:
    """Run the AutoMetabuilder CLI."""
    load_env()
    configure_logging()
    logger = logging.getLogger("autometabuilder")

    args = parse_args()
    if args.web:
        logger.info("Starting Web UI...")
        start_web_ui()
        return

    msgs = load_messages()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        logger.error(msgs["error_github_token_missing"])
        return

    gh = create_github_integration(token, msgs)
    client = create_openai_client(token)
    prompt = load_prompt_yaml()
    metadata = load_metadata()
    tools = load_tools(metadata)

    tool_map = build_tool_map(gh, load_tool_registry())
    load_plugins(tool_map, tools)

    context_parts = {
        "args": args,
        "gh": gh,
        "msgs": msgs,
        "client": client,
        "tools": tools,
        "tool_map": tool_map,
        "prompt": prompt,
        "tool_policies": load_tool_policies()
    }
    workflow_context = build_workflow_context(context_parts)
    logger.debug("Workflow context ready with %s tools", len(tool_map))

    engine = build_workflow_engine(load_workflow_config(metadata), workflow_context, logger)
    engine.execute()
