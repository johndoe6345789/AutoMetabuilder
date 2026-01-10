"""Write file content."""

def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as error:  # pylint: disable=broad-exception-caught
        return f"Error writing to file {path}: {error}"
