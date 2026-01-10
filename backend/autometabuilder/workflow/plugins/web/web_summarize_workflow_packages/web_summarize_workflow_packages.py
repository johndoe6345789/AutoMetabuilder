"""Workflow plugin: summarize workflow packages."""


def run(_runtime, inputs):
    """Summarize workflow packages."""
    packages = inputs.get("packages", [])
    
    summary = []
    for pkg in packages:
        summary.append({
            "id": pkg["id"],
            "name": pkg.get("name", pkg["id"]),
            "label": pkg.get("label") or pkg["id"],
            "description": pkg.get("description", ""),
            "tags": pkg.get("tags", []),
            "version": pkg.get("version", "1.0.0"),
            "category": pkg.get("category", "templates"),
        })
    
    return {"result": summary}
