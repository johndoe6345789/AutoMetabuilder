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
    """Interpret and execute a node-based workflow."""

    def __init__(self, workflow_config, context):
        self.workflow_config = workflow_config or {}
        self.context = context
        self.store = {}
        self.plugins = self._build_plugins()

    def execute(self):
        nodes = self.workflow_config.get("nodes")
        if not isinstance(nodes, list):
            logger.error("Workflow config missing nodes list.")
            return
        self._execute_nodes(nodes)

    def _execute_nodes(self, nodes):
        for node in nodes:
            self._execute_node(node)

    def _execute_node(self, node):
        node_type = node.get("type")
        if not node_type:
            logger.error("Workflow node missing type.")
            return None

        when_value = node.get("when")
        if when_value is not None:
            if not self._coerce_bool(self._resolve_binding(when_value)):
                return None

        if node_type == "control.loop":
            return self._execute_loop(node)

        plugin = self.plugins.get(node_type)
        if not plugin:
            logger.error(f"Unknown node type: {node_type}")
            return None

        inputs = self._resolve_inputs(node.get("inputs", {}))
        result = plugin(inputs)
        if not isinstance(result, dict):
            result = {"result": result}

        outputs = node.get("outputs", {})
        if outputs:
            for output_name, store_key in outputs.items():
                if output_name in result:
                    self.store[store_key] = result[output_name]
        else:
            for output_name, value in result.items():
                self.store[output_name] = value

        return result

    def _execute_loop(self, node):
        inputs = node.get("inputs", {})
        max_iterations = self._resolve_binding(inputs.get("max_iterations", 1))
        stop_when_raw = inputs.get("stop_when")
        stop_on_raw = inputs.get("stop_on", True)

        try:
            max_iterations = int(max_iterations)
        except (TypeError, ValueError):
            max_iterations = 1

        if self.context["args"].once:
            max_iterations = min(max_iterations, 1)

        stop_on = self._coerce_bool(self._resolve_binding(stop_on_raw))

        body = node.get("body", [])
        if not isinstance(body, list):
            logger.error("Loop body must be a list of nodes.")
            return None

        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            logger.info(f"--- Loop iteration {iteration} ---")
            self._execute_nodes(body)

            if stop_when_raw is not None:
                stop_value = self._resolve_binding(stop_when_raw)
                if self._coerce_bool(stop_value) == stop_on:
                    break

        return None

    def _build_plugins(self):
        return {
            "core.load_context": self._plugin_load_context,
            "core.seed_messages": self._plugin_seed_messages,
            "core.append_context_message": self._plugin_append_context_message,
            "core.append_user_instruction": self._plugin_append_user_instruction,
            "core.ai_request": self._plugin_ai_request,
            "core.run_tool_calls": self._plugin_run_tool_calls,
            "core.append_tool_results": self._plugin_append_tool_results,
            "tools.list_files": self._plugin_list_files,
            "tools.read_file": self._plugin_read_file,
            "tools.run_tests": self._plugin_run_tests,
            "tools.run_lint": self._plugin_run_lint,
            "tools.create_branch": self._plugin_create_branch,
            "tools.create_pull_request": self._plugin_create_pull_request,
            "utils.filter_list": self._plugin_filter_list,
            "utils.map_list": self._plugin_map_list,
            "utils.reduce_list": self._plugin_reduce_list,
            "utils.branch_condition": self._plugin_branch_condition,
            "utils.not": self._plugin_not,
        }

    def _plugin_load_context(self, inputs):
        return {"context": get_sdlc_context(self.context["gh"], self.context["msgs"])}

    def _plugin_seed_messages(self, inputs):
        prompt = self.context["prompt"]
        return {"messages": list(prompt["messages"])}

    def _plugin_append_context_message(self, inputs):
        messages = list(inputs.get("messages") or [])
        context_val = inputs.get("context")
        if context_val:
            messages.append(
                {
                    "role": "system",
                    "content": f"{self.context['msgs']['sdlc_context_label']}{context_val}",
                }
            )
        return {"messages": messages}

    def _plugin_append_user_instruction(self, inputs):
        messages = list(inputs.get("messages") or [])
        messages.append({"role": "user", "content": self.context["msgs"]["user_next_step"]})
        return {"messages": messages}

    def _plugin_ai_request(self, inputs):
        messages = list(inputs.get("messages") or [])
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
        tool_calls = getattr(resp_msg, "tool_calls", None) or []
        return {
            "response": resp_msg,
            "has_tool_calls": bool(tool_calls),
            "tool_calls_count": len(tool_calls)
        }

    def _plugin_run_tool_calls(self, inputs):
        resp_msg = inputs.get("response")
        tool_calls = getattr(resp_msg, "tool_calls", None) or []
        if not resp_msg:
            return {"tool_results": [], "no_tool_calls": True}

        tool_results = handle_tool_calls(
            resp_msg,
            self.context["tool_map"],
            self.context["gh"],
            self.context["msgs"],
            dry_run=self.context["args"].dry_run,
            yolo=self.context["args"].yolo
        )
        if not tool_calls and resp_msg.content:
            notify_all(f"AutoMetabuilder task complete: {resp_msg.content[:100]}...")
        return {
            "tool_results": tool_results,
            "no_tool_calls": not bool(tool_calls)
        }

    def _plugin_append_tool_results(self, inputs):
        messages = list(inputs.get("messages") or [])
        tool_results = inputs.get("tool_results") or []
        if tool_results:
            messages.extend(tool_results)

        if self.context["args"].yolo and is_mvp_reached():
            logger.info("MVP reached. Stopping YOLO loop.")
            notify_all("AutoMetabuilder YOLO loop stopped: MVP reached.")

        return {"messages": messages}

    def _plugin_list_files(self, inputs):
        result = self._call_tool("list_files", directory=inputs.get("path", "."))
        return {"files": result}

    def _plugin_read_file(self, inputs):
        result = self._call_tool("read_file", path=inputs.get("path"))
        return {"content": result}

    def _plugin_run_tests(self, inputs):
        result = self._call_tool("run_tests", path=inputs.get("path", "tests"))
        return {"results": result}

    def _plugin_run_lint(self, inputs):
        result = self._call_tool("run_lint", path=inputs.get("path", "src"))
        return {"results": result}

    def _plugin_create_branch(self, inputs):
        result = self._call_tool(
            "create_branch",
            branch_name=inputs.get("branch_name"),
            base_branch=inputs.get("base_branch", "main")
        )
        return {"result": result}

    def _plugin_create_pull_request(self, inputs):
        result = self._call_tool(
            "create_pull_request",
            title=inputs.get("title"),
            body=inputs.get("body"),
            head_branch=inputs.get("head_branch"),
            base_branch=inputs.get("base_branch", "main")
        )
        return {"result": result}

    def _plugin_filter_list(self, inputs):
        items = self._ensure_list(inputs.get("items"))
        mode = inputs.get("mode", "contains")
        pattern = inputs.get("pattern", "")
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
        return {"items": filtered}

    def _plugin_map_list(self, inputs):
        items = self._ensure_list(inputs.get("items"))
        template = inputs.get("template", "{item}")
        mapped = []
        for item in items:
            try:
                mapped.append(template.format(item=item))
            except Exception:
                mapped.append(str(item))
        return {"items": mapped}

    def _plugin_reduce_list(self, inputs):
        items = self._ensure_list(inputs.get("items"))
        separator = self._normalize_separator(inputs.get("separator", ""))
        reduced = separator.join([str(item) for item in items])
        return {"result": reduced}

    def _plugin_branch_condition(self, inputs):
        value = inputs.get("value")
        mode = inputs.get("mode", "is_truthy")
        compare = inputs.get("compare", "")
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

        return {"result": decision}

    def _plugin_not(self, inputs):
        return {"result": not self._coerce_bool(inputs.get("value"))}

    def _resolve_inputs(self, inputs):
        return {key: self._resolve_binding(value) for key, value in (inputs or {}).items()}

    def _resolve_binding(self, value):
        if isinstance(value, str) and value.startswith("$"):
            return self.store.get(value[1:])
        return value

    def _coerce_bool(self, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in ("true", "yes", "1"):
                return True
            if lowered in ("false", "no", "0", ""):
                return False
        return bool(value)

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
        if isinstance(text, str):
            return text.replace("\\n", "\n").replace("\\t", "\t")
        return str(text)

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
            result = tool(**filtered_kwargs)
            return result if result is not None else "Success"
        except Exception as e:
            error_msg = f"Error executing {tool_name}: {e}"
            logger.error(error_msg)
            return error_msg


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
