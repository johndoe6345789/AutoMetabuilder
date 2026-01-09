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
- [ ] **n8n-Style Visual Workflow Canvas (Breakdown)**:
- [ ] **Canvas Layout Engine**: DAG layout, node positioning, zoom/pan, and fit-to-view.
- [x] **Node Palette + Search**: Categorized plugin library with search and click-to-add.
- [ ] **Palette Tags + Drag-to-Canvas**: Add tags, drag handles, and drag/drop placement.
- [ ] **Atomic Node Cards**: Compact node tiles with status badge, type icon, and inline rename.
- [ ] **Ports + Connectors**: Visual input/output ports with link creation + validation.
- [ ] **Edge Routing**: Orthogonal edge routing with arrowheads, hover/selection state.
- [ ] **Mini Map**: Overview map for large workflows with viewport control.
- [ ] **Selection + Multi-Edit**: Multi-select nodes, bulk delete, and bulk edit fields.
- [ ] **Inspector Panel**: Right-side inspector to edit node inputs/outputs/conditions.
- [ ] **Inline Validation**: Missing input warnings, type mismatch hints, and disabled run cues.
- [ ] **Execution Preview**: Simulate data flow highlights and show store bindings.
- [ ] **Auto-Save Drafts**: Local draft save/restore with change markers.
- [ ] **Template Import/Export**: Export current workflow and import to apply or merge.
- [ ] **Keyboard Shortcuts**: Add node, delete, duplicate, undo/redo, and search.
- [ ] **Undo/Redo Stack**: Reversible edits for canvas and inspector changes.
- [ ] **Context Menu**: Right-click actions for node, edge, and canvas.
- [ ] **Performance Tuning**: Virtualized node rendering for large graphs.
