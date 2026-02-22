---
description: "Implementation tasks for textbook generation feature"
---

# Tasks: Textbook Generation System

**Input**: Design documents from `/specs/001-textbook-generation/`
**Prerequisites**: plan.md (tech stack, structure), spec.md (5 user stories P1-P5)

**Tests**: Not requested in specification - test tasks omitted

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Per plan.md, this is a **web application** with:
- Backend: `backend/src/`
- Frontend: `frontend/src/`
- Docs: `docs/` (Docusaurus generated textbook output)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure per plan.md

- [x] T001 Create backend project structure with directories: backend/src/{models,schemas,services,api,core}, backend/tests/{unit,integration,e2e}, backend/alembic
- [x] T002 Create frontend project structure with directories: frontend/src/{components,pages,services,hooks,contexts,types}, frontend/tests/{unit,integration}
- [x] T003 Create shared types directory: shared/types/ for TypeScript definitions
- [x] T004 Create docs directory for Docusaurus: docs/docs/, docs/src/components/RAGChatbot/
- [x] T005 Initialize Python backend with FastAPI dependencies in backend/requirements.txt (FastAPI, SQLAlchemy, Alembic, python-rq, firebase-admin, openai, tiktoken, weasyprint, ebooklib, jinja2, qdrant-client)
- [x] T006 [P] Initialize React frontend with TypeScript in frontend/package.json (React 18, TypeScript, React Router, Firebase Auth SDK)
- [x] T007 [P] Initialize Docusaurus site in docs/package.json
- [x] T008 [P] Configure linting and formatting: backend/.flake8, backend/pyproject.toml (black, isort), frontend/.eslintrc, frontend/.prettierrc
- [x] T009 [P] Create environment configuration template: backend/.env.example (DATABASE_URL, REDIS_URL, OPENAI_API_KEY, FIREBASE_CREDENTIALS, QDRANT_URL, QDRANT_API_KEY)
- [x] T010 Setup Git hooks for pre-commit formatting checks in .git/hooks/pre-commit

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & Configuration

- [x] T011 Setup Neon Serverless Postgres connection in backend/src/core/database.py (SQLAlchemy engine, session management)
- [x] T012 Create Alembic migration configuration in backend/alembic/env.py
- [x] T013 Configure application settings in backend/src/core/config.py (Pydantic BaseSettings for environment variables)

### Authentication Foundation

- [x] T014 Setup Firebase Admin SDK initialization in backend/src/core/security.py
- [x] T015 Implement JWT verification middleware for Firebase tokens in backend/src/core/security.py (verify_firebase_token function)
- [x] T016 Create authentication dependencies for FastAPI routes in backend/src/core/security.py (get_current_user dependency)

### Base Models

- [x] T017 [P] Create User model in backend/src/models/user.py (id, firebase_uid, email, created_at, updated_at)
- [x] T018 [P] Create Textbook model in backend/src/models/textbook.py (id, user_id, title, subject, level, created_at, updated_at)
- [x] T019 [P] Create Chapter model in backend/src/models/chapter.py (id, textbook_id, chapter_number, title, objectives, content, created_at)
- [x] T020 [P] Create Section model in backend/src/models/section.py (id, chapter_id, section_number, title, content, subsections)
- [x] T021 [P] Create Exercise model in backend/src/models/exercise.py (id, chapter_id, question, difficulty, solution, explanation)
- [x] T022 [P] Create GenerationJob model in backend/src/models/generation_job.py (id, user_id, chapter_id, status, progress, tokens_used, error_message, started_at, completed_at)

### Database Migrations

- [x] T023 Create initial database migration for all models in backend/alembic/versions/001_initial_schema.py
- [x] T024 Run migration to create tables in Neon Postgres database

### API Infrastructure

- [x] T025 Create FastAPI app instance with CORS middleware in backend/src/main.py
- [x] T026 Setup API router registration in backend/src/main.py (auth, textbooks, chapters, generation, export)
- [x] T027 Implement global exception handlers in backend/src/core/exceptions.py
- [x] T028 Create standardized error response schemas in backend/src/schemas/errors.py

