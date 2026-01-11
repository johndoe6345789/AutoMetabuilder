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

## Directory layout

- `backend/`: Workflow engine, plugins, data access, and CLI modules.
  - `workflow/`: Workflow engine and 115+ workflow plugins
  - `data/`: Data access functions and Flask routes
  - `packages/`: Workflow packages (including `web_server_bootstrap`)
- `frontend/`: Next.js app (using the app router) that talks to the backend over the REST endpoints.

## Usage

Run the CLI or the web UI via Poetry (the project uses the backend package defined in `pyproject.toml`):

```bash
poetry install
# Start web server (workflow-based)
poetry run autometabuilder --web

# Or run the main workflow
poetry run autometabuilder
```

### Frontend development

```bash
cd frontend
npm install
npm run dev --webpack        # runs the Material UI-based Next.js app located inside frontend/autometabuilder
```

The Next.js app now lives under `frontend/autometabuilder` and uses Material UI panels + webhook helpers to react to workflow runs; it still reads translations, workflows, and metadata from the Flask `/api/*` surface. Override `NEXT_PUBLIC_API_BASE` to point to a remote backend if needed.

## Testing & linting

### Workflow JSON Validation

Validate all workflow JSON files against the N8N schema:

```bash
poetry run validate-workflows
```

See [docs/WORKFLOW_VALIDATION.md](docs/WORKFLOW_VALIDATION.md) for detailed documentation.

### Workflow Triggers

Workflows now support triggers to define entry points. See [docs/TRIGGER_USAGE.md](docs/TRIGGER_USAGE.md) for usage guide.

### Python

```bash
PYTHONPATH=backend pytest backend/tests/test_main.py backend/tests/test_metadata.py backend/tests/test_roadmap.py
PYTHONPATH=backend pytest backend/tests/ui           # Playwright UI tests; they skip when socket creation is blocked
```

### Storybook & Playwright

```bash
cd frontend
npx playwright install chromium
npm run storybook           # launch the component catalog at http://localhost:6006
npm run build:storybook     # compile the catalog to static files
npm run test:e2e            # runs the Playwright tests defined under frontend/playwright/tests
```

Storybook renders the Material UI sections from `frontend/autometabuilder/components`, and Playwright now targets `http://localhost:3000` (override with `NEXT_PUBLIC_API_BASE` if your backend runs elsewhere).

### Frontend

```bash
cd frontend
npm run lint
npm run build --webpack        # currently fails in the sandbox because compiling tries to bind new ports
```

The Webpack build step is disabled in this container because the sandbox denies the port binding Turbopack (and its subprocesses) needs; the rest of the stack, including lint/test, succeeds.
