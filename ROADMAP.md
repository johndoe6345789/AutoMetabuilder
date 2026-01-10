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
- [x] **Metadata modularization**: Split `metadata.json` into focused include files (settings, suggestions, workflow plugin defs) and support directory-based loads.
- [x] **Tool spec modularization**: Break `tools.json` into category files and load them as a directory.
- [x] **Translation assets modularization**: Store messages per language in grouped JSON directories and update loaders/writers accordingly.
- [x] **UI test decomposition**: Split Playwright UI tests into focused modules with shared helpers.

```json
{
"$schema": "https://json-schema.org/draft/2020-12/schema",
"$id": "https://example.com/schemas/n8n-workflow.schema.json",
"title": "N8N-Style Workflow",
"type": "object",
"additionalProperties": false,
"required": ["name", "nodes", "connections"],
"properties": {
"id": {
"description": "Optional external identifier (DB id, UUID, etc.).",
"type": ["string", "integer"]
},
"name": {
"type": "string",
"minLength": 1
},
"active": {
"type": "boolean",
"default": false
},
"versionId": {
"description": "Optional version identifier for optimistic concurrency.",
"type": "string"
},
"createdAt": {
"type": "string",
"format": "date-time"
},
"updatedAt": {
"type": "string",
"format": "date-time"
},
"tags": {
"type": "array",
"items": { "$ref": "#/$defs/tag" },
"default": []
},
"meta": {
"description": "Arbitrary metadata. Keep stable keys for tooling.",
"type": "object",
"additionalProperties": true,
"default": {}
},
"settings": {
"$ref": "#/$defs/workflowSettings"
},
"pinData": {
"description": "Optional pinned execution data (useful for dev).",
"type": "object",
"additionalProperties": {
"type": "array",
"items": {
"type": "object",
"additionalProperties": true
}
}
},
"nodes": {
"type": "array",
"minItems": 1,
"items": { "$ref": "#/$defs/node" }
},
"connections": {
"$ref": "#/$defs/connections"
},
"staticData": {
"description": "Reserved for engine-managed workflow state.",
"type": "object",
"additionalProperties": true,
"default": {}
},
"credentials": {
"description": "Optional top-level credential bindings (engine-specific).",
"type": "array",
"items": { "$ref": "#/$defs/credentialBinding" },
"default": []
},
"triggers": {
"description": "Optional explicit trigger declarations for event-driven workflows.",
"type": "array",
"default": [],
"items": { "$ref": "#/$defs/trigger" }
}
},
"$defs": {
"tag": {
"type": "object",
"additionalProperties": false,
"required": ["name"],
"properties": {
"id": { "type": ["string", "integer"] },
"name": { "type": "string", "minLength": 1 }
}
},
"workflowSettings": {
"type": "object",
"additionalProperties": false,
"properties": {
"timezone": {
"description": "IANA timezone name, e.g. Europe/London.",
"type": "string"
},
"executionTimeout": {
"description": "Hard timeout in seconds for a workflow execution.",
"type": "integer",
"minimum": 0
},
"saveExecutionProgress": {
"type": "boolean",
"default": true
},
"saveManualExecutions": {
"type": "boolean",
"default": true
},
"saveDataErrorExecution": {
"description": "Persist execution data on error.",
"type": "string",
"enum": ["all", "none"],
"default": "all"
},
"saveDataSuccessExecution": {
"description": "Persist execution data on success.",
"type": "string",
"enum": ["all", "none"],
"default": "all"
},
"saveDataManualExecution": {
"description": "Persist execution data for manual runs.",
"type": "string",
"enum": ["all", "none"],
"default": "all"
},
"errorWorkflowId": {
"description": "Optional workflow id to call on error.",
"type": ["string", "integer"]
},
"callerPolicy": {
"description": "Optional policy controlling which workflows can call this workflow.",
"type": "string"
}
},
"default": {}
},
"node": {
"type": "object",
"additionalProperties": false,
"required": ["id", "name", "type", "typeVersion", "position"],
"properties": {
"id": {
"description": "Stable unique id within the workflow. Prefer UUID.",
"type": "string",
"minLength": 1
},
"name": {
"description": "Human-friendly name; should be unique in workflow.",
"type": "string",
"minLength": 1
},
"type": {
"description": "Node type identifier, e.g. n8n-nodes-base.httpRequest.",
"type": "string",
"minLength": 1
},
"typeVersion": {
"description": "Node implementation version.",
"type": ["integer", "number"],
"minimum": 1
},
"disabled": {
"type": "boolean",
"default": false
},
"notes": {
"type": "string",
"default": ""
},
"notesInFlow": {
"description": "When true, notes are displayed on canvas.",
"type": "boolean",
"default": false
},
"retryOnFail": {
"type": "boolean",
"default": false
},
"maxTries": {
"type": "integer",
"minimum": 1
},
"waitBetweenTries": {
"description": "Milliseconds.",
"type": "integer",
"minimum": 0
},
"continueOnFail": {
"type": "boolean",
"default": false
},
"alwaysOutputData": {
"type": "boolean",
"default": false
},
"executeOnce": {
"description": "If true, node executes only once per execution (engine-dependent).",
"type": "boolean",
"default": false
},
"position": {
"$ref": "#/$defs/position"
},
"parameters": {
"description": "Node-specific parameters. Typically JSON-serializable.",
"type": "object",
"additionalProperties": true,
"default": {}
},
"credentials": {
"description": "Node-level credential references.",
"type": "object",
"additionalProperties": {
"$ref": "#/$defs/credentialRef"
},
"default": {}
},
"webhookId": {
"description": "Optional webhook id (for webhook-based trigger nodes).",
"type": "string"
},
"onError": {
"description": "Node-level error routing policy (engine-dependent).",
"type": "string",
"enum": ["stopWorkflow", "continueRegularOutput", "continueErrorOutput"]
}
}
},
"position": {
"type": "array",
"minItems": 2,
"maxItems": 2,
"items": {
"type": "number"
}
},
"credentialRef": {
"type": "object",
"additionalProperties": false,
"required": ["id"],
"properties": {
"id": {
"description": "Credential id or stable key.",
"type": ["string", "integer"]
},
"name": {
"description": "Optional human label.",
"type": "string"
}
}
},
"credentialBinding": {
"type": "object",
"additionalProperties": false,
"required": ["nodeId", "credentialType", "credentialId"],
"properties": {
"nodeId": { "type": "string", "minLength": 1 },
"credentialType": { "type": "string", "minLength": 1 },
"credentialId": { "type": ["string", "integer"] }
}
},
"connections": {
"description": "Adjacency map: fromNodeName -> outputType -> outputIndex -> array of targets.",
"type": "object",
"additionalProperties": {
"$ref": "#/$defs/nodeConnectionsByType"
},
"default": {}
},
"nodeConnectionsByType": {
"type": "object",
"additionalProperties": false,
"properties": {
"main": {
"$ref": "#/$defs/outputIndexMap"
},
"error": {
"$ref": "#/$defs/outputIndexMap"
}
},
"anyOf": [
{ "required": ["main"] },
{ "required": ["error"] }
]
},
"outputIndexMap": {
"description": "Output index -> array of connection targets.",
"type": "object",
"additionalProperties": {
"type": "array",
"items": { "$ref": "#/$defs/connectionTarget" }
},
"default": {}
},
"connectionTarget": {
"type": "object",
"additionalProperties": false,
"required": ["node", "type", "index"],
"properties": {
"node": {
"description": "Target node name (n8n uses node 'name' in connections).",
"type": "string",
"minLength": 1
},
"type": {
"description": "Input type on target node (typically 'main' or 'error').",
"type": "string",
"minLength": 1
},
"index": {
"description": "Input index on target node.",
"type": "integer",
"minimum": 0
}
}
},
"trigger": {
"type": "object",
"additionalProperties": false,
"required": ["nodeId", "kind"],
"properties": {
"nodeId": { "type": "string", "minLength": 1 },
"kind": {
"type": "string",
"enum": ["webhook", "schedule", "queue", "email", "poll", "manual", "other"]
},
"enabled": { "type": "boolean", "default": true },
"meta": {
"description": "Trigger-kind-specific metadata for routing/registration.",
"type": "object",
"additionalProperties": true,
"default": {}
}
}
}
}
}
```