### Frontend Foundation

- [x] T029 Setup Firebase Auth in frontend with React context in frontend/src/contexts/AuthContext.tsx
- [x] T030 Create API client base service in frontend/src/services/api.ts (axios with auth interceptors)
- [x] T031 Create protected route wrapper component in frontend/src/components/auth/ProtectedRoute.tsx
- [x] T032 Implement login page UI in frontend/src/pages/LoginPage.tsx

### External Services Setup

- [x] T033 Setup Upstash Redis connection in backend/src/core/redis.py (Python-RQ queue initialization)
- [x] T034 Setup Qdrant client connection in backend/src/core/rag.py (QdrantClient initialization)
- [x] T035 Initialize OpenAI client in backend/src/core/ai.py (AsyncOpenAI with tiktoken)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Generate Basic Textbook Structure (Priority: P1) 🎯 MVP

**Goal**: Allow educators to create a complete textbook outline with chapters and sections for a specific subject and educational level

**Independent Test**: Provide subject ("Introduction to Python Programming") and level ("High School"), verify complete chapter-based outline generated with appropriate section headings

### Backend Services

- [x] T036 [US1] Create Pydantic schemas for textbook generation in backend/src/schemas/textbook.py (TextbookCreate, TextbookResponse, ChapterOutline)
- [x] T037 [US1] Implement TextbookGenerator class in backend/src/services/generation.py (generate_outline method with OpenAI API, streaming support, timeout handling)
- [x] T038 [US1] Create prompt templates for outline generation in backend/src/services/prompts/ (outline.jinja2 with subject/level parameters)
- [x] T039 [US1] Implement TextbookService CRUD operations in backend/src/services/textbook.py (create, get_by_user, update_structure)
- [x] T040 [US1] Add keyword filtering service in backend/src/services/moderation.py (basic blocklist, whitelist for educational terms)

### Backend API Endpoints

