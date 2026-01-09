"""
Main entry point for AutoMetabuilder.
"""
import os
import json
import subprocess
import argparse
import yaml
import logging
import importlib
import inspect
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv
from openai import OpenAI
from . import load_messages
from .github_integration import GitHubIntegration, get_repo_name_from_env
from .docker_utils import run_command_in_docker
from .web.server import start_web_ui
from .integrations.notifications import notify_all
from .roadmap_utils import update_roadmap, is_mvp_reached

load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("autometabuilder.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("autometabuilder")

DEFAULT_PROMPT_PATH = "prompt.yml"
DEFAULT_ENDPOINT = "https://models.github.ai/inference"
DEFAULT_MODEL = "openai/gpt-4o"


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
            logger.error(msgs["error_sdlc_context"].format(error=e))
    return sdlc_context




def list_files(directory: str = "."):
    """List files in the repository for indexing."""
    files_list = []
    for root, _, files in os.walk(directory):
        if ".git" in root or "__pycache__" in root or ".venv" in root:
            continue
        for file in files:
            files_list.append(os.path.join(root, file))
    
    result = "\n".join(files_list)
    logger.info(f"Indexing repository files in {directory}...")
    return result


def run_tests(path: str = "tests"):
    """Run tests using pytest."""
    logger.info(f"Running tests in {path}...")
    result = subprocess.run(["pytest", path], capture_output=True, text=True, check=False)
    logger.info(result.stdout)
    if result.stderr:
        logger.error(result.stderr)
    return result.stdout


def run_lint(path: str = "src"):
    """Run linting using pylint."""
    logger.info(f"Running linting in {path}...")
    result = subprocess.run(["pylint", path], capture_output=True, text=True, check=False)
    logger.info(result.stdout)
    if result.stderr:
        logger.error(result.stderr)
    return result.stdout


def run_docker_task(image: str, command: str, workdir: str = "/workspace"):
    """
    Run a task inside a Docker container.
    Volumes are automatically mapped from current directory to /workspace.
    """
    volumes = {os.getcwd(): "/workspace"}
    return run_command_in_docker(image, command, volumes=volumes, workdir=workdir)


def read_file(path: str) -> str:
    """Read the content of a file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {path}: {e}"


def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing to file {path}: {e}"


def edit_file(path: str, search: str, replace: str) -> str:
    """Edit a file using search and replace."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if search not in content:
            return f"Error: '{search}' not found in {path}"
        
        new_content = content.replace(search, replace)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return f"Successfully edited {path}"
    except Exception as e:
        return f"Error editing file {path}: {e}"


def load_plugins(tool_map: dict, tools: list):
    """Load custom tools from the plugins directory."""
    plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
    if not os.path.exists(plugins_dir):
        return

    for filename in os.listdir(plugins_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f".plugins.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name, package="autometabuilder")
                for name, obj in inspect.getmembers(module):
                    if inspect.isfunction(obj) and hasattr(obj, "tool_metadata"):
                        tool_metadata = getattr(obj, "tool_metadata")
                        tool_map[name] = obj
                        tools.append(tool_metadata)
                        logger.info(f"Loaded plugin tool: {name}")
            except Exception as e:
                logger.error(f"Failed to load plugin {filename}: {e}")


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_completion(client, model, messages, tools):
    """Get completion from OpenAI with retry logic."""
    return client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=1.0,
        top_p=1.0,
    )


def handle_tool_calls(resp_msg, tool_map: dict, gh: GitHubIntegration, msgs: dict, dry_run: bool = False, yolo: bool = False) -> list:
    """Process tool calls from the AI response and return results for the assistant."""
    if not resp_msg.tool_calls:
        return []

    # Tools that modify state and should be skipped in dry-run
    modifying_tools = {"create_branch", "create_pull_request", "update_roadmap", "write_file", "edit_file"}
    tool_results = []

    for tool_call in resp_msg.tool_calls:
        function_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        call_id = tool_call.id

        handler = tool_map.get(function_name)
        if handler:
            if not yolo:
                confirm = input(msgs.get("confirm_tool_execution", "Do you want to execute {name} with {args}? [y/N]: ").format(name=function_name, args=args))
                if confirm.lower() != 'y':
                    logger.info(msgs.get("info_tool_skipped", "Skipping tool: {name}").format(name=function_name))
                    tool_results.append({
                        "tool_call_id": call_id,
                        "role": "tool",
                        "name": function_name,
                        "content": "Skipped by user.",
                    })
                    continue

            if dry_run and function_name in modifying_tools:
                logger.info(msgs.get("info_dry_run_skipping", "DRY RUN: Skipping state-modifying tool {name}").format(name=function_name))
                tool_results.append({
                    "tool_call_id": call_id,
                    "role": "tool",
                    "name": function_name,
                    "content": "Skipped due to dry-run.",
                })
                continue

            logger.info(msgs.get("info_executing_tool", "Executing tool: {name}").format(name=function_name))
            try:
                result = handler(**args)
                content = str(result) if result is not None else "Success"
                if hasattr(result, "__iter__") and not isinstance(result, str):
                    # Handle iterables (like PyGithub PaginatedList)
                    items = list(result)[:5]
                    content = "\n".join([f"- {item}" for item in items])
                    logger.info(content)
                elif result is not None:
                    logger.info(result)
                
                tool_results.append({
                    "tool_call_id": call_id,
                    "role": "tool",
                    "name": function_name,
                    "content": content,
                })
            except Exception as e:
                error_msg = f"Error executing {function_name}: {e}"
                logger.error(error_msg)
                tool_results.append({
                    "tool_call_id": call_id,
                    "role": "tool",
                    "name": function_name,
                    "content": error_msg,
                })
        else:
            msg = msgs.get("error_tool_not_found", "Tool {name} not found or unavailable.").format(name=function_name)
            logger.error(msg)
            tool_results.append({
                "tool_call_id": call_id,
                "role": "tool",
                "name": function_name,
                "content": msg,
            })
    return tool_results


def main():
    """Main function to run AutoMetabuilder."""
    parser = argparse.ArgumentParser(description="AutoMetabuilder: AI-driven SDLC assistant.")
    parser.add_argument("--dry-run", action="store_true", help="Do not execute state-modifying tools.")
    parser.add_argument("--yolo", action="store_true", help="Execute tools without confirmation.")
    parser.add_argument("--once", action="store_true", help="Run a single full iteration (AI -> Tool -> AI).")
    parser.add_argument("--web", action="store_true", help="Start the Web UI.")
    args = parser.parse_args()

    if args.web:
        logger.info("Starting Web UI...")
        start_web_ui()
        return

    msgs = load_messages()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        logger.error(msgs["error_github_token_missing"])
        return

    # Initialize GitHub Integration
    gh = None
    try:
        repo_name = get_repo_name_from_env()
        gh = GitHubIntegration(token, repo_name)
        logger.info(msgs["info_integrated_repo"].format(repo_name=repo_name))
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.warning(msgs["warn_github_init_failed"].format(error=e))

    client = OpenAI(
        base_url=os.environ.get("GITHUB_MODELS_ENDPOINT", DEFAULT_ENDPOINT),
        api_key=token,
    )

    prompt = load_prompt_yaml()

    # Load tools for SDLC operations from JSON file
    tools_path = os.path.join(os.path.dirname(__file__), "tools.json")
    with open(tools_path, "r", encoding="utf-8") as f:
        tools = json.load(f)

    # Declarative mapping of tool names to functions
    tool_map = {
        "create_branch": gh.create_branch if gh else None,
        "create_pull_request": gh.create_pull_request if gh else None,
        "get_pull_request_comments": gh.get_pull_request_comments if gh else None,
        "update_roadmap": update_roadmap,
        "list_files": list_files,
        "run_tests": run_tests,
        "run_lint": run_lint,
        "run_docker_task": run_docker_task,
        "read_file": read_file,
        "write_file": write_file,
        "edit_file": edit_file,
    }

    # Load plugins and update tool_map and tools list
    load_plugins(tool_map, tools)

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

    model_name = os.environ.get("LLM_MODEL", prompt.get("model", DEFAULT_MODEL))

    # Multi-iteration loop
    iteration = 0
    max_iterations = 10
    
    while iteration < max_iterations:
        iteration += 1
        logger.info(f"--- Iteration {iteration} ---")
        
        response = get_completion(client, model_name, messages, tools)
        resp_msg = response.choices[0].message
        
        logger.info(
            resp_msg.content
            if resp_msg.content
            else msgs["info_tool_call_requested"]
        )
        
        messages.append(resp_msg)
        
        if not resp_msg.tool_calls:
            # If no more tools requested, we are done
            notify_all(f"AutoMetabuilder task complete: {resp_msg.content[:100]}...")
            break
            
        # Handle tool calls
        tool_results = handle_tool_calls(resp_msg, tool_map, gh, msgs, dry_run=args.dry_run, yolo=args.yolo)
        messages.extend(tool_results)

        if args.yolo and is_mvp_reached():
            logger.info("MVP reached. Stopping YOLO loop.")
            notify_all("AutoMetabuilder YOLO loop stopped: MVP reached.")
            break
        
        if args.once:
            # If --once is set, we do one more pass to show the final result
            logger.info(msgs.get("info_second_pass", "Performing second pass with tool results..."))
            response = get_completion(client, model_name, messages, tools)
            final_msg = response.choices[0].message
            logger.info(final_msg.content if final_msg.content else msgs["info_tool_call_requested"])
            notify_all(f"AutoMetabuilder task complete: {final_msg.content[:100]}...")
            
            # For --once, we still handle tool calls if any in the second pass, but then stop.
            if final_msg.tool_calls:
                handle_tool_calls(final_msg, tool_map, gh, msgs, dry_run=args.dry_run, yolo=args.yolo)
            break
    else:
        logger.warning(f"Reached maximum iterations ({max_iterations}). Stopping.")
        notify_all(f"AutoMetabuilder stopped: Reached {max_iterations} iterations.")


if __name__ == "__main__":
    main()
