# Roadmap

## Phase 1: Foundation
- [x] Basic GitHub Integration (fetching issues/PRs)
- [x] Local YAML prompt loading
- [x] Tool-based SDLC operations (branch/PR creation)
- [x] Multi-language support for messages

## Phase 2: Enhanced Context & Reasoning
- [x] **Roadmap Awareness**: Bot should explicitly read and update `ROADMAP.md`.
- [x] **Repository Indexing**: Implement a way to index the codebase for better context.
- [x] **Declarative Task Processing**: Move more logic into JSON/YAML specifications.
- [x] **Feedback Loop**: Support for the AI to read comments on PRs it created.

## Phase 3: Advanced Automation (MVP)
- [x] **Automated Testing**: Integration with test runners to verify changes before PR.
- [x] **Linting Integration**: Automatically run and fix linting issues.
- [x] **Multi-Model Support**: Easily switch between different LLM providers.
- [x] **CI/CD Integration**: Github Actions to run AutoMetabuilder on schedule or trigger.

## Phase 4: Optimization & Scalability
- [x] **Dockerization**: Provide a Dockerfile and docker-compose for easy environment setup. Added `run_docker_task` tool.
- [x] **Extended Toolset**: Add tools for dependency management (poetry) and file manipulation (read/write/edit).
- [x] **Self-Improvement**: Allow the bot to suggest and apply changes to its own `prompt.yml` or `tools.json`.
- [x] **Robust Error Handling**: Implement exponential backoff for API calls and better error recovery.
- [x] **Monitoring & Logging**: Structured logging and status reporting for long-running tasks.

## Phase 5: Ecosystem & User Experience
- [x] **Web UI**: A simple dashboard to monitor tasks and approve tool executions. Enhanced with settings and translation management.
- [x] **Plugin System**: Allow users to add custom tools via a plugin directory.
- [x] **Slack/Discord Integration**: Command and notify the bot from chat platforms.

## Phase 6: Advanced Web UI & Remote Control
- [x] **Remote Command Execution**: Trigger bot runs from the Web UI.
- [x] **User Authentication**: Secure the Web UI with login.
- [x] **Visual Task Progress**: Real-time progress bars for long-running tasks.

## Phase 7: Workflow UX & Component Library
- [x] **Node-Based Workflow Engine**: Replace task steps with micro-plugin nodes (inputs/outputs, loops).
- [x] **Workflow Templates**: Package reusable workflow presets (blank, single pass, iterative loop, plan/execute/summarize).
- [x] **Workflow Template Picker**: AJAX-loaded catalog with localized labels/descriptions.
- [x] **Atomic Jinja Components**: Split dashboard/prompt/settings/translations/sidebar into single-macro files.
- [x] **AJAX Navigation Data**: Render sidebar links from API payload with a client-side fallback.
- [x] **Node Palette + Search**: Categorized plugin library with search and click-to-add.

## Phase 8: Modern Frontend Platform
- [x] **Flask + Next.js split**: Replace the Jinja-based FastAPI UI with a Flask REST backend and Next.js frontend consuming metadata, translations, workflows, logs, and nav via AJAX.
- [x] **Atomic Next sections**: Compose dashboard, workflow builder, prompt editor, settings, and translation editor into dedicated components powered by localized strings.
- [x] **Workflow templates & navigation JSON**: Serve workflow packages, nav items, and translation mappings from metadata-backed JSON endpoints.
- [x] **Document build constraints**: Record that `next build --webpack` fails in this sandbox because bundlers attempt to bind new ports, and continue iterating locally.
- [x] **Storybook + Playwright**: Add a Storybook catalog for the Material UI sections and a Playwright suite (with `npm run test:e2e`) so the frontend gets visual regression/backstop coverage tied to the Flask API.
- [x] **Material UI + webhooks**: Drive the dashboard with Material UI surfaces and a lightweight webhook emitter/listener so downstream components can react to run events without prop drilling.

## Phase 9: Visual Workflow Canvas
- [ ] **n8n-Style Visual Workflow Canvas (Breakdown)**: Capture node + edge details so the canvas understands the micro-plugin graphs.
- [ ] **Canvas Layout Engine**: DAG layout, zoom/pan, and background grid to keep large graphs navigable.
- [ ] **Palette Tags + Drag-to-Canvas**: Tag nodes, add drag handles, and allow drag/drop placement onto the canvas.
- [ ] **Atomic Node Cards**: Compact tile UI with status badges, icons, and inline rename/edit actions.
- [ ] **Ports + Connectors**: Visualize input/output ports with validation and JSON metadata.
- [ ] **Edge Routing + Mini Map**: Orthogonal edges with hover/selection states plus a mini overview map.
- [ ] **Selection + Inspector**: Multi-select, bulk edit, right-side inspector for node/edge properties.
- [ ] **Inline Validation & Execution Preview**: Warn on missing inputs and simulate data flow + store bindings.
- [ ] **Workspace Controls**: Auto-save drafts, template import/export, keyboard shortcuts, undo/redo stack, context menus, and performant rendering for big graphs.

## Phase 10: Workflow & UI Refinement
- [ ] **Atomic Workflow Plugin System**: Define micro plugin/lambda nodes (filters, maps, reduces, fetches, branches, AI requests) with clear multi-input/multi-output contracts so workflows mirror n8n’s granularity and can broadcast webhook events.
- [ ] **Workflow Package Templates**: Package curated templates (blank, single pass, contextual loops, plan/execute/summarize, iteration controls like “1 run”, “X runs”, “YOLO”, “Stop at MVP”) and surface them via AJAX-enabled picker so builders import pre-configured flows.
- [ ] **AJAX Configuration Delivery**: Serve navigation, metadata, translations, workflow packages, and script wiring from dedicated endpoints instead of embedding JSON in pages; let the client hydrate via fetch loops.
- [ ] **Localized UI Editors**: Rework settings, translation, and prompt editors to show human descriptions, full CRUD flows, and ensure metadata/strings come from translation files so Playwright can assert localization coverage.
- [ ] **Workflow Action Library**: Build an atomic action library with declarative JSON definitions for each filter, transformer, and AI request, wire them into the plugin registry, and add DEBUG/INFO/TRACE/ERROR logging for execution visibility.
- [ ] **Testing & Quality**: Expand Playwright suites to cover internationalization/localization, workflow templates, and AJAX-driven navigation; continue running unit tests, static analysis, linters, and e2e jobs to close the testing triangle.
- [ ] **Styling & Tooling**: Investigate SASS adoption for the Material UI theme, keep component files ≤100 LOC, and enforce plugin/service/controller patterns with DI so styles stay modular.
- [ ] **Component Decomposition**: Audit remaining Jinja templates and Next.js components so each file owns a single macro/component, loops over declarative data, and delegates translation lookups to shared helpers.

## Phase 11: Technical Debt
- [x] **Structured workflow logging**: Add debug/trace warnings when parsing workflow definitions so graph builders surface malformed JSON and unbound bindings.
- [x] **Route modularization**: Split `backend/autometabuilder/web/server.py` into focused route modules or blueprints so each file stays under 100 LOC and supports DI of helpers.
- [x] **AJAX contract tests**: Expand the backend test suite to cover `/api/workflow/graph`, `/api/workflow/plugins`, and nav/translation payloads with mocked metadata so API drift is caught early.
