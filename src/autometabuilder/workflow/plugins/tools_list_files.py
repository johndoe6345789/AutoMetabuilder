"""Workflow plugin: list files."""


def run(runtime, inputs):
    result = runtime.tool_runner.call("list_files", directory=inputs.get("path", "."))
    return {"files": result}
