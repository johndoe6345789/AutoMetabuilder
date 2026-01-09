"""
Main entry point for AutoMetabuilder.
"""
import os
import json
import subprocess
import yaml
from dotenv import load_dotenv
from openai import OpenAI
from . import load_messages
from .github_integration import GitHubIntegration, get_repo_name_from_env

load_dotenv()

DEFAULT_PROMPT_PATH = "prompt.yml"
DEFAULT_ENDPOINT = "https://models.github.ai/inference"


def load_prompt_yaml() -> dict:
    """Load prompt configuration from local file."""
    local_path = os.environ.get("PROMPT_PATH", DEFAULT_PROMPT_PATH)
    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    raise FileNotFoundError(f"Prompt file not found at {local_path}")


def get_sdlc_context(gh: GitHubIntegration, msgs: dict) -> str:
    """Retrieve SDLC context (issues, PRs, and Roadmap) from GitHub/Local."""
    sdlc_context = ""
    
    # Load ROADMAP.md if it exists, otherwise add instruction to create it
    if os.path.exists("ROADMAP.md"):
        with open("ROADMAP.md", "r", encoding="utf-8") as f:
            roadmap_content = f.read()
            sdlc_context += f"\n{msgs.get('roadmap_label', 'ROADMAP.md Content:')}\n{roadmap_content}\n"
    else:
        msg = msgs.get('missing_roadmap_msg', 'ROADMAP.md is missing. Please analyze the repository and create it.')
        sdlc_context += f"\n{msg}\n"

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


def update_roadmap(content: str):
    """Update ROADMAP.md with new content."""
    with open("ROADMAP.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("ROADMAP.md updated successfully.")


def list_files(directory: str = "."):
    """List files in the repository for indexing."""
    files_list = []
    for root, _, files in os.walk(directory):
        if ".git" in root or "__pycache__" in root or ".venv" in root:
            continue
        for file in files:
            files_list.append(os.path.join(root, file))
    
    result = "\n".join(files_list)
    print(f"Indexing repository files in {directory}...")
    return result


def run_tests(path: str = "tests"):
    """Run tests using pytest."""
    print(f"Running tests in {path}...")
    result = subprocess.run(["pytest", path], capture_output=True, text=True, check=False)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.stdout


def run_lint(path: str = "src"):
    """Run linting using pylint."""
    print(f"Running linting in {path}...")
    result = subprocess.run(["pylint", path], capture_output=True, text=True, check=False)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.stdout


def handle_tool_calls(resp_msg, gh: GitHubIntegration, msgs: dict):
    """Process tool calls from the AI response using a declarative mapping."""
    if not resp_msg.tool_calls:
        return

    # Declarative mapping of tool names to functions
    tool_map = {
        "create_branch": gh.create_branch if gh else None,
        "create_pull_request": gh.create_pull_request if gh else None,
        "get_pull_request_comments": gh.get_pull_request_comments if gh else None,
        "update_roadmap": update_roadmap,
        "list_files": list_files,
        "run_tests": run_tests,
        "run_lint": run_lint,
    }

    for tool_call in resp_msg.tool_calls:
        function_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        handler = tool_map.get(function_name)
        if handler:
            print(msgs.get("info_executing_tool", "Executing tool: {name}").format(name=function_name))
            try:
                result = handler(**args)
                if result:
                    # In a real scenario, we might want to feed this back to the AI
                    if hasattr(result, "__iter__") and not isinstance(result, str):
                        # Handle iterables (like PyGithub PaginatedList)
                        for item in list(result)[:5]:
                            print(f"- {item}")
                    else:
                        print(result)
            except Exception as e:
                print(f"Error executing {function_name}: {e}")
        else:
            print(msgs.get("error_tool_not_found", "Tool {name} not found or unavailable.").format(name=function_name))


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

    prompt = load_prompt_yaml()

    # Load tools for SDLC operations from JSON file
    tools_path = os.path.join(os.path.dirname(__file__), "tools.json")
    with open(tools_path, "r", encoding="utf-8") as f:
        tools = json.load(f)

    # Add SDLC Context if available
    sdlc_context_val = get_sdlc_context(gh, msgs)

    messages = prompt["messages"]
    if sdlc_context_val:
        messages.append(
            {
                "role": "system",
                "content": f"{msgs['sdlc_context_label']}{sdlc_context_val}",
            }
        )

    # Add runtime request
    messages.append({"role": "user", "content": msgs["user_next_step"]})

    response = client.chat.completions.create(
        model=os.environ.get("LLM_MODEL", prompt.get("model", "openai/gpt-4.1")),
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
