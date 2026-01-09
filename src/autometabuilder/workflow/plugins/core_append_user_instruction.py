"""Workflow plugin: append user instruction."""


def run(runtime, inputs):
    messages = list(inputs.get("messages") or [])
    messages.append({"role": "user", "content": runtime.context["msgs"]["user_next_step"]})
    return {"messages": messages}
