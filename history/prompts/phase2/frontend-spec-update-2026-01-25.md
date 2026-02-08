---
id: frontend-spec-update-2026-01-25
title: Frontend Spec Update - Architecture Details
stage: spec
date: 2026-01-25
author: Claude
---

## Prompt

Update the existing Frontend Specification to include the following missing architectural details required by the Project Constitution and Phase 2 constraints.

Do NOT change existing features. Only ADD the sections below.

---

## Authentication Integration

- Authentication must be implemented using the Better Auth client SDK on the frontend.
- Authentication tokens must be stored in HTTP-only cookies (NOT localStorage).
- All API requests from the frontend must include credentials using:
  fetch(..., { credentials: "include" })
- Route protection must be handled using Next.js middleware.
- Unauthenticated users attempting to access protected routes must be redirected to /login.

---

## Environment Configuration

- The backend API base URL must be stored in an environment variable:
  NEXT_PUBLIC_API_URL
- All frontend API calls must use:
  ${process.env.NEXT_PUBLIC_API_URL}/api/v1/...

---

## Data Fetching Strategy

- Todo data fetching must be handled in Client Components.
- Use native fetch() inside useEffect for retrieving todos.
- Create, update, delete, and toggle actions must be performed using client-side API calls.
- No external state management or data-fetching libraries are allowed (no Redux, React Query, SWR, etc.).

---

## Required Folder Structure

The frontend must follow the monorepo structure defined in the constitution:

apps/frontend/
  app/
    login/
    signup/
    dashboard/
  components/
  lib/
    api.ts
    auth.ts
  middleware.ts

No frontend code may be placed outside apps/frontend/.

## Response

Updated the frontend specification file (specs/phase2/frontend_spec.md) by adding the required architectural details without changing existing features:

1. Added Authentication Integration section with Better Auth requirements
2. Added Environment Configuration section with API URL handling
3. Added Data Fetching Strategy section specifying native fetch usage
4. Added Required Folder Structure section defining the monorepo layout

All existing features and functionality remain unchanged.