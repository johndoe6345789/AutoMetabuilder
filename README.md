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

- `backend/`: FastAPI/Flask API, workflow controllers, metadata, and CLI modules.
- `frontend/`: Next.js app (using the app router) that talks to the backend over the REST endpoints.

## Usage

Run the CLI or the web UI via Poetry (the project uses the backend package defined in `pyproject.toml`):

```bash
poetry install
poetry run autometabuilder    # starts the CLI or the web server when `--web` is supplied
```

### Frontend development

```bash
cd frontend
npm install
npm run dev --webpack        # runs the Material UI-based Next.js app located inside frontend/autometabuilder
```

The Next.js app now lives under `frontend/autometabuilder` and uses Material UI panels + webhook helpers to react to workflow runs; it still reads translations, workflows, and metadata from the Flask `/api/*` surface. Override `NEXT_PUBLIC_API_BASE` to point to a remote backend if needed.

## Testing & linting

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
