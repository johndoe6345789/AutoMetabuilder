"""
Main entry point for AutoMetabuilder.
"""
import os
import json
import requests
import yaml
from dotenv import load_dotenv
from openai import OpenAI
from . import load_messages
from .github_integration import GitHubIntegration, get_repo_name_from_env

load_dotenv()

DEFAULT_RAW_PROMPT_URL = (
    "https://raw.githubusercontent.com/johndoe6345789/"
    "metabuilder/main/getonwithit.prompt.yml"
)
DEFAULT_ENDPOINT = "https://models.github.ai/inference"


def load_prompt_yaml(url: str, token: str) -> dict:
    """Load prompt configuration from a remote YAML file."""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return yaml.safe_load(r.text)


def get_sdlc_context(gh: GitHubIntegration, msgs: dict) -> str:
    """Retrieve SDLC context (issues and PRs) from GitHub."""
    sdlc_context = ""
    if gh:
        try:
            issues = gh.get_open_issues()
            issue_list = "\n".join(
                [f"- #{i.number}: {i.title}" for i in issues[:5]]
            )
            if issue_list:
                sdlc_context += f"\n{msgs['open_issues_label']}\n{issue_list}"

            prs = gh.get_pull_requests()
            pr_list = "\n".join([f"- #{p.number}: {p.title}" for p in prs[:5]])
            if pr_list:
                sdlc_context += f"\n{msgs['open_prs_label']}\n{pr_list}"
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(msgs["error_sdlc_context"].format(error=e))
    return sdlc_context


def handle_tool_calls(resp_msg, gh: GitHubIntegration, msgs: dict):
    """Process tool calls from the AI response."""
    if resp_msg.tool_calls:
        for tool_call in resp_msg.tool_calls:
            function_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if function_name == "create_branch":
                if gh:
                    print(
                        msgs["info_executing_create_branch"].format(args=args)
                    )
                    gh.create_branch(**args)
                else:
                    print(msgs["error_github_not_available"])

            elif function_name == "create_pull_request":
                if gh:
                    print(msgs["info_executing_create_pr"].format(args=args))
                    gh.create_pull_request(**args)
                else:
                    print(msgs["error_github_not_available"])


def main():
    """Main function to run AutoMetabuilder."""
    msgs = load_messages()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print(msgs["error_github_token_missing"])
        return

    # Initialize GitHub Integration
    gh = None
    try:
        repo_name = get_repo_name_from_env()
        gh = GitHubIntegration(token, repo_name)
        print(msgs["info_integrated_repo"].format(repo_name=repo_name))
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(msgs["warn_github_init_failed"].format(error=e))

    client = OpenAI(
        base_url=os.environ.get("GITHUB_MODELS_ENDPOINT", DEFAULT_ENDPOINT),
        api_key=token,
    )

    prompt = load_prompt_yaml(
        os.environ.get("RAW_PROMPT_URL", DEFAULT_RAW_PROMPT_URL), token
    )

    # Load tools for SDLC operations from JSON file
    tools_path = os.path.join(os.path.dirname(__file__), "tools.json")
    with open(tools_path, "r", encoding="utf-8") as f:
        tools = json.load(f)

    # Add SDLC Context if available
    sdlc_context = get_sdlc_context(gh, msgs)

    messages = prompt["messages"]
    if sdlc_context:
        messages.append(
            {
                "role": "system",
                "content": f"{msgs['sdlc_context_label']}{sdlc_context}",
            }
        )

    # Add runtime request
    messages.append({"role": "user", "content": msgs["user_next_step"]})

    response = client.chat.completions.create(
        model=prompt.get("model", "openai/gpt-4.1"),
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=1.0,
        top_p=1.0,
    )

    resp_msg = response.choices[0].message
    print(
        resp_msg.content
        if resp_msg.content
        else msgs["info_tool_call_requested"]
    )

    # Handle tool calls
    handle_tool_calls(resp_msg, gh, msgs)


if __name__ == "__main__":
    main()
