"""Workflow plugin: run lint."""


def run(runtime, inputs):
    result = runtime.tool_runner.call("run_lint", path=inputs.get("path", "src"))
    return {"results": result}
