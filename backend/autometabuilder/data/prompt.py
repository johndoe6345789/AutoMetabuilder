from __future__ import annotations

import os
from pathlib import Path


def build_prompt_yaml(system_content: str | None, user_content: str | None, model: str | None) -> str:
    def indent_block(text: str | None) -> str:
        if not text:
            return ""
        return "\n      ".join(line.rstrip() for line in text.splitlines())

    model_value = model or "openai/gpt-4o"
    system_block = indent_block(system_content)
    user_block = indent_block(user_content)
    return f"""messages:
  - role: system
    content: >-
      {system_block}
  - role: user
    content: >-
      {user_block}
model: {model_value}
"""


def get_prompt_content() -> str:
    path = Path(os.environ.get("PROMPT_PATH", "prompt.yml"))
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return ""


def write_prompt(content: str) -> None:
    path = Path(os.environ.get("PROMPT_PATH", "prompt.yml"))
    path.write_text(content or "", encoding="utf-8")
