# Workflow Architecture Visualization

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        AutoMetabuilder                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Workflow Engine                        │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │            Plugin Registry (78 plugins)           │  │  │
│  │  │  ┌────────────────────────────────────────────┐   │  │  │
│  │  │  │  Backend Infrastructure (8)                │   │  │  │
│  │  │  │  Logic & Comparison (9)                    │   │  │  │
│  │  │  │  List Operations (7)                       │   │  │  │
│  │  │  │  Dictionary Operations (6)                 │   │  │  │
│  │  │  │  String Manipulation (8)                   │   │  │  │
│  │  │  │  Math Operations (10)                      │   │  │  │
│  │  │  │  Type Conversions (7)                      │   │  │  │
│  │  │  │  Control Flow (1)                          │   │  │  │
│  │  │  │  State Management (4)                      │   │  │  │
│  │  │  │  Core AI & Tools (19 existing)            │   │  │  │
│  │  │  └────────────────────────────────────────────┘   │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                                                           │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │              Workflow Packages                     │  │  │
│  │  │  • backend_bootstrap                               │  │  │
│  │  │  • data_processing_demo                            │  │  │
│  │  │  • conditional_logic_demo                          │  │  │
│  │  │  • single_pass, iterative_loop, etc. (existing)   │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                                                           │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │              Workflow Runtime                      │  │  │
│  │  │  • Store (mutable state)                           │  │  │
│  │  │  • Context (immutable config)                      │  │  │
│  │  │  • Variable Binding ($var syntax)                  │  │  │
│  │  │  • Error Handling                                  │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Plugin Execution Flow

```
┌─────────────┐
│   Start     │
│  Workflow   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  Load Workflow Definition (JSON)            │
│  • nodes: array of plugin instances         │
│  • connections: node linkages                │
└──────┬──────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  Initialize Runtime                          │
│  • store = {} (empty state)                  │
│  • context = {config, clients, tools}        │
└──────┬──────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  Execute Node (example: logic.and)           │
│  1. Resolve inputs from store                │
│     values = [$is_adult, $is_passing]        │
│  2. Call plugin: run(runtime, inputs)        │
│  3. Store outputs to runtime.store           │
│     store["result"] = True/False             │
└──────┬──────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  Execute Next Connected Node                 │
│  (repeat until all nodes executed)           │
└──────┬──────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│   Workflow  │
│   Complete  │
└─────────────┘
```

## Plugin Structure

```python
# Generic plugin template
def run(runtime, inputs):
    """
    Args:
        runtime: WorkflowRuntime
            - runtime.store: dict (shared state)
            - runtime.context: dict (config)
            - runtime.logger: Logger
        
        inputs: dict
            - Parameters from workflow definition
            - Can reference store variables with $name
    
    Returns:
        dict: Output values stored in runtime.store
            - Keys become available as $key in later nodes
            - Optional "error" field for error handling
    """
    # Example: math.add
    numbers = inputs.get("numbers", [])
    result = sum(numbers)
    return {"result": result}
```

## Variable Binding Example

```json
{
  "nodes": [
    {
      "id": "node1",
      "type": "var.set",
      "parameters": {
        "key": "user_age",
        "value": 25
      }
    },
    {
      "id": "node2",
      "type": "logic.gte",
      "parameters": {
        "a": "$user_age",      // References store["user_age"]
        "b": 18
      }
    },
    {
      "id": "node3",
      "type": "string.format",
      "parameters": {
        "template": "Age {age} is adult: {is_adult}",
        "variables": {
          "age": "$user_age",       // From node1
          "is_adult": "$result"     // From node2
        }
      }
    }
  ]
}
```

## Backend Bootstrap Workflow

```
┌──────────────────┐
│ Load Messages    │  → store["messages"] = {...}
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Load Metadata    │  → store["metadata"] = {...}
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Load Prompt      │  → store["prompt"] = {...}
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Create GitHub    │  → store["gh"] = GitHubIntegration(...)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Create OpenAI    │  → store["client"] = OpenAI(...)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Load Tools       │  → store["tools"] = [...]
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Build Tool Map   │  → store["tool_map"] = {...}
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Load Plugins     │  → Registers all plugins
└──────────────────┘
```

## Data Processing Demo Workflow

```
┌────────────────┐
│ Create Data    │  numbers = [1,2,3,4,5,6,7,8,9,10]
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Filter Even    │  filtered = [2,4,6,8,10]
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Square Values  │  squared = [4,16,36,64,100]
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Sum Values     │  sum = 220
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Check > 50     │  is_greater = True
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Branch Result  │  → output[0] if True
└───┬────────┬───┘    → output[1] if False
    │        │
    ▼        ▼
  [True]  [False]
    │        │
    ▼        ▼
┌─────────┐ ┌─────────┐
│Success  │ │Failure  │
│Message  │ │Message  │
└────┬────┘ └────┬────┘
     └──────┬────┘
            ▼
    ┌──────────────┐
    │ Store Result │
    └──────────────┘
```

## Plugin Categories & Use Cases

### Backend Infrastructure
**Purpose**: System initialization  
**Use Case**: Replace imperative setup code with declarative workflow

### Logic & Comparison
**Purpose**: Boolean operations  
**Use Case**: Conditional branching, validation rules

### List Operations
**Purpose**: Collection manipulation  
**Use Case**: Data filtering, searching, aggregation

### Dictionary Operations
**Purpose**: Object/map manipulation  
**Use Case**: Configuration management, data extraction

### String Manipulation
**Purpose**: Text processing  
**Use Case**: Formatting, parsing, report generation

### Math Operations
**Purpose**: Arithmetic calculations  
**Use Case**: Score calculations, statistics, metrics

### Type Conversions
**Purpose**: Data type transformations  
**Use Case**: API data normalization, serialization

### Control Flow
**Purpose**: Execution branching  
**Use Case**: State machines, routing logic

### State Management
**Purpose**: Variable storage/retrieval  
**Use Case**: Passing data between distant nodes

## Benefits of This Architecture

### 1. Declarative Programming
- Logic expressed as data (JSON)
- Visual representation possible
- Version controllable

### 2. Composability
- Small plugins combine into complex workflows
- Reusable patterns as packages
- No code duplication

### 3. Testability
- Plugins testable in isolation
- Workflows testable as units
- Mock-free testing

### 4. Extensibility
- New plugins easy to add
- No changes to core engine
- Backward compatible

### 5. Low-Code Capability
- Non-programmers can build workflows
- Drag-and-drop potential
- Template-based development

## Performance Characteristics

- **Plugin Loading**: O(1) - cached after first load
- **Node Execution**: O(n) - linear in number of nodes
- **Variable Resolution**: O(1) - dict lookup
- **Memory Usage**: O(m) - proportional to store size
- **Scalability**: Each workflow runs independently

## Future Extensions

### More Plugins
- File I/O operations
- HTTP/REST calls
- Database queries
- Date/time operations
- Regular expressions
- Crypto operations

### Advanced Features
- Parallel execution
- Async operations
- Error recovery
- Workflow versioning
- Performance profiling

### Developer Tools
- Visual workflow editor
- Plugin scaffolding CLI
- Workflow debugger
- Performance analyzer
- Template marketplace
