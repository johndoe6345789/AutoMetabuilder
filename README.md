# AutoMetabuilder

AutoMetabuilder is an AI-powered tool designed to integrate with the metabuilder SDLC workflow.

## Features

- **GitHub Integration**: Automatically fetches context from GitHub Issues and Pull Requests.
- **SDLC Automation**: Can create branches and pull requests based on the AI's decisions.
- **Customizable Prompts**: Loads workflow instructions from a local YAML prompt.

## Configuration

The following environment variables are required:

- `GITHUB_TOKEN`: A GitHub Personal Access Token with repository permissions.
- `GITHUB_REPOSITORY`: The full name of the repository (e.g., `owner/repo`).

## Usage

Run the tool using poetry:

```bash
poetry run autometabuilder
```

## Testing

To run the unit tests:
```bash
PYTHONPATH=src pytest tests/test_main.py tests/test_metadata.py tests/test_roadmap.py
```

To run the Web UI tests (Playwright):
```bash
# First install browsers if you haven't already
playwright install chromium

# Run the UI tests
PYTHONPATH=src pytest tests/ui
```
