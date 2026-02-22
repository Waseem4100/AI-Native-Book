# Implementation Plan: Textbook Generation System

**Branch**: `001-textbook-generation` | **Date**: 2025-12-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-textbook-generation/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an AI-powered educational textbook generation system that allows authenticated educators to create a single comprehensive textbook project. The system will generate structured educational content including table of contents, chapter content, learning objectives, examples, and practice exercises. Content is generated using AI with basic keyword filtering for safety, stored server-side with user authentication, and exportable to PDF, EPUB, and HTML formats. The system enforces a single-textbook-per-user model for focused user experience, with indefinite retention and 5-minute per-chapter generation timeouts.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript/React 18 (frontend)
**Primary Dependencies**: FastAPI (backend API), React 18, Docusaurus (frontend framework per constitution), OpenAI SDK (AI generation), Firebase Authentication (unlimited free tier with 2FA)
**Storage**: Neon Serverless Postgres (relational data per constitution), Qdrant Cloud Free Tier (vector storage for RAG per constitution), Upstash Redis (Python-RQ job queue)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (browser-based, deployed on Vercel or GitHub Pages per constitution)
**Project Type**: Web application (frontend + backend)
**Performance Goals**:
- Chapter outline generation: <2 minutes for 10-15 chapters
- Chapter content generation: <3 minutes per chapter
- API response time: <200ms for CRUD operations
- Support 50 concurrent users without degradation

**Constraints**:
- Single textbook per user (simplified data model)
- 5-minute timeout per chapter generation with automatic retry
- Basic keyword filtering for content safety
- Must integrate with constitution-mandated tech stack (FastAPI, Neon Postgres, Qdrant, OpenAI)

**Scale/Scope**:
- Initial: 100 users
- Textbook size: 8-20 chapters typical, up to 50 chapters maximum
- Content per chapter: ~5-10 sections, 3-10 exercises
- Export file sizes: PDF <50MB per textbook

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Platform Constraints ✅
- ✅ **Docusaurus**: System will use Docusaurus for the generated textbook content rendering (constitution requirement)
- ✅ **GitHub Pages/Vercel**: Deployment target satisfied
- ✅ **Public GitHub repository**: Satisfied

### AI-Native Constraints ✅
- ✅ **RAG chatbot mandatory**: Will be implemented to answer questions about generated textbook content
- ✅ **Answer only from book content**: RAG system will be scoped to generated textbook
- ✅ **Support user-selected text**: Will implement selection-based context passing

### Engineering Constraints ✅
- ✅ **Backend MUST use FastAPI**: Satisfied (specified in Technical Context)
- ✅ **Vector storage MUST use Qdrant Cloud (Free Tier)**: Satisfied for RAG embeddings
- ✅ **Relational storage MUST use Neon Serverless Postgres**: Satisfied for user data, textbook structure
- ✅ **AI orchestration MUST use OpenAI Agents / ChatKit SDKs**: Will use OpenAI API for content generation

### Pedagogical Philosophy ⚠️ DEFERRED
- The textbook generation system itself doesn't need to follow the progressive embodied intelligence model
- This philosophy applies to the *content of the generated Physical AI textbook*, not the generation tool
- Generator will support customizable chapter structures to enable this philosophy in generated content

### Quality Standards ✅
- ✅ Reusable intelligence via subagents supported
- ✅ Quality gates through educator review requirement (FR-014)

**GATE RESULT**: ✅ PASS - All applicable constitution constraints satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-textbook-generation/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── auth-api.yaml
│   ├── textbook-api.yaml
│   └── generation-api.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/          # SQLAlchemy models (User, Textbook, Chapter, Section, Exercise)
│   ├── schemas/         # Pydantic schemas for API validation
│   ├── services/        # Business logic
│   │   ├── auth.py      # Authentication service
│   │   ├── generation.py # AI content generation service
│   │   ├── textbook.py  # Textbook CRUD operations
│   │   └── export.py    # PDF/EPUB/HTML export service
│   ├── api/             # FastAPI routes
│   │   ├── auth.py      # Authentication endpoints
│   │   ├── textbooks.py # Textbook CRUD endpoints
│   │   ├── chapters.py  # Chapter endpoints
│   │   ├── generation.py # Generation job endpoints
│   │   └── export.py    # Export endpoints
│   ├── core/            # Configuration, database, dependencies
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── rag.py       # Qdrant vector store integration
│   └── main.py          # FastAPI app entry point
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── alembic/             # Database migrations
└── requirements.txt

frontend/
├── src/
│   ├── components/      # Reusable React components
│   │   ├── auth/        # Login, Register, Profile
│   │   ├── textbook/    # TextbookEditor, ChapterList, SectionEditor
│   │   ├── generation/  # GenerationProgress, GenerationForm
│   │   └── export/      # ExportDialog, FormatSelector
│   ├── pages/           # Page-level components
│   │   ├── DashboardPage.tsx
│   │   ├── EditorPage.tsx
│   │   ├── LoginPage.tsx
│   │   └── ExportPage.tsx
│   ├── services/        # API client services
│   │   ├── api.ts       # Base API client
│   │   ├── auth.ts      # Authentication API calls
│   │   ├── textbook.ts  # Textbook API calls
│   │   └── generation.ts # Generation API calls
│   ├── hooks/           # Custom React hooks
│   ├── contexts/        # React contexts (AuthContext, TextbookContext)
│   ├── types/           # TypeScript type definitions
│   └── App.tsx
├── tests/
│   ├── unit/
│   └── integration/
├── package.json
└── tsconfig.json

