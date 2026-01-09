import os
from github import Github
from github.Repository import Repository
from github.Issue import Issue
from github.PullRequest import PullRequest

class GitHubIntegration:
    def __init__(self, token: str, repo_name: str):
        self.github = Github(token)
        self.repo = self.github.get_repo(repo_name)

    def get_open_issues(self):
        return self.repo.get_issues(state='open')

    def get_issue(self, issue_number: int) -> Issue:
        return self.repo.get_issue(number=issue_number)

    def create_branch(self, branch_name: str, base_branch: str = "main"):
        base_ref = self.repo.get_git_ref(f"heads/{base_branch}")
        self.repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base_ref.object.sha)

    def create_pull_request(self, title: str, body: str, head_branch: str, base_branch: str = "main") -> PullRequest:
        return self.repo.create_pull(title=title, body=body, head=head_branch, base=base_branch)

    def get_pull_requests(self, state: str = 'open'):
        return self.repo.get_pulls(state=state)

def get_repo_name_from_env() -> str:
    # Try to get from environment variable, or fallback to some detection if possible
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    if not repo_name:
        # Fallback or error
        raise ValueError("GITHUB_REPOSITORY environment variable not set")
    return repo_name
