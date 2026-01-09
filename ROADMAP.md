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
- [/] **Dockerization**: Provide a Dockerfile and docker-compose for easy environment setup. Added `run_docker_task` tool.
- [ ] **Extended Toolset**: Add tools for dependency management (poetry) and file manipulation (read/write/edit).
- [ ] **Self-Improvement**: Allow the bot to suggest and apply changes to its own `prompt.yml` or `tools.json`.
- [ ] **Robust Error Handling**: Implement exponential backoff for API calls and better error recovery.
- [ ] **Monitoring & Logging**: Structured logging and status reporting for long-running tasks.
