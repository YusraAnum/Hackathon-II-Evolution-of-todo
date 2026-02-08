<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 -> 1.1.0 (minor update - adding new principles)
Added sections: Monorepo Structure Rule, Technology Stack Lock, No Assumptions Rule
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
Removed sections: None
Follow-up TODOs: None
-->
# Hackathon II — The Evolution of Todo App Constitution

## Core Principles

### Strict Adherence to Spec-Driven Development (SDD)
Phase 1 must follow the exact sequence: Constitution → Specification → Plan → Tasks → Implementation. No deviations or skipping of phases are permitted. All work must be traceable through this sequence.

### Phase Isolation and Scope Control
Phase 1 must not include or anticipate features intended for future phases. The system must remain focused solely on in-memory Todo functionality without planning for persistence, UI, or authentication. Simplicity and clarity over extensibility.

### Deterministic and Reproducible Behavior
All functionality must behave predictably and consistently. The in-memory Todo system must have deterministic outcomes for all operations. All behavior must be traceable from specification to implementation.

### In-Memory Only Architecture
The Todo management system must operate solely in memory with no persistence beyond runtime. No databases, file-based storage, or external persistence mechanisms are allowed. State exists only during program execution.

### Minimal Backend-Only Functionality
Phase 1 is strictly backend/logic-only with no UI, web frameworks, APIs, or external services. The system implements core Todo CRUD operations (Create, Read, List, Update, Delete) without user interfaces or network exposure.

### No Future-Phase Features
No authentication, authorization, databases, file persistence, web frameworks, UI components, or scalability optimizations are allowed in Phase 1. All such features are explicitly forbidden until future phases.

### Monorepo Structure Rule
The project MUST follow this folder structure for Phase 2 and beyond:

root/
  apps/
    backend/
    frontend/
  specs/

Claude is not allowed to place backend or frontend code outside the apps/ directory.

### Technology Stack Lock
Claude must use only the following technologies for Phase 2:

Backend:
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic

Frontend:
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS

Authentication:
- Better Auth

Claude may NOT replace these technologies with alternatives.

### No Assumptions Rule
Claude must NOT add extra features, tools, libraries, or architecture decisions that are not explicitly defined in the specs.

If something is unclear, Claude must STOP and ask instead of assuming.

## Process Rules
- No code may be written without approved tasks
- No tasks without a plan
- No plan without a specification
- All artifacts must align strictly with this constitution
- If ambiguity exists, the agent must STOP and ask

## Technology and Tooling Constraints
- Claude Code
- Spec-Kit Plus
- MCP Server
- No manual coding outside the defined workflow
- No external libraries beyond core language features
- No web frameworks or server implementations (for Phase 1)
- For Phase 2+: FastAPI, PostgreSQL, SQLAlchemy, Alembic, Next.js 14, TypeScript, Tailwind CSS, Better Auth only

## Governance

All development must strictly comply with these principles. Any deviation requires explicit amendment to this constitution following the established SDD process. Code reviews must verify compliance with Phase 1 scope limitations. The constitution serves as the governing authority superseding all other practices during Phase 1 development.

**Version**: 1.1.0 | **Ratified**: 2026-01-21 | **Last Amended**: 2026-01-25