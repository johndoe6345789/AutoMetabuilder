"""Workflow plugin: seed messages."""


def run(runtime, inputs):
    prompt = runtime.context["prompt"]
    return {"messages": list(prompt["messages"])}
