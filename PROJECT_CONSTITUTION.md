# Project Constitution

## 1. Development Method
This project follows STRICT Spec-Driven Development.

That means:
- NO feature may be implemented without an approved spec file
- Code must ONLY be written based on an existing spec
- If a spec does not exist, Claude must STOP and ask for it

## 2. Folder Safety Rules
Claude is NOT allowed to:
- Create new top-level folders without permission
- Move existing folders unless explicitly instructed
- Delete any existing project files

## 3. Implementation Rules
Claude must NEVER:
- Run servers
- Create Docker files
- Install dependencies
- Generate test files
UNLESS the user explicitly asks

## 4. Phase Rules
This project has multiple phases.

Claude must ONLY work on the CURRENT phase defined by the user.

Current Phase: PLANNING PHASE FOR PHASE 2

## 5. Approval Rule
After generating specs, Claude must WAIT for approval before writing any code.