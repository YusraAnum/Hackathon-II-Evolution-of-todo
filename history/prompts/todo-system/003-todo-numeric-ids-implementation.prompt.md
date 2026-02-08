---
id: 003-todo-numeric-ids-implementation
title: Todo Numeric IDs Implementation
stage: green
date: 2026-01-21
surface: ""
model: opus
feature: todo-system
branch: ""
user: Claude
command: /sp.implement
labels: [implementation, todo-system, phase-1, numeric-ids, python]
links:
  spec: "specs/todo-system/spec.md"
  plan: "specs/todo-system/plan.md"
  tasks: "specs/todo-system/tasks.md"
  ticket: ""
  adr: ""
  pr: ""
files:
  - src/models/todo.py
  - src/lib/storage.py
  - src/services/todo_service.py
  - src/cli.py
  - test_numeric_ids.py
  - test_cli_numeric_ids.py
tests:
  - status: PASS
    name: numeric-ids-test
    result: System now uses auto-increment numeric IDs
    notes: IDs start from 1 and increment correctly
  - status: PASS
    name: cli-numeric-id-handling-test
    result: CLI properly handles numeric ID conversion
    notes: String input converted to int for all operations
  - status: PASS
    name: existing-tests-still-pass
    result: All original functionality preserved
    notes: Comprehensive test suite passes unchanged
---

## Prompt

```
Goal: Replace UUID-based todo IDs with simple auto-increment numeric IDs.

Requirements:
- Remove UUID usage completely
- Each todo should have an integer ID starting from 1
- ID should auto-increment when a new todo is added
- IDs must be unique within the runtime session
- All existing CLI commands (add, list, view, update, delete, mark complete) must work using numeric IDs
- Update storage, model, and any related logic consistently
- Do NOT add persistence (keep in-memory only)
- Do NOT change CLI menu structure or flow

Constraints:
- Minimal code changes
- No new features
- Follow existing spec and tests logic

Output:
- Updated code only
- Ensure all tests pass
```

## Response snapshot

The numeric ID implementation was successfully completed with the following changes:

- Updated storage mechanism (src/lib/storage.py) to use auto-increment integer IDs
- Updated Todo model (src/models/todo.py) to accept integer IDs
- Updated Todo service (src/services/todo_service.py) to work with integer IDs
- Updated CLI (src/cli.py) to properly convert string input to integer IDs
- Created tests to verify numeric ID functionality works correctly
- All existing functionality preserved and tests continue to pass

## Outcome

- ✅ Impact: Replaced UUID-based IDs with auto-increment numeric IDs starting from 1
- 🧪 Tests: All new and existing tests pass
- 📁 Files: Updated models, storage, service, and CLI to use numeric IDs
- 🔁 Next prompts: Phase 1 system enhanced with numeric IDs, ready for evaluation
- 🧠 Reflection: Implementation maintains Phase 1 compliance with minimal changes

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All tests PASSED
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - Enhancement complete