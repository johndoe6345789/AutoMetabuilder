"""Workflow plugin: build prompt YAML."""
from ....web.data.prompt import build_prompt_yaml


def run(_runtime, inputs):
    """Build prompt YAML from system and user content."""
    system_content = inputs.get("system_content")
    user_content = inputs.get("user_content")
    model = inputs.get("model")
    
    yaml_content = build_prompt_yaml(system_content, user_content, model)
    return {"result": yaml_content}
