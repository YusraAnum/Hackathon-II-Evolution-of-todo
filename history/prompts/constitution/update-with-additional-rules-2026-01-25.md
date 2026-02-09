---
id: constitution-update-2026-01-25
title: Update Constitution with Additional Rules
stage: constitution
date: 2026-01-25
author: Claude
---

## Prompt

Update the Project Constitution with the following additional rules:

## 6. Monorepo Structure Rule
The project MUST follow this folder structure for Phase 2 and beyond:

root/
  apps/
    backend/
    frontend/
  specs/

Claude is not allowed to place backend or frontend code outside the apps/ directory.

## 7. Technology Stack Lock
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

## 8. No Assumptions Rule
Claude must NOT add extra features, tools, libraries, or architecture decisions that are not explicitly defined in the specs.

If something is unclear, Claude must STOP and ask instead of assuming.

## Response

Updated the constitution by adding three new principles: Monorepo Structure Rule, Technology Stack Lock, and No Assumptions Rule. The version was incremented from 1.0.0 to 1.1.0 to reflect these additions. The updated constitution maintains all existing principles while incorporating the new rules about monorepo structure, technology stack constraints, and assumption avoidance.