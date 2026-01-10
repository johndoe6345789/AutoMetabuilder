"""
Utilities module for AutoMetabuilder.

This module contains various utility functions:
- cli_args: CLI argument parsing
- context_loader: Load SDLC context from repo and GitHub
- docker_utils: Docker command utilities
- logging_config: Logging configuration with TRACE support
- model_resolver: Resolve LLM model names
- roadmap_utils: Roadmap file utilities
- tool_map_builder: Build tool map from registry
"""

from .cli_args import parse_args
from .context_loader import get_sdlc_context
from .docker_utils import run_command_in_docker
from .logging_config import configure_logging
from .model_resolver import resolve_model_name
from .roadmap_utils import is_mvp_reached, update_roadmap
from .tool_map_builder import build_tool_map

__all__ = [
    "parse_args",
    "get_sdlc_context",
    "run_command_in_docker",
    "configure_logging",
    "resolve_model_name",
    "is_mvp_reached",
    "update_roadmap",
    "build_tool_map",
]
