# AGENTS.md

## Project Rulebook
This project follows STRICT Spec-Driven Development (SDD).
All AI agents must operate only within the rules defined here.

## Mandatory Workflow
All work MUST follow this exact order:
1. Constitution
2. Specification
3. Plan
4. Tasks
5. Implementation

Breaking this order is not allowed.

## Hard Rules (Non-Negotiable)
- No code may be written without approved tasks
- No tasks may be created without a plan
- No plan may be created without a specification
- Agents must not jump to another phase on their own
- If anything is unclear, the agent must STOP and ask
- Agents must not add assumptions or extra features

## Agent Behavior
- Agents must follow only the rules of the current phase
- Repository files are the single source of truth
- Output should be minimal and step-by-step unless asked otherwise

## Tooling
- Claude Code
- Spec-Kit Plus
- MCP Server
- No manual coding allowed

## Current Phase
Phase I — In-Memory Todo System