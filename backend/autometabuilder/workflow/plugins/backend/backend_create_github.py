"""Workflow plugin: create GitHub integration."""
import os
import logging
from github import Github
from github.Issue import Issue
from github.PullRequest import PullRequest
from tenacity import retry, stop_after_attempt, wait_exponential

from .... import load_messages

logger = logging.getLogger("autometabuilder")


class GitHubIntegration:
    """Class to handle GitHub interactions."""

    def __init__(self, token: str, repo_name: str):
        self.github = Github(token)
        self.repo = self.github.get_repo(repo_name)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_open_issues(self):
        """Get open issues from the repository."""
        return self.repo.get_issues(state='open')

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_issue(self, issue_number: int) -> Issue:
        """Get a specific issue by number."""
        return self.repo.get_issue(number=issue_number)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def create_branch(self, branch_name: str, base_branch: str = "main"):
        """Create a new branch from a base branch."""
        base_ref = self.repo.get_git_ref(f"heads/{base_branch}")
        self.repo.create_git_ref(
            ref=f"refs/heads/{branch_name}", sha=base_ref.object.sha
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def create_pull_request(
        self,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main",
    ) -> PullRequest:
        """Create a new pull request."""
        return self.repo.create_pull(
            title=title, body=body, head=head_branch, base=base_branch
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_pull_requests(self, state: str = "open"):
        """Get pull requests from the repository."""
        return self.repo.get_pulls(state=state)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_pull_request_comments(self, pr_number: int):
        """Get comments from a specific pull request."""
        pr = self.repo.get_pull(pr_number)
        return pr.get_issue_comments()


def get_repo_name_from_env() -> str:
    """Retrieve repository name from environment variable."""
    # Try to get from environment variable
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    if not repo_name:
        # Fallback or error
        msgs = load_messages()
        raise ValueError(msgs["error_github_repo_missing"])
    return repo_name


def run(runtime, _inputs):
    """Initialize GitHub client."""
    token = runtime.context.get("github_token")
    msgs = runtime.context.get("msgs", {})
    
    # Create GitHub integration if possible
    if not token:
        gh = None
    else:
        try:
            repo_name = get_repo_name_from_env()
            gh = GitHubIntegration(token, repo_name)
            logger.info(msgs["info_integrated_repo"].format(repo_name=repo_name))
        except Exception as error:  # pylint: disable=broad-exception-caught
            logger.warning(msgs["warn_github_init_failed"].format(error=error))
            gh = None
    
    # Store in both store (for workflow) and context (for other plugins)
    runtime.context["gh"] = gh
    return {"result": gh, "initialized": gh is not None}
