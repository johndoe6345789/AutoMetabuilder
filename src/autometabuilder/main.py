import os
import requests
import yaml
import json
from dotenv import load_dotenv
from openai import OpenAI
from .github_integration import GitHubIntegration, get_repo_name_from_env

load_dotenv()

RAW_PROMPT_URL = "https://raw.githubusercontent.com/johndoe6345789/metabuilder/main/getonwithit.prompt.yml"

def load_prompt_yaml(url: str, token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return yaml.safe_load(r.text)

def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        return

    # Initialize GitHub Integration
    try:
        repo_name = get_repo_name_from_env()
        gh = GitHubIntegration(token, repo_name)
        print(f"Integrated with repository: {repo_name}")
    except Exception as e:
        print(f"Warning: GitHub integration failed: {e}")
        gh = None

    endpoint = "https://models.github.ai/inference"

    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )

    prompt = load_prompt_yaml(RAW_PROMPT_URL, token)

    messages = prompt["messages"]
    model = prompt.get("model", "openai/gpt-4.1")

    # Define tools for SDLC operations
    tools = [
        {
            "type": "function",
            "function": {
                "name": "create_branch",
                "description": "Create a new git branch in the repository",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "branch_name": {"type": "string", "description": "The name of the new branch"},
                        "base_branch": {"type": "string", "description": "The name of the base branch", "default": "main"},
                    },
                    "required": ["branch_name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_pull_request",
                "description": "Create a new pull request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "The title of the PR"},
                        "body": {"type": "string", "description": "The body content of the PR"},
                        "head_branch": {"type": "string", "description": "The branch where changes are implemented"},
                        "base_branch": {"type": "string", "description": "The branch to merge into", "default": "main"},
                    },
                    "required": ["title", "body", "head_branch"],
                },
            },
        }
    ]

    # Add SDLC Context if available
    sdlc_context = ""
    if gh:
        try:
            issues = gh.get_open_issues()
            issue_list = "\n".join([f"- #{i.number}: {i.title}" for i in issues[:5]])
            if issue_list:
                sdlc_context += f"\nOpen Issues:\n{issue_list}"
            
            prs = gh.get_pull_requests()
            pr_list = "\n".join([f"- #{p.number}: {p.title}" for p in prs[:5]])
            if pr_list:
                sdlc_context += f"\nOpen Pull Requests:\n{pr_list}"
        except Exception as e:
            print(f"Error fetching SDLC context: {e}")

    if sdlc_context:
        messages.append({"role": "system", "content": f"SDLC Context:{sdlc_context}"})

    # Add runtime request
    messages.append({"role": "user", "content": "What should I do next?"})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=1.0,
        top_p=1.0,
    )

    response_message = response.choices[0].message
    print(response_message.content if response_message.content else "Tool call requested...")

    # Handle tool calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            if function_name == "create_branch":
                if gh:
                    print(f"Executing: create_branch({args})")
                    gh.create_branch(**args)
                else:
                    print("Error: GitHub integration not available for tool call.")
            
            elif function_name == "create_pull_request":
                if gh:
                    print(f"Executing: create_pull_request({args})")
                    gh.create_pull_request(**args)
                else:
                    print("Error: GitHub integration not available for tool call.")

if __name__ == "__main__":
    main()
