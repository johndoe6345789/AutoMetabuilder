"""Build workflow runtime context."""
from .model_resolver import resolve_model_name


def build_workflow_context(args, gh, msgs, client, tools, tool_map, prompt, tool_policies) -> dict:
    return {
        "args": args,
        "gh": gh,
        "msgs": msgs,
        "client": client,
        "model_name": resolve_model_name(prompt),
        "tools": tools,
        "tool_map": tool_map,
        "prompt": prompt,
        "tool_policies": tool_policies,
    }