- [x] T041 [US1] Implement POST /api/v1/textbooks/generate-outline endpoint in backend/src/api/generation.py (accepts subject, level, num_chapters)
- [x] T042 [US1] Implement GET /api/v1/textbooks/me endpoint in backend/src/api/textbooks.py (get current user's textbook)
- [x] T043 [US1] Implement PUT /api/v1/textbooks/{id}/structure endpoint in backend/src/api/textbooks.py (update chapter structure)

### Frontend Components

- [ ] T044 [P] [US1] Create GenerationForm component in frontend/src/components/generation/GenerationForm.tsx (subject, level, num_chapters inputs)
- [ ] T045 [P] [US1] Create TextbookOutline component in frontend/src/components/textbook/TextbookOutline.tsx (displays chapter tree structure)
- [ ] T046 [P] [US1] Create generation API service in frontend/src/services/generation.ts (API calls for outline generation)

### Frontend Pages

- [ ] T047 [US1] Implement DashboardPage in frontend/src/pages/DashboardPage.tsx (shows generation form, current textbook outline)
- [ ] T048 [US1] Add routing for dashboard in frontend/src/App.tsx

### Integration

- [ ] T049 [US1] Integrate GenerationForm with API backend in DashboardPage
- [ ] T050 [US1] Add loading states and error handling for outline generation
- [ ] T051 [US1] Implement textbook outline display with expand/collapse functionality

**Checkpoint**: At this point, User Story 1 should be fully functional - educators can generate and view textbook outlines

---

## Phase 4: User Story 2 - Generate Chapter Content (Priority: P2)

**Goal**: Allow educators to populate chapters with detailed educational content including explanations, examples, and learning objectives

**Independent Test**: Select a chapter from existing structure, verify comprehensive educational content is generated with explanations, examples, and learning objectives

### Backend Services

- [ ] T052 [US2] Extend TextbookGenerator class in backend/src/services/generation.py (add generate_chapter_content method with streaming)
- [ ] T053 [US2] Create chapter content prompt templates in backend/src/services/prompts/ (chapter_content.jinja2, learning_objectives.jinja2)
- [ ] T054 [US2] Implement Python-RQ job queueing in backend/src/services/job_queue.py (enqueue_generation_job, get_job_status, retry_logic)
- [ ] T055 [US2] Create ChapterService in backend/src/services/chapter.py (CRUD operations, content management)

### Backend API Endpoints

- [ ] T056 [US2] Implement POST /api/v1/chapters/{id}/generate-content endpoint in backend/src/api/generation.py (queues generation job, returns job_id)
- [ ] T057 [US2] Implement GET /api/v1/jobs/{job_id}/status endpoint in backend/src/api/generation.py (polls Python-RQ job status)
- [ ] T058 [US2] Implement WebSocket endpoint /api/v1/ws/generation/{job_id} in backend/src/api/generation.py (streams chapter content generation progress)
- [ ] T059 [US2] Implement GET /api/v1/chapters/{id} endpoint in backend/src/api/chapters.py (retrieve chapter with generated content)

### Worker Process

- [ ] T060 [US2] Create RQ worker script in backend/src/worker.py (listens to generation queue, executes jobs with timeout)
- [ ] T061 [US2] Implement graceful timeout handling with exponential backoff retry in backend/src/services/generation.py

### Frontend Components

- [ ] T062 [P] [US2] Create GenerationProgress component in frontend/src/components/generation/GenerationProgress.tsx (WebSocket listener, progress bar, status updates)
- [ ] T063 [P] [US2] Create ChapterView component in frontend/src/components/textbook/ChapterView.tsx (displays generated content, learning objectives)
- [ ] T064 [P] [US2] Create chapter API service in frontend/src/services/textbook.ts (generate content, poll status, fetch chapter)

### Frontend Pages

- [ ] T065 [US2] Implement EditorPage in frontend/src/pages/EditorPage.tsx (chapter list, content viewer, generation trigger)
- [ ] T066 [US2] Add routing for editor page in frontend/src/App.tsx

### Integration

- [ ] T067 [US2] Connect GenerationProgress to WebSocket in EditorPage
- [ ] T068 [US2] Implement chapter content generation workflow (trigger → poll → display)
- [ ] T069 [US2] Add error handling for timeouts and failed generation jobs

**Checkpoint**: At this point, User Story 2 should be fully functional - educators can generate detailed chapter content with streaming progress

---

## Phase 5: User Story 3 - Add Practice Exercises and Assessments (Priority: P3)

**Goal**: Allow educators to include practice problems, exercises, and assessment questions at the end of each chapter

**Independent Test**: Request exercise generation for an existing chapter, verify appropriate questions/problems/solutions are created matching chapter content and difficulty

### Backend Services

- [ ] T070 [US3] Extend TextbookGenerator class in backend/src/services/generation.py (add generate_exercises method)
- [ ] T071 [US3] Create exercise generation prompt templates in backend/src/services/prompts/ (exercises.jinja2 with difficulty levels)
- [ ] T072 [US3] Implement ExerciseService in backend/src/services/exercise.py (CRUD operations, difficulty classification)

### Backend API Endpoints

- [ ] T073 [US3] Implement POST /api/v1/chapters/{id}/generate-exercises endpoint in backend/src/api/generation.py (queues exercise generation job)
- [ ] T074 [US3] Implement GET /api/v1/chapters/{id}/exercises endpoint in backend/src/api/chapters.py (retrieve all exercises for chapter)
- [ ] T075 [US3] Implement PUT /api/v1/exercises/{id} endpoint in backend/src/api/chapters.py (update exercise content)

### Frontend Components

- [ ] T076 [P] [US3] Create ExerciseList component in frontend/src/components/textbook/ExerciseList.tsx (displays exercises grouped by difficulty)
- [ ] T077 [P] [US3] Create ExerciseGenerationButton component in frontend/src/components/generation/ExerciseGenerationButton.tsx (triggers exercise generation for chapter)

### Integration

- [ ] T078 [US3] Add exercise generation to EditorPage chapter view
- [ ] T079 [US3] Integrate exercise display in ChapterView component
- [ ] T080 [US3] Add exercise generation progress tracking (reuse GenerationProgress component)

**Checkpoint**: At this point, User Story 3 should be fully functional - educators can generate practice exercises for chapters

---

## Phase 6: User Story 4 - Customize and Edit Generated Content (Priority: P4)

**Goal**: Allow educators to review, edit, and customize generated textbook content to match their teaching style

**Independent Test**: Modify generated content (chapter text, structure, exercises), verify changes are saved and reflected in subsequent views

### Backend API Endpoints

- [ ] T081 [US4] Implement PUT /api/v1/textbooks/{id}/metadata endpoint in backend/src/api/textbooks.py (update title, subject, level)
- [ ] T082 [US4] Implement PUT /api/v1/chapters/{id}/content endpoint in backend/src/api/chapters.py (update chapter content, objectives)
- [ ] T083 [US4] Implement POST /api/v1/chapters/{id}/reorder endpoint in backend/src/api/chapters.py (change chapter ordering)
- [ ] T084 [US4] Implement PUT /api/v1/sections/{id} endpoint in backend/src/api/chapters.py (update section content)

### Backend Services

- [ ] T085 [US4] Add content update validation in backend/src/services/chapter.py (ensure content integrity, update timestamps)
- [ ] T086 [US4] Implement chapter reordering logic in backend/src/services/textbook.py (update chapter_number fields)

### Frontend Components

- [ ] T087 [P] [US4] Create RichTextEditor component in frontend/src/components/textbook/RichTextEditor.tsx (markdown editor with preview)
- [ ] T088 [P] [US4] Create ChapterReorder component in frontend/src/components/textbook/ChapterReorder.tsx (drag-and-drop chapter ordering)
- [ ] T089 [P] [US4] Create SectionEditor component in frontend/src/components/textbook/SectionEditor.tsx (inline section editing)
- [ ] T090 [P] [US4] Create ExerciseEditor component in frontend/src/components/textbook/ExerciseEditor.tsx (edit exercise questions/solutions)

### Integration

- [ ] T091 [US4] Add edit mode toggle to ChapterView component
- [ ] T092 [US4] Implement auto-save functionality for content edits (debounced PUT requests)
- [ ] T093 [US4] Add undo/redo functionality for edit history (local state management)
- [ ] T094 [US4] Implement chapter reordering in TextbookOutline component

**Checkpoint**: At this point, User Story 4 should be fully functional - educators can edit and customize all generated content

---

## Phase 7: User Story 5 - Export Textbook in Multiple Formats (Priority: P5)

**Goal**: Allow educators to export completed textbooks in PDF, EPUB, and HTML formats for distribution

**Independent Test**: Select complete textbook, export to each format, verify exported files contain all content with proper formatting

### Backend Services

- [ ] T095 [US5] Implement PDF export service in backend/src/services/export.py (WeasyPrint integration, HTML-to-PDF conversion)
- [ ] T096 [US5] Implement EPUB export service in backend/src/services/export.py (ebooklib integration, EPUB3 generation)
- [ ] T097 [US5] Implement HTML export service in backend/src/services/export.py (Jinja2 static site generation)
- [ ] T098 [US5] Create export Jinja2 templates in backend/src/services/templates/export/ (pdf.html, chapter.xhtml, toc.html)
- [ ] T099 [US5] Implement Docusaurus export in backend/src/services/export.py (generate Markdown files + sidebars.js)

### Backend API Endpoints

- [ ] T100 [US5] Implement POST /api/v1/textbooks/{id}/export endpoint in backend/src/api/export.py (accepts format parameter: pdf|epub|html, queues export job)
- [ ] T101 [US5] Implement GET /api/v1/exports/{job_id}/download endpoint in backend/src/api/export.py (streams generated file for download)
- [ ] T102 [US5] Implement GET /api/v1/exports/{job_id}/status endpoint in backend/src/api/export.py (checks export job status)

### Frontend Components

- [ ] T103 [P] [US5] Create ExportDialog component in frontend/src/components/export/ExportDialog.tsx (format selection, download button)
- [ ] T104 [P] [US5] Create FormatSelector component in frontend/src/components/export/FormatSelector.tsx (PDF/EPUB/HTML radio buttons with descriptions)
- [ ] T105 [P] [US5] Create ExportProgress component in frontend/src/components/export/ExportProgress.tsx (shows export generation status)

### Frontend Pages

- [ ] T106 [US5] Implement ExportPage in frontend/src/pages/ExportPage.tsx (textbook preview, export options, download controls)
- [ ] T107 [US5] Add routing for export page in frontend/src/App.tsx

### Integration

- [ ] T108 [US5] Connect ExportDialog to export API endpoints
- [ ] T109 [US5] Implement file download handling (browser download trigger)
- [ ] T110 [US5] Add export validation (file size checks, format verification)

**Checkpoint**: At this point, User Story 5 should be fully functional - educators can export textbooks in all formats

---

## Phase 8: RAG Chatbot Integration (Cross-Cutting)

**Purpose**: Implement constitution-mandated RAG chatbot for generated textbook content

**Dependencies**: Requires User Story 2 (chapter content) to have content to query

### Backend RAG Services

- [ ] T111 [P] Implement chunking service in backend/src/services/rag_chunking.py (hierarchical semantic splitter, 800-1200 token chunks, 200 token overlap)
- [ ] T112 [P] Implement embedding service in backend/src/services/rag_embedding.py (OpenAI text-embedding-3-small integration)
- [ ] T113 Create Qdrant collection initialization in backend/src/core/rag.py (create collection with 512D vectors, cosine distance)
- [ ] T114 Implement content ingestion pipeline in backend/src/services/rag_ingestion.py (chunk chapters, embed, upsert to Qdrant)
- [ ] T115 Implement RAG query service in backend/src/services/rag_query.py (semantic search, metadata filtering, confidence scoring)
- [ ] T116 Create grounded prompt builder in backend/src/services/rag_prompts.py (builds LLM prompts with retrieved chunks, hallucination prevention)

### Backend API Endpoints

- [ ] T117 Implement POST /api/v1/chat endpoint in backend/src/api/rag.py (accepts question, returns answer with sources)
- [ ] T118 Implement POST /api/v1/chat/selected-text endpoint in backend/src/api/rag.py (accepts selected text + question, scoped query)
- [ ] T119 Implement POST /api/v1/textbooks/{id}/ingest endpoint in backend/src/api/rag.py (triggers chapter ingestion to Qdrant)

### Frontend Components

- [ ] T120 [P] Create RAGChatbot component in docs/src/components/RAGChatbot/ChatWidget.tsx (chat interface, message display)
- [ ] T121 [P] Create ChatMessage component in docs/src/components/RAGChatbot/ChatMessage.tsx (individual message with source citations)
- [ ] T122 [P] Create SelectedTextQuery component in docs/src/components/RAGChatbot/SelectedTextQuery.tsx (handles text selection + query)

### Integration

- [ ] T123 Integrate RAG chatbot into Docusaurus site in docs/docusaurus.config.js (global component)
- [ ] T124 Implement text selection handler for selected-text queries
- [ ] T125 Add automatic content ingestion trigger after chapter generation completion

**Checkpoint**: RAG chatbot operational - can answer questions from generated textbook content

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Performance & Optimization

- [ ] T126 [P] Implement token usage tracking per user in backend/src/services/analytics.py (budget enforcement)
- [ ] T127 [P] Add database indexing for common queries in Alembic migration (user_id, textbook_id, chapter_number)
- [ ] T128 [P] Implement API response caching for static endpoints (textbook structure) in backend/src/core/cache.py

### Security & Validation

- [ ] T129 [P] Implement rate limiting middleware in backend/src/core/rate_limit.py (generation requests per user per hour)
- [ ] T130 [P] Add input validation for all user inputs in backend/src/schemas/ (subject length limits, chapter count limits)
- [ ] T131 [P] Implement CSRF protection for state-changing endpoints in backend/src/core/security.py

### Error Handling & Logging

- [ ] T132 [P] Setup structured logging with correlation IDs in backend/src/core/logging.py (request tracing)
- [ ] T133 [P] Add error logging for failed generation jobs in backend/src/services/generation.py
- [ ] T134 [P] Implement user-friendly error messages in frontend/src/services/errors.ts (map API errors to readable messages)

### Documentation & Developer Experience

- [ ] T135 [P] Create API documentation with OpenAPI spec in backend/openapi.json (auto-generated from FastAPI)
- [ ] T136 [P] Write developer setup guide in specs/001-textbook-generation/quickstart.md (environment setup, local development, testing)
- [ ] T137 [P] Add inline code comments for complex generation logic in backend/src/services/generation.py

### Deployment

- [ ] T138 Create Vercel deployment configuration in vercel.json (backend API routes, frontend build settings)
- [ ] T139 Create Railway deployment configuration for RQ worker in backend/railway.json
- [ ] T140 Setup environment variables in Vercel dashboard (DATABASE_URL, REDIS_URL, OPENAI_API_KEY, etc.)
- [ ] T141 Create deployment documentation in specs/001-textbook-generation/deployment.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion - No dependencies on other stories
- **User Story 2 (Phase 4)**: Depends on Foundational completion - Integrates with US1 (needs textbook structure) but independently testable
- **User Story 3 (Phase 5)**: Depends on Foundational completion + US2 (needs chapter content) - Independently testable
- **User Story 4 (Phase 6)**: Depends on Foundational completion + US1/US2/US3 (needs content to edit) - Independently testable
- **User Story 5 (Phase 7)**: Depends on Foundational completion + US1/US2 (needs content to export) - Independently testable
- **RAG Chatbot (Phase 8)**: Depends on US2 (needs chapter content to query) - Cross-cutting feature
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

```
Foundation (Phase 2) - BLOCKS EVERYTHING
    ↓
    ├── US1 (P1): Generate Structure - Independent
    ├── US2 (P2): Generate Content - Needs US1 structure
    ├── US3 (P3): Generate Exercises - Needs US2 content
    ├── US4 (P4): Edit Content - Needs US1/US2/US3 content
    └── US5 (P5): Export Formats - Needs US1/US2 content

RAG (Phase 8): Needs US2 content
```

### Within Each User Story

- Backend services before API endpoints
- API endpoints before frontend services
- Frontend components before page integration
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

**Setup Phase (Phase 1)**: Tasks T005, T006, T007, T008, T009 can run in parallel

**Foundational Phase (Phase 2)**:
- Models T017-T022 can all run in parallel
- Frontend foundation T029-T032 can run in parallel with backend work

**User Story 1 (Phase 3)**:
- Components T044, T045, T046 can run in parallel after backend is complete

**User Story 2 (Phase 4)**:
- Components T062, T063, T064 can run in parallel after backend is complete

**User Story 3 (Phase 5)**:
- Components T076, T077 can run in parallel after backend is complete

**RAG Phase (Phase 8)**:
- Services T111, T112 can run in parallel
- Components T120, T121, T122 can run in parallel

**Polish Phase (Phase 9)**:
- All tasks marked [P] (T126-T137) can run in parallel

**Cross-Story Parallelization**:
Once Foundation (Phase 2) is complete, different teams can work on different user stories simultaneously:
- Team A: User Story 1 (T036-T051)
- Team B: User Story 2 (T052-T069)
- Team C: User Story 5 (T095-T110)

---

## Parallel Example: User Story 1

```bash
# After Backend Services complete, launch all frontend components together:
Task T044: "Create GenerationForm component in frontend/src/components/generation/GenerationForm.tsx"
Task T045: "Create TextbookOutline component in frontend/src/components/textbook/TextbookOutline.tsx"
Task T046: "Create generation API service in frontend/src/services/generation.ts"
```

---

## Parallel Example: Foundation Phase

```bash
# Launch all model creation tasks together:
Task T017: "Create User model in backend/src/models/user.py"
Task T018: "Create Textbook model in backend/src/models/textbook.py"
Task T019: "Create Chapter model in backend/src/models/chapter.py"
Task T020: "Create Section model in backend/src/models/section.py"
Task T021: "Create Exercise model in backend/src/models/exercise.py"
Task T022: "Create GenerationJob model in backend/src/models/generation_job.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T010)
2. Complete Phase 2: Foundational (T011-T035) - CRITICAL
3. Complete Phase 3: User Story 1 (T036-T051)
4. **STOP and VALIDATE**: Test outline generation independently
5. Deploy/demo if ready

**Estimated Effort**: 2-3 weeks for MVP (outline generation only)

### Incremental Delivery

1. **Foundation** (Phases 1-2): Setup + Foundational → T001-T035 → ~1-2 weeks
2. **MVP** (Phase 3): User Story 1 → T036-T051 → ~1 week → **Deploy & Demo**
3. **Content Generation** (Phase 4): User Story 2 → T052-T069 → ~2 weeks → **Deploy & Demo**
4. **Exercises** (Phase 5): User Story 3 → T070-T080 → ~1 week → **Deploy & Demo**
5. **Editing** (Phase 6): User Story 4 → T081-T094 → ~1-2 weeks → **Deploy & Demo**
6. **Export** (Phase 7): User Story 5 → T095-T110 → ~2 weeks → **Deploy & Demo**
7. **RAG** (Phase 8): RAG Chatbot → T111-T125 → ~2 weeks → **Deploy & Demo**
8. **Polish** (Phase 9): Cross-cutting concerns → T126-T141 → ~1 week → **Final Release**

**Total Estimated Effort**: 10-14 weeks for complete feature

### Parallel Team Strategy

With 3 developers after Foundation complete:

1. **Week 1-2**: All work on Foundation together (T001-T035)
2. **Week 3**:
   - Dev A: User Story 1 (T036-T051) - MVP
   - Dev B: User Story 2 backend (T052-T061)
   - Dev C: User Story 5 backend (T095-T099)
3. **Week 4-5**:
   - Dev A: User Story 2 frontend (T062-T069)
   - Dev B: User Story 3 (T070-T080)
   - Dev C: User Story 5 frontend (T100-T110)
4. **Week 6-7**:
   - Dev A: User Story 4 (T081-T094)
   - Dev B: RAG backend (T111-T119)
   - Dev C: RAG frontend (T120-T125)
5. **Week 8**: All work on Polish (T126-T141) in parallel

**Accelerated Timeline**: 8 weeks with 3 developers vs 14 weeks solo

---

## Task Summary

**Total Tasks**: 141 tasks
**Parallelizable Tasks**: 42 tasks marked [P]

**Tasks per User Story**:
- Setup (Phase 1): 10 tasks
- Foundational (Phase 2): 25 tasks
- User Story 1 (P1): 16 tasks
- User Story 2 (P2): 18 tasks
- User Story 3 (P3): 11 tasks
- User Story 4 (P4): 14 tasks
- User Story 5 (P5): 16 tasks
- RAG Chatbot (Phase 8): 15 tasks
- Polish (Phase 9): 16 tasks

**MVP Scope (Recommended)**: Phases 1-3 only (T001-T051 = 51 tasks, ~3-4 weeks)
- Delivers User Story 1: Educators can generate and view textbook outlines
- Provides immediate value and validates technical approach
- Foundation for all subsequent stories

**Parallel Opportunities**: 42 tasks can execute concurrently within their phases

**Independent Test Criteria Met**: Each user story has clear acceptance tests and can be validated independently

---

## Notes

- All tasks follow strict checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
- Tasks organized by user story for independent implementation and testing
- Each phase checkpoint validates story works independently
- [P] tasks target different files with no dependencies - safe for concurrent execution
- Backend structure follows plan.md web application layout (backend/, frontend/, docs/)
- Constitution-mandated technologies integrated (FastAPI, Neon, Qdrant, Firebase, OpenAI, Docusaurus)
- Single-textbook-per-user constraint simplifies data model and reduces task complexity
- Export and RAG features support constitution requirements for AI-native textbook platform
