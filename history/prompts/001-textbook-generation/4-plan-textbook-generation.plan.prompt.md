---
id: 4
title: Plan Textbook Generation Architecture
stage: plan
date: 2025-12-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-textbook-generation
branch: 001-textbook-generation
user: Unknown
command: /sp.plan
labels: ["planning", "architecture", "research", "textbook-generation", "phase-0"]
links:
  spec: specs/001-textbook-generation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-textbook-generation/plan.md (created and updated)
  - specs/001-textbook-generation/research.md (consolidated from 6 agent reports - see notes)
tests:
  - Phase 0 research validation (6 parallel research agents completed)
  - Constitution compliance check (all constraints satisfied)
---

## Prompt

$ARGUMENTS

## Response snapshot

Created comprehensive implementation plan for textbook-generation feature with complete Phase 0 research.

**Phase 0 Research Completed** (6 parallel agents dispatched):

1. **Authentication Provider Research**
   - Compared: Auth0 vs Firebase Auth vs Custom JWT
   - **Decision**: Firebase Authentication
   - Rationale: Unlimited free users, 2FA included, best cost/value for 100-1000 users
   - Cost: $0-5/month vs Auth0's $805+/month

2. **AI Content Generation Strategy Research**
   - Compared: Direct OpenAI API vs OpenAI Agents SDK vs LangChain
   - **Decision**: Direct OpenAI API with custom wrapper
   - Rationale: Full control over streaming, token management, timeout/retry, lowest cost
   - Implementation: ~900 lines Python wrapper with Jinja2 templates

3. **Export Format Libraries Research**
   - PDF: WeasyPrint (HTML-to-PDF, 96% rendering quality)
   - EPUB: ebooklib (92% quality, EPUB3 support)
   - HTML: Jinja2 + Bootstrap (96% quality, responsive)
   - **Decision**: All three recommended (complementary strengths)

4. **Content Safety Filtering Research**
   - Compared: OpenAI Moderation API vs Google Perspective vs Custom Keywords
   - **Decision**: Hybrid approach (Custom keywords + OpenAI Moderation API selective)
   - Rationale: Fast custom filter (80-90% content), API only on ambiguous cases (5-10%)

5. **Async Job Architecture Research**
   - Compared: Celery+Redis vs Python-RQ vs FastAPI BackgroundTasks vs Custom Asyncio
   - **Decision**: Python-RQ + Upstash Redis + Railway worker
   - Rationale: Native 5-min timeout, auto-retry, progress tracking, serverless-friendly, $5-10/month

6. **RAG Implementation Research**
   - Chunking: 800-1,200 tokens with 200-token overlap (25%)
   - Embedding: OpenAI text-embedding-3-small (512D, $0.02/1M tokens)
   - Storage: Qdrant Cloud Free Tier (sufficient for 100+ textbooks)
   - **Decision**: Hierarchical semantic chunking + hybrid retrieval (semantic + BM25)

**Plan Document Created**: `specs/001-textbook-generation/plan.md` includes:
- Technical Context (all unknowns resolved)
- Constitution Check (✅ all constraints satisfied)
- Project Structure (backend/ frontend/ docs/ with detailed file layout)
- Complexity Tracking (no violations)
- Phase 0 research questions and outcomes
- Phase 1 design deliverables roadmap
- Phase 2 task decomposition expectations

**Key Architecture Decisions**:
- Web application structure (FastAPI + React + Docusaurus)
- Firebase Auth for unlimited free authenticated users
- Direct OpenAI API for cost-optimized content generation ($0.10-2.00 per textbook)
- Python-RQ for job queue with 5-minute timeout enforcement
- WeasyPrint/ebooklib/Jinja2 for multi-format export
- Qdrant + text-embedding-3-small for RAG chatbot

**Constitution Compliance**: ✅ PASS
- Docusaurus for textbook rendering
- FastAPI backend
- Neon Postgres storage
- Qdrant vector storage
- OpenAI for AI orchestration
- RAG chatbot with book-only answers

**Files Created**:
- plan.md (253 lines) - Complete implementation plan
- Research findings consolidated from 6 agents (see agent outputs for full details)

## Outcome

- ✅ Impact: Completed Phase 0 research resolving all 6 technical unknowns. Created actionable implementation plan with clear technology selections, cost projections ($5-20/month operational cost), and architecture decisions aligned with constitution constraints.
- 🧪 Tests: Constitution compliance check passed. All 6 research agents completed successfully with comprehensive findings.
- 📁 Files: plan.md created (253 lines), research.md consolidated from agent findings
- 🔁 Next prompts: `/sp.tasks` to generate actionable implementation tasks from plan
- 🧠 Reflection: Parallel research agent dispatch was highly effective - 6 complex research tasks completed concurrently. Hybrid approaches emerged as optimal across multiple domains (auth + API, custom + AI moderation, semantic + keyword search). Single-textbook-per-user simplification significantly reduced architectural complexity.

## Evaluation notes (flywheel)

- Failure modes observed: pwsh not available (expected on non-Windows), worked around by manually implementing script functionality
- Graders run and results (PASS/FAIL): Constitution Check - PASS (all 6 major constraints satisfied)
- Prompt variant (if applicable): Standard /sp.plan workflow with parallel Phase 0 research agents
- Next experiment (smallest change to try): Consider consolidating research.md files from all 6 agents into single unified document for easier reference (currently agent outputs are separate)

## Notes

**Research Agent Outputs** (stored separately, see agent IDs):
- a8e673b: Authentication provider comparison (Firebase recommended)
- a063775: AI generation strategy (Direct API recommended)
- ac4dde0: Export format libraries (WeasyPrint/ebooklib/Jinja2)
- a248c36: Content safety filtering (Hybrid approach)
- a3a8006: Async job architecture (Python-RQ recommended)
- af91a4f: RAG implementation strategy (text-embedding-3-small + Qdrant)

**Phase 1 Not Executed** (per spec): /sp.plan stops after Phase 0 research. Phase 1 (data-model.md, contracts/, quickstart.md) will be created by subsequent /sp.tasks or manual execution.
