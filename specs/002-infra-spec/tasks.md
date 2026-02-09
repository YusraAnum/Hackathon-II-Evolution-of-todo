---

description: "Task list template for feature implementation"
---

# Tasks: Infrastructure Deployment (Docker, Kubernetes, Helm)

**Input**: Design documents from `/specs/002-infra-spec/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /sp.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 [P] Create infrastructure directory structure per implementation plan
- [X] T002 [P] Set up Docker build environment for frontend and backend
- [X] T003 [P] Verify Minikube and Helm installations

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Create Dockerfile for frontend (Next.js) application
- [X] T005 Create Dockerfile for backend (FastAPI) application
- [ ] T006 [P] Build Docker images: todo-frontend and todo-backend
- [ ] T007 Verify Docker images work locally before Kubernetes deployment
- [ ] T008 Set up Minikube cluster with required resources

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Deploy Application to Kubernetes (Priority: P1) 🎯 MVP

**Goal**: Deploy the Todo application to a Kubernetes cluster with proper replica counts and service exposure

**Independent Test**: The application can be accessed via the configured ingress endpoints and all services are running with the specified replica counts.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Contract test for ingress routing in tests/contract/test_ingress.py
- [ ] T010 [P] [US1] Integration test for deployment verification in tests/integration/test_deployment.py

### Implementation for User Story 1

- [X] T011 [P] [US1] Create backend deployment manifest with 2 replicas in infra/k8s/deployments/backend-deployment.yaml
- [X] T012 [P] [US1] Create frontend deployment manifest with 2 replicas in infra/k8s/deployments/frontend-deployment.yaml
- [X] T013 [US1] Create backend service manifest (ClusterIP) in infra/k8s/services/backend-service.yaml
- [X] T014 [US1] Create frontend service manifest (ClusterIP) in infra/k8s/services/frontend-service.yaml
- [X] T015 [US1] Create ingress manifest routing "/" to frontend and "/api" to backend in infra/k8s/ingress/ingress.yaml
- [ ] T016 [US1] Apply Kubernetes manifests to Minikube cluster
- [ ] T017 [US1] Verify deployments have correct replica counts

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Secure Configuration Management (Priority: P2)

**Goal**: Implement secure management of sensitive configuration values using Kubernetes secrets

**Independent Test**: Sensitive values like DATABASE_URL, OPENAI_API_KEY, and AUTH_SECRET are stored as Kubernetes secrets and accessible only to the appropriate services.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Contract test for secret injection in tests/contract/test_secrets.py
- [ ] T019 [P] [US2] Integration test for secure configuration in tests/integration/test_config.py

### Implementation for User Story 2

- [X] T020 [P] [US2] Create secrets manifest for DATABASE_URL, OPENAI_API_KEY, AUTH_SECRET in infra/k8s/secrets/secrets.yaml
- [X] T021 [US2] Update backend deployment to mount secrets as environment variables
- [X] T022 [US2] Create ConfigMap for API base URL and environment name in infra/k8s/configmaps/configmap.yaml
- [X] T023 [US2] Update frontend deployment to use ConfigMap values
- [ ] T024 [US2] Verify secrets are not exposed in plain text in pod configurations
- [ ] T025 [US2] Verify ConfigMap values are correctly injected

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Health Monitoring (Priority: P3)

**Goal**: Implement health monitoring with liveness and readiness probes

**Independent Test**: The backend service exposes a health endpoint at /api/v1/health and Kubernetes correctly restarts unhealthy pods based on probe results.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T026 [P] [US3] Contract test for health endpoint in tests/contract/test_health.py
- [ ] T027 [P] [US3] Integration test for probe functionality in tests/integration/test_probes.py

### Implementation for User Story 3

- [X] T028 [P] [US3] Update backend deployment with liveness probe for /api/v1/health in infra/k8s/deployments/backend-deployment.yaml
- [X] T029 [US3] Update backend deployment with readiness probe for /api/v1/health in infra/k8s/deployments/backend-deployment.yaml
- [ ] T030 [US3] Verify health endpoint responds correctly
- [ ] T031 [US3] Test Kubernetes automatic pod restart on probe failure

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase 6: Helm Packaging (Priority: P4)

**Goal**: Package all Kubernetes manifests into a Helm chart with configurable values

### Implementation for Helm Packaging

- [X] T032 [P] Create Helm chart structure in infra/helm/todo-app-chart/
- [X] T033 [P] Create Chart.yaml with metadata for todo-app-chart
- [X] T034 [P] Create values.yaml with default configuration
- [X] T035 Create values-dev.yaml for development environment
- [X] T036 Create deployment template in infra/helm/todo-app-chart/templates/deployment.yaml
- [X] T037 Create service template in infra/helm/todo-app-chart/templates/service.yaml
- [X] T038 Create ingress template in infra/helm/todo-app-chart/templates/ingress.yaml
- [X] T039 Create secrets template in infra/helm/todo-app-chart/templates/secrets.yaml
- [X] T040 Create configmap template in infra/helm/todo-app-chart/templates/configmap.yaml
- [ ] T041 Test Helm chart installation with values-dev.yaml
- [ ] T042 Verify all resources are deployed correctly via Helm

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T043 [P] Documentation updates in docs/
- [ ] T044 Code cleanup and refactoring of infrastructure files
- [ ] T045 [P] Additional integration tests (if requested) in tests/integration/
- [ ] T046 Security scan of Docker images
- [ ] T047 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Helm Packaging (Phase 6)**: Depends on all user stories being complete
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for ingress routing in tests/contract/test_ingress.py"
Task: "Integration test for deployment verification in tests/integration/test_deployment.py"

# Launch all models for User Story 1 together:
Task: "Create backend deployment manifest with 2 replicas in infra/k8s/deployments/backend-deployment.yaml"
Task: "Create frontend deployment manifest with 2 replicas in infra/k8s/deployments/frontend-deployment.yaml"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence