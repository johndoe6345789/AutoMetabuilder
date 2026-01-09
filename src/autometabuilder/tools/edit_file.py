"""Edit file content with search/replace."""

def edit_file(path: str, search: str, replace: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if search not in content:
            return f"Error: '{search}' not found in {path}"
        new_content = content.replace(search, replace)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return f"Successfully edited {path}"
    except Exception as error:  # pylint: disable=broad-exception-caught
        return f"Error editing file {path}: {error}"