shared/                  # Shared types between frontend and backend
├── types/
│   ├── user.ts
│   ├── textbook.ts
│   └── generation.ts
└── constants/

docs/                    # Docusaurus site (generated textbook output)
├── docs/               # Generated textbook chapters
├── src/
│   └── components/
│       └── RAGChatbot/  # Embedded RAG chatbot for generated content
├── docusaurus.config.js
└── package.json
```

**Structure Decision**: Selected **Web application** structure (Option 2 from template) because the feature requires both a user-facing frontend for textbook creation/editing and a backend API for data persistence, AI generation, and export processing. The `docs/` directory houses the Docusaurus-powered generated textbook output as mandated by the constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations - all constitution constraints satisfied.*

## Phase 0: Research & Technology Decisions

### Research Questions

The following areas require research and decision-making:

1. **Authentication Provider Selection**
   - Decision needed: Auth0 vs Firebase Auth vs custom JWT
   - Factors: Cost (free tier), ease of integration, security features
   - Constitution constraint: Must support user isolation and data protection

2. **AI Content Generation Strategy**
   - Decision needed: Direct OpenAI API vs OpenAI Agents SDK vs LangChain
   - Factors: Streaming support, retry logic, token management, cost
   - Requirement: Must generate educational content with examples and exercises

3. **Export Format Implementation**
   - Decision needed: Library selection for PDF (ReportLab/WeasyPrint), EPUB (ebooklib), HTML (Jinja2)
   - Factors: Formatting quality, Table of Contents generation, cross-platform compatibility
   - Requirement: 95% rendering quality (SC-006)

4. **Content Safety & Keyword Filtering**
   - Decision needed: Custom filter vs third-party API (OpenAI Moderation, Perspective API)
   - Factors: Accuracy, latency, cost
   - Requirement: Basic keyword filtering per FR-014

5. **Generation Job Management**
   - Decision needed: Celery vs FastAPI BackgroundTasks vs separate worker process
   - Factors: Timeout handling, retry logic, progress tracking
   - Requirement: 5-minute timeout with automatic retry per FR-015

6. **RAG Implementation for Generated Content**
   - Decision needed: Chunking strategy, embedding model, query optimization
   - Factors: Retrieval accuracy, response latency
   - Constitution requirement: Must answer questions only from generated book content

### Research Tasks

These will be investigated in Phase 0 and documented in `research.md`:

- **Task 1**: Compare Auth0 vs Firebase Auth for educator authentication (free tier, React/FastAPI SDKs)
- **Task 2**: Evaluate OpenAI API approaches for educational content generation (streaming, prompt engineering)
- **Task 3**: Test PDF/EPUB/HTML generation libraries for quality and formatting (ReportLab, WeasyPrint, ebooklib)
- **Task 4**: Research content moderation approaches (OpenAI Moderation API, custom keyword lists)
- **Task 5**: Design async job architecture for 5-minute generation timeout requirement
- **Task 6**: Define RAG chunking and embedding strategy for Qdrant integration

## Phase 1: Design Artifacts

### Deliverables

1. **data-model.md**: Entity-relationship model for User, Textbook, Chapter, Section, Exercise, GenerationJob
2. **contracts/**: OpenAPI specifications for all REST API endpoints
   - auth-api.yaml: Authentication endpoints (login, register, logout, profile)
   - textbook-api.yaml: Textbook CRUD operations
   - generation-api.yaml: Content generation and job status endpoints
   - export-api.yaml: Export format generation endpoints
3. **quickstart.md**: Developer setup guide for local development

### Key Design Decisions (to be made in Phase 1)

- Database schema with proper indexing for single-textbook-per-user queries
- API endpoint naming conventions and versioning strategy
- WebSocket vs Server-Sent Events for generation progress streaming
- Qdrant collection schema for generated textbook embeddings
- Error response format standardization across API

## Phase 2: Task Decomposition

*This phase is executed by the `/sp.tasks` command (NOT /sp.plan). Tasks will be generated based on Phase 1 design artifacts.*

Expected task categories:
- Backend API implementation (auth, CRUD, generation, export)
- Frontend UI implementation (editor, progress tracking, export dialog)
- RAG chatbot integration with Qdrant
- Database migrations and seed data
- Testing (unit, integration, E2E)
- Deployment configuration (Vercel, environment variables)

## Notes

- The textbook generation system is a **meta-tool** that creates the Physical AI & Humanoid Robotics textbook specified in the constitution
- Single-textbook-per-user simplification significantly reduces complexity (no project selection UI, simpler data model)
- Constitution mandates specific tech stack (FastAPI, Neon Postgres, Qdrant, OpenAI) which aligns well with feature requirements
- Phase 0 research critical for AI generation quality and export format reliability
- RAG chatbot for generated content ensures AI-native learning experience per constitution
