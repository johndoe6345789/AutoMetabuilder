"""Load SDLC context from repo and GitHub."""
import os
import logging
from ..services.github_integration import GitHubIntegration

logger = logging.getLogger("autometabuilder")


def get_sdlc_context(gh: GitHubIntegration, msgs: dict) -> str:
    """Return SDLC context text from roadmap, issues, and PRs."""
    sdlc_context = ""
    if os.path.exists("ROADMAP.md"):
        with open("ROADMAP.md", "r", encoding="utf-8") as f:
            roadmap_content = f.read()
            label = msgs.get("roadmap_label", "ROADMAP.md Content:")
            sdlc_context += f"\n{label}\n{roadmap_content}\n"
    else:
        msg = msgs.get(
            "missing_roadmap_msg",
            "ROADMAP.md is missing. Please analyze the repository and create it."
        )
        sdlc_context += f"\n{msg}\n"

    if gh:
        try:
            issues = gh.get_open_issues()
            issue_list = "\n".join([f"- #{i.number}: {i.title}" for i in issues[:5]])
            if issue_list:
                sdlc_context += f"\n{msgs['open_issues_label']}\n{issue_list}"

            prs = gh.get_pull_requests()
            pr_list = "\n".join([f"- #{p.number}: {p.title}" for p in prs[:5]])
            if pr_list:
                sdlc_context += f"\n{msgs['open_prs_label']}\n{pr_list}"
        except Exception as error:  # pylint: disable=broad-exception-caught
            logger.error(msgs["error_sdlc_context"].format(error=error))

    return sdlc_context
