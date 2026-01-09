"""
GitHub integration module.
"""
import os
from github import Github
from github.Issue import Issue
from github.PullRequest import PullRequest

from . import load_messages


class GitHubIntegration:
    """Class to handle GitHub interactions."""

    def __init__(self, token: str, repo_name: str):
        self.github = Github(token)
        self.repo = self.github.get_repo(repo_name)

    def get_open_issues(self):
        """Get open issues from the repository."""
        return self.repo.get_issues(state='open')

    def get_issue(self, issue_number: int) -> Issue:
        """Get a specific issue by number."""
        return self.repo.get_issue(number=issue_number)

    def create_branch(self, branch_name: str, base_branch: str = "main"):
        """Create a new branch from a base branch."""
        base_ref = self.repo.get_git_ref(f"heads/{base_branch}")
        self.repo.create_git_ref(
            ref=f"refs/heads/{branch_name}", sha=base_ref.object.sha
        )

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

    def get_pull_requests(self, state: str = "open"):
        """Get pull requests from the repository."""
        return self.repo.get_pulls(state=state)


def get_repo_name_from_env() -> str:
    """Retrieve repository name from environment variable."""
    # Try to get from environment variable
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    if not repo_name:
        # Fallback or error
        msgs = load_messages()
        raise ValueError(msgs["error_github_repo_missing"])
    return repo_name
