"""Workflow plugin: create pull request."""


def run(runtime, inputs):
    result = runtime.tool_runner.call(
        "create_pull_request",
        title=inputs.get("title"),
        body=inputs.get("body"),
        head_branch=inputs.get("head_branch"),
        base_branch=inputs.get("base_branch", "main")
    )
    return {"result": result}
