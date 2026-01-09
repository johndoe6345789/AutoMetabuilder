"""Workflow plugin: run tests."""


def run(runtime, inputs):
    result = runtime.tool_runner.call("run_tests", path=inputs.get("path", "tests"))
    return {"results": result}
