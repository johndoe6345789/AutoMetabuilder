# Workflow Plugins Documentation

This document describes all available workflow plugins for building declarative n8n-style workflows.

## Directory Structure

Plugins are now organized into subdirectories by category:
- **backend/** - Backend infrastructure and initialization plugins (12 plugins)
- **core/** - Core workflow orchestration plugins (7 plugins)
- **tools/** - Tool execution and development plugins (7 plugins)
- **notifications/** - External notification integrations (3 plugins)
- **logic/** - Logic and comparison operations (9 plugins)
- **list/** - List/array operations (7 plugins)
- **dict/** - Dictionary/object operations (6 plugins)
- **string/** - String manipulation (8 plugins)
- **math/** - Mathematical operations (10 plugins)
- **convert/** - Type conversions (7 plugins)
- **control/** - Control flow (1 plugin)
- **var/** - Variable management (4 plugins)
- **test/** - Unit testing and assertions (5 plugins)
- **utils/** - Utility functions (7 plugins)
- **web/** - Web UI and Flask operations (26 plugins)

**Total: 93 plugins**

## Categories

- [Core Plugins](#core-plugins) - AI and context management
- [Tool Plugins](#tool-plugins) - File system and SDLC operations
- [Notification Plugins](#notification-plugins) - External notification integrations
- [Logic Plugins](#logic-plugins) - Boolean logic and comparisons
- [List Plugins](#list-plugins) - Collection operations
- [Dictionary Plugins](#dictionary-plugins) - Object/map operations
- [String Plugins](#string-plugins) - Text manipulation
- [Math Plugins](#math-plugins) - Arithmetic operations
- [Conversion Plugins](#conversion-plugins) - Type conversions
- [Control Flow Plugins](#control-flow-plugins) - Branching and switching
- [Variable Plugins](#variable-plugins) - State management
- [Test Plugins](#test-plugins) - Unit testing and assertions
- [Backend Plugins](#backend-plugins) - System initialization
- [Utility Plugins](#utility-plugins) - General utilities
- [Web Plugins](#web-plugins) - Web UI and Flask operations

---

## Core Plugins

### `core.load_context`
Load SDLC context (roadmap, issues, PRs) from GitHub.

**Outputs:**
- `context` - String containing SDLC context

### `core.seed_messages`
Initialize empty message array for AI conversation.

**Outputs:**
- `messages` - Empty array

### `core.append_context_message`
Add context to messages array.

**Inputs:**
- `messages` - Message array
- `context` - Context text

**Outputs:**
- `messages` - Updated array

### `core.append_user_instruction`
Add user instruction to messages.

**Inputs:**
- `messages` - Message array

**Outputs:**
- `messages` - Updated array

### `core.ai_request`
Make AI request with messages.

**Inputs:**
- `messages` - Message array

**Outputs:**
- `response` - AI response message
- `has_tool_calls` - Boolean
- `tool_calls_count` - Number

### `core.run_tool_calls`
Execute tool calls from AI response.

**Inputs:**
- `response` - AI response message

**Outputs:**
- `tool_results` - Array of results

### `core.append_tool_results`
Add tool results to messages.

**Inputs:**
- `messages` - Message array
- `tool_results` - Tool results array

**Outputs:**
- `messages` - Updated array

---

## Tool Plugins

### `tools.list_files`
List files in directory.

**Inputs:**
- `path` - Directory path

**Outputs:**
- `files` - Array of file paths

### `tools.read_file`
Read file contents.

**Inputs:**
- `path` - File path

**Outputs:**
- `content` - File content

### `tools.run_tests`
Execute test suite.

**Outputs:**
- `success` - Boolean
- `output` - Test output

### `tools.run_lint`
Run linter.

**Outputs:**
- `success` - Boolean
- `output` - Lint output

### `tools.create_branch`
Create Git branch.

**Inputs:**
- `branch_name` - Branch name

**Outputs:**
- `success` - Boolean

### `tools.create_pull_request`
Create GitHub pull request.

**Inputs:**
- `title` - PR title
- `body` - PR description

**Outputs:**
- `pr_number` - PR number

### `tools.run_docker`
Run command inside Docker container.

**Inputs:**
- `image` - Docker image name
- `command` - Command to execute
- `volumes` - Optional volume mappings dict
- `workdir` - Optional working directory

**Outputs:**
- `output` - Command output
- `error` - Error message (if any)

---

## Notification Plugins

### `notifications.slack`
Send notification to Slack.

**Inputs:**
- `message` - The message to send
- `token` - Optional Slack bot token (defaults to SLACK_BOT_TOKEN env var)
- `channel` - Optional channel (defaults to SLACK_CHANNEL env var)

**Outputs:**
- `success` - Boolean (true if sent successfully)
- `message` - Status message
- `error` - Error message (if failed)
- `skipped` - Boolean (true if skipped due to missing config)

### `notifications.discord`
Send notification to Discord.

**Inputs:**
- `message` - The message to send
- `token` - Optional Discord bot token (defaults to DISCORD_BOT_TOKEN env var)
- `channel_id` - Optional channel ID (defaults to DISCORD_CHANNEL_ID env var)

**Outputs:**
- `success` - Boolean (true if sent successfully)
- `message` - Status message
- `error` - Error message (if failed)
- `skipped` - Boolean (true if skipped due to missing config)

### `notifications.all`
Send notification to all configured channels (Slack and Discord).

**Inputs:**
- `message` - The message to send to all channels

**Outputs:**
- `success` - Boolean
- `message` - Status message

---

## Logic Plugins

### `logic.and`
Logical AND operation.

**Inputs:**
- `values` - Array of boolean values

**Outputs:**
- `result` - Boolean (all values are true)

### `logic.or`
Logical OR operation.

**Inputs:**
- `values` - Array of boolean values

**Outputs:**
- `result` - Boolean (any value is true)

### `logic.xor`
Logical XOR operation.

**Inputs:**
- `a` - First boolean
- `b` - Second boolean

**Outputs:**
- `result` - Boolean (exactly one is true)

### `logic.equals`
Equality comparison.

**Inputs:**
- `a` - First value
- `b` - Second value

**Outputs:**
- `result` - Boolean (a == b)

### `logic.gt`
Greater than comparison.

**Inputs:**
- `a` - First value
- `b` - Second value

**Outputs:**
- `result` - Boolean (a > b)

### `logic.lt`
Less than comparison.

**Inputs:**
- `a` - First value
- `b` - Second value

**Outputs:**
- `result` - Boolean (a < b)

### `logic.gte`
Greater than or equal comparison.

**Inputs:**
- `a` - First value
- `b` - Second value

**Outputs:**
- `result` - Boolean (a >= b)

### `logic.lte`
Less than or equal comparison.

**Inputs:**
- `a` - First value
- `b` - Second value

**Outputs:**
- `result` - Boolean (a <= b)

### `logic.in`
Membership test.

**Inputs:**
- `value` - Value to find
- `collection` - Array or string

**Outputs:**
- `result` - Boolean (value in collection)

---

## List Plugins

### `list.find`
Find first item matching condition.

**Inputs:**
- `items` - Array of objects
- `key` - Property name
- `value` - Value to match

**Outputs:**
- `result` - Found item or null
- `found` - Boolean

### `list.some`
Check if any item matches.

**Inputs:**
- `items` - Array
- `key` - Optional property name
- `value` - Optional value to match

**Outputs:**
- `result` - Boolean

### `list.every`
Check if all items match.

**Inputs:**
- `items` - Array
- `key` - Optional property name
- `value` - Optional value to match

**Outputs:**
- `result` - Boolean

### `list.concat`
Concatenate multiple lists.

**Inputs:**
- `lists` - Array of arrays

**Outputs:**
- `result` - Concatenated array

### `list.slice`
Extract slice from list.

**Inputs:**
- `items` - Array
- `start` - Start index (default: 0)
- `end` - End index (optional)

**Outputs:**
- `result` - Sliced array

### `list.sort`
Sort list.

**Inputs:**
- `items` - Array
- `key` - Optional sort key
- `reverse` - Boolean (default: false)

**Outputs:**
- `result` - Sorted array

### `list.length`
Get list length.

**Inputs:**
- `items` - Array

**Outputs:**
- `result` - Number (length)

---

## Dictionary Plugins

### `dict.get`
Get value from dictionary.

**Inputs:**
- `object` - Dictionary
- `key` - Key name
- `default` - Default value (optional)

**Outputs:**
- `result` - Value
- `found` - Boolean

### `dict.set`
Set value in dictionary.

**Inputs:**
- `object` - Dictionary
- `key` - Key name
- `value` - Value to set

**Outputs:**
- `result` - Updated dictionary

### `dict.merge`
Merge multiple dictionaries.

**Inputs:**
- `objects` - Array of dictionaries

**Outputs:**
- `result` - Merged dictionary

### `dict.keys`
Get dictionary keys.

**Inputs:**
- `object` - Dictionary

**Outputs:**
- `result` - Array of keys

### `dict.values`
Get dictionary values.

**Inputs:**
- `object` - Dictionary

**Outputs:**
- `result` - Array of values

### `dict.items`
Get dictionary items as [key, value] pairs.

**Inputs:**
- `object` - Dictionary

**Outputs:**
- `result` - Array of [key, value] arrays

---

## String Plugins

### `string.concat`
Concatenate strings.

**Inputs:**
- `strings` - Array of strings
- `separator` - Separator string (default: "")

**Outputs:**
- `result` - Concatenated string

### `string.split`
Split string.

**Inputs:**
- `text` - Input string
- `separator` - Split separator (default: " ")
- `max_splits` - Max splits (optional)

**Outputs:**
- `result` - Array of strings

### `string.replace`
Replace occurrences in string.

**Inputs:**
- `text` - Input string
- `old` - String to replace
- `new` - Replacement string
- `count` - Max replacements (default: -1 for all)

**Outputs:**
- `result` - Modified string

### `string.trim`
Trim whitespace.

**Inputs:**
- `text` - Input string
- `mode` - "both", "start", or "end" (default: "both")

**Outputs:**
- `result` - Trimmed string

### `string.upper`
Convert to uppercase.

**Inputs:**
- `text` - Input string

**Outputs:**
- `result` - Uppercase string

### `string.lower`
Convert to lowercase.

**Inputs:**
- `text` - Input string

**Outputs:**
- `result` - Lowercase string

### `string.format`
Format string with variables.

**Inputs:**
- `template` - Template string with {placeholders}
- `variables` - Dictionary of variables

**Outputs:**
- `result` - Formatted string

### `string.length`
Get string length.

**Inputs:**
- `text` - Input string

**Outputs:**
- `result` - Number (length)

---

## Math Plugins

### `math.add`
Add numbers.

**Inputs:**
- `numbers` - Array of numbers

**Outputs:**
- `result` - Sum

### `math.subtract`
Subtract numbers.

**Inputs:**
- `a` - Minuend
- `b` - Subtrahend

**Outputs:**
- `result` - Difference (a - b)

### `math.multiply`
Multiply numbers.

**Inputs:**
- `numbers` - Array of numbers

**Outputs:**
- `result` - Product

### `math.divide`
Divide numbers.

**Inputs:**
- `a` - Dividend
- `b` - Divisor

**Outputs:**
- `result` - Quotient (a / b)

### `math.modulo`
Modulo operation.

**Inputs:**
- `a` - Dividend
- `b` - Divisor

**Outputs:**
- `result` - Remainder (a % b)

### `math.power`
Power operation.

**Inputs:**
- `a` - Base
- `b` - Exponent

**Outputs:**
- `result` - a^b

### `math.min`
Find minimum value.

**Inputs:**
- `numbers` - Array of numbers

**Outputs:**
- `result` - Minimum value

### `math.max`
Find maximum value.

**Inputs:**
- `numbers` - Array of numbers

**Outputs:**
- `result` - Maximum value

### `math.abs`
Absolute value.

**Inputs:**
- `value` - Number

**Outputs:**
- `result` - |value|

### `math.round`
Round number.

**Inputs:**
- `value` - Number
- `precision` - Decimal places (default: 0)

**Outputs:**
- `result` - Rounded number

---

## Conversion Plugins

### `convert.to_string`
Convert to string.

**Inputs:**
- `value` - Any value

**Outputs:**
- `result` - String

### `convert.to_number`
Convert to number.

**Inputs:**
- `value` - String or number
- `default` - Default value (default: 0)

**Outputs:**
- `result` - Number

### `convert.to_boolean`
Convert to boolean.

**Inputs:**
- `value` - Any value

**Outputs:**
- `result` - Boolean

### `convert.to_list`
Convert to list.

**Inputs:**
- `value` - Any value

**Outputs:**
- `result` - Array

### `convert.to_dict`
Convert to dictionary.

**Inputs:**
- `value` - List of [key, value] pairs or dict

**Outputs:**
- `result` - Dictionary

### `convert.parse_json`
Parse JSON string.

**Inputs:**
- `text` - JSON string

**Outputs:**
- `result` - Parsed object

### `convert.to_json`
Convert to JSON string.

**Inputs:**
- `value` - Any value
- `indent` - Indentation (optional)

**Outputs:**
- `result` - JSON string

---

## Control Flow Plugins

### `control.switch`
Switch/case statement.

**Inputs:**
- `value` - Value to match
- `cases` - Dictionary of case values
- `default` - Default value (optional)

**Outputs:**
- `result` - Matched case value
- `matched` - Boolean

### `utils.branch_condition`
Branch based on condition.

**Inputs:**
- `condition` - Boolean

**Outputs:**
- Routes to output 0 (true) or 1 (false)

---

## Variable Plugins

### `var.get`
Get variable from workflow store.

**Inputs:**
- `key` - Variable name
- `default` - Default value (optional)

**Outputs:**
- `result` - Variable value
- `exists` - Boolean

### `var.set`
Set variable in workflow store.

**Inputs:**
- `key` - Variable name
- `value` - Value to set

**Outputs:**
- `result` - Set value
- `key` - Variable name

### `var.delete`
Delete variable from workflow store.

**Inputs:**
- `key` - Variable name

**Outputs:**
- `result` - Boolean (success)
- `deleted` - Boolean

### `var.exists`
Check if variable exists.

**Inputs:**
- `key` - Variable name

**Outputs:**
- `result` - Boolean

---

## Test Plugins

### `test.assert_equals`
Assert that two values are equal.

**Inputs:**
- `actual` - Actual value
- `expected` - Expected value
- `message` - Optional assertion message

**Outputs:**
- `passed` - Boolean (true if values are equal)
- `expected` - Expected value
- `actual` - Actual value
- `error` - Error message (if failed)

### `test.assert_true`
Assert that a value is true.

**Inputs:**
- `value` - Value to check
- `message` - Optional assertion message

**Outputs:**
- `passed` - Boolean (true if value is true)
- `value` - The checked value
- `error` - Error message (if failed)

### `test.assert_false`
Assert that a value is false.

**Inputs:**
- `value` - Value to check
- `message` - Optional assertion message

**Outputs:**
- `passed` - Boolean (true if value is false)
- `value` - The checked value
- `error` - Error message (if failed)

### `test.assert_exists`
Assert that a value exists (is not None/null).

**Inputs:**
- `value` - Value to check
- `message` - Optional assertion message

**Outputs:**
- `passed` - Boolean (true if value is not None)
- `value` - The checked value
- `error` - Error message (if failed)

### `test.run_suite`
Run a suite of test assertions and aggregate results.

**Inputs:**
- `results` - Array of test result objects (each with 'passed' field)
- `suite_name` - Optional name for the test suite

**Outputs:**
- `passed` - Boolean (true if all tests passed)
- `total` - Total number of tests
- `passed_count` - Number of tests that passed
- `failed_count` - Number of tests that failed
- `failures` - Array of failed test details
- `summary` - Summary string

---

## Backend Plugins

### `backend.create_github`
Initialize GitHub client.

**Outputs:**
- `result` - GitHub client
- `initialized` - Boolean

### `backend.create_openai`
Initialize OpenAI client.

**Outputs:**
- `result` - OpenAI client
- `initialized` - Boolean

### `backend.load_metadata`
Load metadata.json.

**Outputs:**
- `result` - Metadata dictionary

### `backend.load_messages`
Load translation messages.

**Outputs:**
- `result` - Messages dictionary

### `backend.load_tools`
Load tool definitions.

**Outputs:**
- `result` - Tools array

### `backend.load_prompt`
Load prompt.yml.

**Outputs:**
- `result` - Prompt dictionary

### `backend.build_tool_map`
Build tool registry map.

**Outputs:**
- `result` - Tool map dictionary

### `backend.load_plugins`
Load and register plugins.

**Outputs:**
- `result` - Boolean (success)

### `backend.parse_cli_args`
Parse command line arguments.

**Outputs:**
- `dry_run` - Boolean (dry-run mode)
- `yolo` - Boolean (execute without confirmation)
- `once` - Boolean (run single iteration)
- `web` - Boolean (start web UI)

### `backend.load_env`
Load environment variables from .env file.

**Outputs:**
- `result` - String (status message)

### `backend.load_tool_registry`
Load tool registry entries.

**Outputs:**
- `result` - Tool registry array

### `backend.load_tool_policies`
Load tool policies from JSON.

**Outputs:**
- `result` - Tool policies dictionary

---

## Utility Plugins

### `utils.filter_list`
Filter list by condition.

**Inputs:**
- `items` - Array
- `mode` - Filter mode
- `pattern` - Pattern/condition

**Outputs:**
- `result` - Filtered array

### `utils.map_list`
Map/transform list items.

**Inputs:**
- `items` - Array
- `transform` - Transformation

**Outputs:**
- `result` - Transformed array

### `utils.reduce_list`
Reduce list to single value.

**Inputs:**
- `items` - Array
- `separator` - Join separator

**Outputs:**
- `result` - Reduced value

### `utils.not`
Logical NOT operation.

**Inputs:**
- `value` - Boolean value

**Outputs:**
- `result` - Negated boolean

### `utils.check_mvp`
Check if MVP section in ROADMAP.md is completed.

**Outputs:**
- `mvp_reached` - Boolean

### `utils.update_roadmap`
Update ROADMAP.md with new content.

**Inputs:**
- `content` - New roadmap content

**Outputs:**
- `result` - Status message

---

## Variable Binding

All plugins support variable binding using `$variable_name` syntax in inputs. Variables are stored in the workflow runtime store and can be accessed across nodes.

Example:
```json
{
  "parameters": {
    "text": "$user_input",
    "template": "Hello {name}!",
    "variables": {
      "name": "$user_name"
    }
  }
}
```

## Error Handling

Plugins may return an `error` field in their output when an error occurs. Check for this field to handle errors gracefully in your workflow.

Example:
```json
{
  "result": null,
  "error": "Division by zero"
}
```
