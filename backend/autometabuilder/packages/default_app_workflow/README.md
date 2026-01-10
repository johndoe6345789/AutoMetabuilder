# Default Application Workflow

This workflow package provides a comprehensive, production-ready workflow that combines backend initialization with an iterative AI agent loop. It demonstrates the "dogfooding" approach where AutoMetabuilder's own application logic is expressed as a declarative workflow.

## Overview

The Default Application Workflow is a complete end-to-end workflow that:

1. **Bootstraps the backend** - Loads all necessary configuration, clients, and tools
2. **Executes the AI loop** - Runs the core AutoMetabuilder agent with tool calling capabilities

This workflow replaces the imperative Python code that was previously in `app_runner.py`, making the application logic:
- **Declarative** - Expressed as data (JSON) rather than code
- **Visual** - Can be visualized as a node graph
- **Testable** - Each node can be tested independently
- **Modular** - Easy to modify, extend, or replace nodes

## Workflow Structure

### Phase 1: Backend Bootstrap (9 nodes)

These nodes initialize all backend services and dependencies:

1. **Load Messages** (`backend.load_messages`)
   - Loads internationalized translation messages
   - Stores in `runtime.context["msgs"]`

2. **Load Metadata** (`backend.load_metadata`)
   - Loads `metadata.json` configuration
   - Stores in `runtime.context["metadata"]`

3. **Load Prompt** (`backend.load_prompt`)
   - Loads `prompt.yml` configuration
   - Resolves model name from environment or prompt
   - Stores in `runtime.context["prompt"]` and `runtime.context["model_name"]`

4. **Create GitHub Client** (`backend.create_github`)
   - Initializes GitHub API client
   - Requires `GITHUB_TOKEN` environment variable
   - Stores in `runtime.context["gh"]`

5. **Create OpenAI Client** (`backend.create_openai`)
   - Initializes OpenAI/LLM client
   - Uses GitHub token for authentication
   - Stores in `runtime.context["client"]`

6. **Load Tools** (`backend.load_tools`)
   - Loads tool definitions from metadata
   - Stores in `runtime.context["tools"]`

7. **Build Tool Map** (`backend.build_tool_map`)
   - Creates callable tool registry
   - Maps tool names to implementations
   - Stores in `runtime.context["tool_map"]`

8. **Load Plugins** (`backend.load_plugins`)
   - Loads any custom user plugins
   - Registers them in the tool map

9. **Load Tool Policies** (`backend.load_tool_policies`)
   - Loads tool execution policies
   - Defines which tools require confirmation
   - Stores in `runtime.context["tool_policies"]`

### Phase 2: AI Agent Loop (8 nodes)

These nodes execute the core AutoMetabuilder agent:

1. **Load Context** (`core.load_context`)
   - Loads SDLC context (roadmap, issues, PRs)
   - Provides situational awareness

2. **Seed Messages** (`core.seed_messages`)
   - Initializes empty message array
   - Prepares conversation state

3. **Append Context** (`core.append_context_message`)
   - Adds SDLC context to messages
   - Gives AI awareness of repository state

4. **Append User Instruction** (`core.append_user_instruction`)
   - Adds user's task instruction
   - Defines what the AI should accomplish

5. **Main Loop** (`control.loop`)
   - Iterative execution controller
   - Runs up to 10 iterations
   - Stops when AI has no more tool calls

6. **AI Request** (`core.ai_request`)
   - Sends messages to LLM
   - Gets back response and optional tool calls

7. **Run Tool Calls** (`core.run_tool_calls`)
   - Executes requested tool calls
   - Handles confirmation prompts
   - Returns results

8. **Append Tool Results** (`core.append_tool_results`)
   - Adds tool results to messages
   - Loops back to Main Loop for next iteration

## Usage

This workflow is automatically loaded when you run AutoMetabuilder:

```bash
# Set in metadata.json
{
  "workflow_path": "packages/default_app_workflow/workflow.json"
}

# Then run
autometabuilder
```

The `app_runner.py` module now simply:
1. Loads environment and configuration
2. Parses command line arguments
3. Loads this workflow
4. Executes it

## Benefits of Workflow-Based Architecture

### 1. Separation of Concerns
- Backend initialization is isolated from AI logic
- Each phase can be tested independently
- Easy to add new initialization steps

### 2. Flexibility
- Swap out individual nodes without touching code
- Try different AI loop strategies
- Add monitoring or logging nodes

### 3. Observability
- Clear execution order
- Easy to trace data flow
- Can add debug nodes at any point

### 4. Extensibility
- Create variant workflows for different use cases
- Mix and match nodes from other packages
- Build custom workflows without code changes

## Data Flow

```
Environment Variables (GITHUB_TOKEN, LLM_MODEL)
    ↓
Backend Bootstrap Phase
    ↓
runtime.context populated with:
    - msgs (translations)
    - metadata (config)
    - prompt (agent instructions)
    - model_name (LLM to use)
    - gh (GitHub client)
    - client (OpenAI client)
    - tools (tool definitions)
    - tool_map (callable tools)
    - tool_policies (execution policies)
    ↓
AI Agent Loop Phase
    ↓
Iterative execution:
    - Load SDLC context
    - Send to LLM with tools
    - Execute tool calls
    - Append results
    - Repeat until done
```

## Customization

To create a custom variant:

1. Copy this package:
   ```bash
   cp -r packages/default_app_workflow packages/my_custom_workflow
   ```

2. Edit `workflow.json`:
   - Add/remove nodes
   - Change connections
   - Modify parameters

3. Update `package.json`:
   ```json
   {
     "name": "my_custom_workflow",
     "description": "My custom AutoMetabuilder workflow"
   }
   ```

4. Update `metadata.json`:
   ```json
   {
     "workflow_path": "packages/my_custom_workflow/workflow.json"
   }
   ```

## Related Workflows

- **backend_bootstrap** - Just the initialization phase, useful for testing
- **single_pass** - One-shot AI request without iteration
- **iterative_loop** - Just the AI loop, assumes backend is initialized
- **plan_execute_summarize** - Multi-phase workflow with explicit planning

## Technical Notes

### Runtime Context vs Store

- **Context** (`runtime.context`): Immutable configuration and dependencies
  - Set once during bootstrap
  - Available to all nodes
  - Contains clients, tools, settings

- **Store** (`runtime.store`): Mutable execution state
  - Changes during execution
  - Node outputs stored here
  - Temporary working data

### Plugin Responsibility

Backend workflow plugins (`backend.*`) have dual responsibility:
1. Return result in output dict (for store)
2. Update `runtime.context` directly (for downstream plugins)

This ensures both workflow data flow and imperative access work correctly.

## Version History

- **1.0.0** - Initial release combining backend bootstrap and AI loop
  - Replaces imperative `app_runner.py` logic
  - Enables "dogfooding" of workflow architecture
  - 17 nodes total: 9 bootstrap + 8 AI loop

## See Also

- [Workflow Architecture](../../../../docs/archive/WORKFLOW_ARCHITECTURE.md)
- [Workflow Plugin Expansion](../../../../docs/archive/WORKFLOW_PLUGIN_EXPANSION.md)
- [Workflow Plugins README](../../workflow/plugins/README.md)
