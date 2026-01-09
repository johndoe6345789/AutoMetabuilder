"""GitHub integration builder."""
import logging
from .github_integration import GitHubIntegration, get_repo_name_from_env

logger = logging.getLogger("autometabuilder")


def create_github_integration(token: str, msgs: dict):
    """Create GitHub integration if possible."""
    if not token:
        return None
    try:
        repo_name = get_repo_name_from_env()
        gh = GitHubIntegration(token, repo_name)
        logger.info(msgs["info_integrated_repo"].format(repo_name=repo_name))
        return gh
    except Exception as error:  # pylint: disable=broad-exception-caught
        logger.warning(msgs["warn_github_init_failed"].format(error=error))
        return None
