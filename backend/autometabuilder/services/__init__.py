"""
Services module for AutoMetabuilder.

This module contains service integrations:
- github_integration: GitHub API integration
- github_service: GitHub service builder
- openai_client: OpenAI client helpers
- openai_factory: OpenAI client factory
"""

from .github_integration import GitHubIntegration, get_repo_name_from_env
from .github_service import create_github_integration
from .openai_client import get_completion
from .openai_factory import create_openai_client

__all__ = [
    "GitHubIntegration",
    "get_repo_name_from_env",
    "create_github_integration",
    "get_completion",
    "create_openai_client",
]
