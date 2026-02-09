<!-- SYNC IMPACT REPORT:
Version change: 1.1.0 -> 1.2.0 (minor update - adding new principles for Phase 4)
Added sections: Infrastructure-Only Constraint, Containerization Mandate, Orchestration Requirement, Configuration Management Policy
Removed sections: In-Memory Only Architecture, Minimal Backend-Only Functionality, No Future-Phase Features (Phase 1 specific)
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
Removed sections: In-Memory Only Architecture, Minimal Backend-Only Functionality, No Future-Phase Features (Phase 1 specific)
Follow-up TODOs: None
-->
# Hackathon II — The Evolution of Todo App Constitution

## Core Principles

### Strict Adherence to Spec-Driven Development (SDD)
All phases must follow the exact sequence: Constitution → Specification → Plan → Tasks → Implementation. No deviations or skipping of phases are permitted. All work must be traceable through this sequence.

### Phase Isolation and Scope Control
Each phase must not include or anticipate features intended for other phases. Current work must remain focused solely on infrastructure and deployment concerns without altering business logic. Simplicity and clarity over feature development.

### Deterministic and Reproducible Behavior
All infrastructure and deployment configurations must behave predictably and consistently. Deployments must have deterministic outcomes for all operations. All behavior must be traceable from specification to implementation.

### Infrastructure-Only Constraint
Phase 4 work must focus exclusively on infrastructure and deployment. No new application features are permitted. No business logic changes are allowed. Existing Phase 3 frontend and backend must be used as-is without modifications.

### Containerization Mandate
Docker must be used for containerization of all application components. All services must be packaged in containers following industry best practices. Images must be optimized for size and security.

### Orchestration Requirement
Kubernetes (Minikube) must be used for orchestration. All deployment configurations must be compatible with Kubernetes environments. Helm must be used to manage Kubernetes manifests for consistent deployments.

### Configuration Management Policy
Secrets must NOT be hardcoded in any configuration files. Environment variables must be injected at runtime through secure mechanisms. No sensitive information should be stored in plain text in the repository.

### Local Deployment Focus
Deployment targets must be limited to local Kubernetes (Minikube) only. No cloud deployment is permitted in Phase 4. All configurations must be validated in local Minikube environment.

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
- For Phase 4: Docker, Kubernetes (Minikube), Helm only for infrastructure/deployment
- No changes to existing application codebase

## Governance

All development must strictly comply with these principles. Any deviation requires explicit amendment to this constitution following the established SDD process. Code reviews must verify compliance with Phase 4 scope limitations. The constitution serves as the governing authority superseding all other practices during Phase 4 development.

**Version**: 1.2.0 | **Ratified**: 2026-01-21 | **Last Amended**: 2026-02-09