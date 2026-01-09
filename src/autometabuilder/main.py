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
import re
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


class WorkflowEngine:
    """Interpret and execute a JSON-defined workflow."""

    def __init__(self, workflow_config, context):
        self.workflow_config = workflow_config
        self.context = context
        self.state = {}

    def execute(self):
        """Execute the workflow sequence."""
        for phase in self.workflow_config:
            if phase.get("type") == "loop":
                self._execute_loop(phase)
            else:
                self._execute_phase(phase)

    def _call_tool(self, tool_name, **kwargs):
        tool = self.context["tool_map"].get(tool_name)
        if not tool:
            msg = self.context["msgs"].get(
                "error_tool_not_found",
                "Tool {name} not found or unavailable."
            ).format(name=tool_name)
            logger.error(msg)
            return msg

        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return tool(**filtered_kwargs)
        except Exception as e:
            error_msg = f"Error executing {tool_name}: {e}"
            logger.error(error_msg)
            return error_msg

    def _ensure_list(self, value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, (tuple, set)):
            return list(value)
        if isinstance(value, str):
            return [line for line in value.splitlines() if line.strip()]
        return [value]

    def _normalize_separator(self, text):
        if text is None:
            return ""
        return text.replace("\\n", "\n").replace("\\t", "\t")

    def _execute_phase(self, phase):
        """Execute a phase which contains steps."""
        logger.info(f"--- Executing phase: {phase.get('name', 'unnamed')} ---")
        for step in phase.get("steps", []):
            self._execute_step(step)

    def _execute_loop(self, phase):
        """Execute a loop of steps."""
        max_iterations = phase.get("max_iterations", 10)
        if self.context["args"].once:
            max_iterations = 2 # At most 2 passes for --once

        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            logger.info(f"--- {phase.get('name', 'loop')} Iteration {iteration} ---")
            should_stop = False
            for step in phase.get("steps", []):
                result = self._execute_step(step)
                if step.get("stop_if_no_tools") and result is True:
                    should_stop = True
                    break
            
            if should_stop or (self.context["args"].once and iteration >= 1 and not self.state.get("llm_response").tool_calls):
                 break
            
            if self.context["args"].once and iteration == 2:
                break

    def _execute_step(self, step):
        """Execute a single workflow step."""
        step_type = step.get("type")
        output_key = step.get("output_key")

        try:
            if step_type == "load_context":
                sdlc_context = get_sdlc_context(self.context["gh"], self.context["msgs"])
                if output_key:
                    self.state[output_key] = sdlc_context
                return sdlc_context

            elif step_type == "seed_messages":
                prompt = self.context["prompt"]
                messages = list(prompt["messages"])
                if output_key:
                    self.state[output_key] = messages
                return messages

            elif step_type == "prepare_messages":
                prompt = self.context["prompt"]
                msgs = self.context["msgs"]
                sdlc_context_val = self.state.get(step.get("input_context"))
                messages = list(prompt["messages"])
                if sdlc_context_val:
                    messages.append(
                        {
                            "role": "system",
                            "content": f"{msgs['sdlc_context_label']}{sdlc_context_val}",
                        }
                    )
                messages.append({"role": "user", "content": msgs["user_next_step"]})
                if output_key:
                    self.state[output_key] = messages
                return messages

            elif step_type in ("append_context_message",):
                msgs = self.context["msgs"]
                sdlc_context_val = self.state.get(step.get("input_context"))
                target_messages = self.state.get(step.get("target_messages"))
                if sdlc_context_val and target_messages is not None:
                    target_messages.append(
                        {
                            "role": "system",
                            "content": f"{msgs['sdlc_context_label']}{sdlc_context_val}",
                        }
                    )
                return target_messages

            elif step_type in ("append_user_instruction",):
                msgs = self.context["msgs"]
                target_messages = self.state.get(step.get("target_messages"))
                if target_messages is not None:
                    target_messages.append({"role": "user", "content": msgs["user_next_step"]})
                return target_messages

            elif step_type in ("llm_gen", "ai_request"):
                messages = self.state.get(step.get("input_messages"))
                response = get_completion(
                    self.context["client"],
                    self.context["model_name"],
                    messages,
                    self.context["tools"]
                )
                resp_msg = response.choices[0].message
                logger.info(
                    resp_msg.content
                    if resp_msg.content
                    else self.context["msgs"]["info_tool_call_requested"]
                )
                messages.append(resp_msg)
                if output_key:
                    self.state[output_key] = resp_msg
                return resp_msg

            elif step_type in ("process_response", "run_tool_calls"):
                resp_msg = self.state.get(step.get("input_response"))
                tool_results = handle_tool_calls(
                    resp_msg,
                    self.context["tool_map"],
                    self.context["gh"],
                    self.context["msgs"],
                    dry_run=self.context["args"].dry_run,
                    yolo=self.context["args"].yolo
                )
                if output_key:
                    self.state[output_key] = tool_results

                if step.get("stop_if_no_tools") and not resp_msg.tool_calls:
                    notify_all(f"AutoMetabuilder task complete: {resp_msg.content[:100]}...")
                    return True
                return False

            elif step_type in ("update_messages", "append_tool_results"):
                tool_results = self.state.get(step.get("input_results"))
                target_messages = self.state.get(step.get("target_messages"))
                if tool_results and target_messages is not None:
                    target_messages.extend(tool_results)

                if self.context["args"].yolo and is_mvp_reached():
                    logger.info("MVP reached. Stopping YOLO loop.")
                    notify_all("AutoMetabuilder YOLO loop stopped: MVP reached.")
                    return True

            elif step_type == "list_files":
                result = self._call_tool("list_files", directory=step.get("path", "."))
                if output_key:
                    self.state[output_key] = result
                return result

            elif step_type == "read_file":
                result = self._call_tool("read_file", path=step.get("path"))
                if output_key:
                    self.state[output_key] = result
                return result

            elif step_type == "run_tests":
                result = self._call_tool("run_tests", path=step.get("path", "tests"))
                if output_key:
                    self.state[output_key] = result
                return result

            elif step_type == "run_lint":
                result = self._call_tool("run_lint", path=step.get("path", "src"))
                if output_key:
                    self.state[output_key] = result
                return result

            elif step_type == "create_branch":
                return self._call_tool(
                    "create_branch",
                    branch_name=step.get("branch_name"),
                    base_branch=step.get("base_branch", "main")
                )

            elif step_type == "create_pull_request":
                return self._call_tool(
                    "create_pull_request",
                    title=step.get("title"),
                    body=step.get("body"),
                    head_branch=step.get("head_branch"),
                    base_branch=step.get("base_branch", "main")
                )

            elif step_type == "update_roadmap":
                content = step.get("content") or self.state.get(step.get("input_key"))
                result = self._call_tool("update_roadmap", content=content)
                if output_key:
                    self.state[output_key] = result
                return result

            elif step_type == "filter_list":
                items = self._ensure_list(self.state.get(step.get("input_key")))
                mode = step.get("mode", "contains")
                pattern = step.get("pattern", "")
                filtered = []
                for item in items:
                    candidate = str(item)
                    matched = False
                    if mode == "contains":
                        matched = pattern in candidate
                    elif mode == "regex":
                        matched = bool(re.search(pattern, candidate))
                    elif mode == "equals":
                        matched = candidate == pattern
                    elif mode == "not_equals":
                        matched = candidate != pattern
                    elif mode == "starts_with":
                        matched = candidate.startswith(pattern)
                    elif mode == "ends_with":
                        matched = candidate.endswith(pattern)
                    if matched:
                        filtered.append(item)
                if output_key:
                    self.state[output_key] = filtered
                return filtered

            elif step_type == "map_list":
                items = self._ensure_list(self.state.get(step.get("input_key")))
                template = step.get("template", "{item}")
                mapped = []
                for item in items:
                    try:
                        mapped.append(template.format(item=item))
                    except Exception:
                        mapped.append(str(item))
                if output_key:
                    self.state[output_key] = mapped
                return mapped

            elif step_type == "reduce_list":
                items = self._ensure_list(self.state.get(step.get("input_key")))
                separator = self._normalize_separator(step.get("separator", ""))
                reduced = separator.join([str(item) for item in items])
                if output_key:
                    self.state[output_key] = reduced
                return reduced

            elif step_type == "branch":
                value = self.state.get(step.get("input_key"))
                mode = step.get("mode", "is_truthy")
                compare = step.get("compare", "")
                decision = False

                if mode == "is_empty":
                    decision = not self._ensure_list(value)
                elif mode == "is_truthy":
                    decision = bool(value)
                elif mode == "equals":
                    decision = str(value) == compare
                elif mode == "not_equals":
                    decision = str(value) != compare
                elif mode == "contains":
                    decision = compare in str(value)
                elif mode == "regex":
                    decision = bool(re.search(compare, str(value)))

                if output_key:
                    self.state[output_key] = decision

                branch_steps = step.get("then_steps") if decision else step.get("else_steps")
                if isinstance(branch_steps, list):
                    for branch_step in branch_steps:
                        self._execute_step(branch_step)
                return decision

            else:
                logger.error(f"Unknown step type: {step_type}")

        except Exception as e:
            logger.error(f"Error executing step {step_type}: {e}")
            raise

        return None


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

    # Load Metadata
    metadata_path = os.path.join(os.path.dirname(__file__), "metadata.json")
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Load tools for SDLC operations from JSON file
    tools_path = os.path.join(os.path.dirname(__file__), metadata.get("tools_path", "tools.json"))
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

    model_name = os.environ.get("LLM_MODEL", prompt.get("model", DEFAULT_MODEL))

    # Load Workflow
    workflow_path = os.path.join(os.path.dirname(__file__), metadata.get("workflow_path", "workflow.json"))
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow_config = json.load(f)

    # Initialize Context for Workflow Engine
    workflow_context = {
        "gh": gh,
        "msgs": msgs,
        "client": client,
        "prompt": prompt,
        "tools": tools,
        "tool_map": tool_map,
        "model_name": model_name,
        "args": args
    }

    engine = WorkflowEngine(workflow_config, workflow_context)
    engine.execute()


if __name__ == "__main__":
    main()
