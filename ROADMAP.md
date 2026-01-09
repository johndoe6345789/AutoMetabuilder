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

## Phase 3: Advanced Automation
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
