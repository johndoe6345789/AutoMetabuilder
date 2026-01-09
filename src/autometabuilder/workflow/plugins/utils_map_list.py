"""Workflow plugin: map list."""
from ..value_helpers import ValueHelpers


def run(runtime, inputs):
    items = ValueHelpers.ensure_list(inputs.get("items"))
    template = inputs.get("template", "{item}")
    mapped = []
    for item in items:
        try:
            mapped.append(template.format(item=item))
        except Exception:  # pylint: disable=broad-exception-caught
            mapped.append(str(item))
    return {"items": mapped}