```json
example data:
{
"id": "wf-001",
"name": "Example HTTP → Transform → Log",
"active": false,
"createdAt": "2026-01-10T10:15:00Z",
"updatedAt": "2026-01-10T10:20:00Z",
"tags": [
{ "id": 1, "name": "example" },
{ "id": 2, "name": "demo" }
],
"settings": {
"timezone": "Europe/London",
"executionTimeout": 300,
"saveExecutionProgress": true,
"saveDataErrorExecution": "all",
"saveDataSuccessExecution": "all"
},
"nodes": [
{
"id": "node-1",
"name": "HTTP Request",
"type": "n8n-nodes-base.httpRequest",
"typeVersion": 4,
"position": [0, 0],
"parameters": {
"method": "GET",
"url": "https://api.example.com/users",
"responseFormat": "json"
},
"credentials": {
"httpBasicAuth": {
"id": "cred-123",
"name": "Example API Auth"
}
}
},
{
"id": "node-2",
"name": "Transform Data",
"type": "n8n-nodes-base.function",
"typeVersion": 1,
"position": [300, 0],
"parameters": {
"code": "return items.map(i => ({ json: { id: i.json.id, email: i.json.email } }));"
}
},
{
"id": "node-3",
"name": "Log Output",
"type": "n8n-nodes-base.noOp",
"typeVersion": 1,
"position": [600, 0],
"parameters": {}
}
],
"connections": {
"HTTP Request": {
"main": {
"0": [
{
"node": "Transform Data",
"type": "main",
"index": 0
}
]
}
},
"Transform Data": {
"main": {
"0": [
{
"node": "Log Output",
"type": "main",
"index": 0
}
]
}
}
},
"staticData": {},
"credentials": [
{
"nodeId": "node-1",
"credentialType": "httpBasicAuth",
"credentialId": "cred-123"
}
]
}
```
