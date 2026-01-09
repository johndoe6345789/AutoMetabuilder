"""Read file content."""

def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as error:  # pylint: disable=broad-exception-caught
        return f"Error reading file {path}: {error}"
