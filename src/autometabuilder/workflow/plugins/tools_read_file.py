"""Workflow plugin: read file."""


def run(runtime, inputs):
    result = runtime.tool_runner.call("read_file", path=inputs.get("path"))
    return {"content": result}
