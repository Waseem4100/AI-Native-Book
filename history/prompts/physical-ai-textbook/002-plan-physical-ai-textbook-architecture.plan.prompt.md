---
id: 002
title: Plan Physical AI Textbook Architecture
stage: plan
date: 2025-12-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: physical-ai-textbook
branch: 001-physical-ai-textbook
user: system
command: /sp.plan
labels: ["planning", "architecture", "docusaurus", "ros2", "textbook"]
links:
  spec: specs/001-physical-ai-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-physical-ai-textbook/plan.md
  - specs/001-physical-ai-textbook/research.md
  - specs/001-physical-ai-textbook/data-model.md
  - specs/001-physical-ai-textbook/quickstart.md
  - specs/001-physical-ai-textbook/contracts/docusaurus-config.yaml
  - CLAUDE.md (updated with Docusaurus context)
tests:
  - Constitution Check validation (all principles passed)
  - API verification (Phase 0 research complete)
---

## Prompt

# PLANE: High-Level Plan for Building the Textbook
# Title: Physical AI & Humanoid Robotics
# Using Docusaurus + Spec-Kit Plus + Claude Code

MISSION: Create a complete, publish-ready Docusaurus textbook titled "Physical AI & Humanoid Robotics"

HIGH-LEVEL OUTCOME:
- Structured Docusaurus documentation website
- All chapters, modules, examples, illustrations, and exercises
- Capstone project documentation
- ROS 2, Gazebo, Unity, Isaac, and VLA technical content
- GitHub Pages-deployable final book

BOOK BLUEPRINT (TOP LEVEL STRUCTURE):
1. Introduction
2. Module 1: The Robotic Nervous System (ROS 2)
3. Module 2: The Digital Twin (Gazebo & Unity)
4. Module 3: The AI-Robot Brain (NVIDIA Isaac™)
5. Module 4: Vision-Language-Action (VLA)
6. Capstone Project: The Autonomous Humanoid
7. Appendix
8. Glossary
9. Practice Labs

STRATEGIC PLAN:
STEP 1 — Establish the Docusaurus Project
STEP 2 — Generate All Textbook Chapters
STEP 3 — Build Robotics-Focused Content
STEP 4 — Capstone Project
STEP 5 — Create Visuals & Diagrams
STEP 6 — Add Labs & Exercises
STEP 7 — Final Docusaurus Cleanup
STEP 8 — Deployment

SUCCESS CRITERIA:
- Every module has full-length chapters
- Each topic includes examples, code, diagrams, and exercises
- Capstone project includes full implementation plan
- Docusaurus builds successfully
- The site deploys on GitHub Pages
- Students can learn humanoid robotics from zero to advanced

## Response snapshot

Created comprehensive implementation plan for Physical AI & Humanoid Robotics textbook with complete architecture, technical context, and design artifacts.

**Planning Artifacts Created:**

1. **plan.md** (553 lines) - Complete implementation plan with:
   - Technical Context (Docusaurus 3.x, Markdown/MDX, Python 3.10+, Node.js 18+)
   - Constitution Check (all 6 principles validated)
   - Project Structure (docs/ directory with 4 modules, capstone, appendix, glossary)
   - Phase 0: Research & API Verification (8 research tasks)
   - Phase 1: Content Design & Structure (data model, contracts, quickstart)
   - Estimated Effort: 10-14 weeks

2. **research.md** (comprehensive API verification) covering:
   - ROS 2 Humble: rclpy, QoS, URDF, RViz2 (all APIs verified with official docs)
   - Gazebo 11: Physics engines (ODE), joint types, sensor plugins (LiDAR, depth, IMU)
   - Unity Robotics: ROS-TCP-Connector, URDF Importer, URP rendering
   - Isaac Sim & Isaac ROS: USD format, domain randomization, VSLAM, hardware acceleration
   - Nav2: Costmap config, behavior trees, AMCL localization
   - Whisper & LLMs: Voice transcription, task decomposition, action mapping
   - Docusaurus 3.x: Docs-only mode, Mermaid diagrams, code highlighting, GitHub Pages
   - Educational Best Practices: Bloom's taxonomy, exercise design patterns

3. **data-model.md** (comprehensive content entity definitions):
   - 9 entities: Module, Chapter, LearningObjective, CodeExample, Exercise, Solution, Diagram, ComprehensionQuestion, GlossaryEntry
   - Entity relationships and validation rules
   - ER diagram (Mermaid)
   - Estimated metrics: ~25 chapters, ~35 exercises, ~100 code examples, ~120 glossary entries

4. **contracts/docusaurus-config.yaml** (Docusaurus configuration schema):
   - Complete sidebar navigation (4 modules + capstone + appendix + glossary)
   - Front-matter templates (required: title, description, sidebar_position)
   - Code block configuration (Python, Bash, YAML, XML, Mermaid)
   - Quality gates (code execution, link validation, word count, front-matter)
   - Deployment configuration (GitHub Actions, gh-pages)

5. **quickstart.md** (contributor setup guide - 12 sections):
   - Prerequisites (Node.js 18+, Git, ROS 2 Humble optional)
   - Repository setup and local development
   - 5-part pedagogical structure (objectives, explanation, code, exercises, questions)
   - Code example standards (commenting, verification, language tags)
   - Exercise and solution creation
   - Mermaid diagram syntax
   - Quality checks and commit workflow
   - Deployment to GitHub Pages

6. **CLAUDE.md updated** with Docusaurus conventions:
   - Markdown/MDX formatting
   - Front-matter requirements
   - Code example standards
   - Quality gate reminders

**Constitution Check Results:**
- ✅ Principle I (Content Modularity): One chapter = one file, <3000 words
- ✅ Principle II (Technical Accuracy): All APIs verified in research.md
- ✅ Principle III (Docusaurus Standards): Front-matter, Mermaid, code highlighting
- ✅ Principle IV (Pedagogical Structure): 5-part chapter structure mandated
- ✅ Principle V (Version Control Ready): Atomic commits, branching strategy
- ✅ Principle VI (Physical AI Focus): ROS 2, simulation, Isaac, VLA focus

**Project Structure Designed:**
```
docs/
├── intro.md
├── glossary.md
├── module-1-ros2/ (5 chapters + 3 exercises)
├── module-2-simulation/ (5 chapters + 3 exercises)
├── module-3-isaac/ (6 chapters + 3 exercises)
├── module-4-vla/ (5 chapters + 3 exercises)
├── capstone/ (5 documents)
└── appendix/ (3 documents)

solutions/
├── module-1/ to module-4/
└── capstone/
```

**Technical Decisions:**
- Docusaurus 3.x for static site generation (docs-only mode)
- ROS 2 Humble (LTS) for all robotics examples
- Gazebo 11 + Isaac Sim 2023.1+ for simulation
- Mermaid + ASCII art for diagrams (no external images)
- GitHub Actions for automated deployment
- Estimated 60,000-70,000 words total content

**Critical Path:**
Phase 0 (Research) → Phase 1 (Design) → `/sp.tasks` (Task Generation) → Implementation (Chapter Creation)
- Module 1 (ROS 2) must complete before Modules 2-4 (foundational dependency)
- Capstone Project depends on all modules

**Next Steps:**
Ready for `/sp.tasks` to generate actionable task list for textbook implementation following the designed architecture.

## Outcome

- ✅ Impact: Complete implementation plan created with technical context, constitution compliance, project structure, and Phase 0/1 design artifacts. All APIs verified against official documentation (ROS 2, Gazebo, Unity, Isaac, Nav2, Whisper, LLMs, Docusaurus). Data model defines 9 content entities with relationships and validation rules. Docusaurus configuration schema provides complete sidebar structure and quality gates. Contributor quickstart enables new authors to add chapters in <30 minutes. Ready for task generation (`/sp.tasks`).
- 🧪 Tests: Constitution Check passed all 6 principles. API verification completed with official doc links for all frameworks. Data model validation rules defined. Quality gates configured (code execution, link validation, word count, front-matter, API verification).
- 📁 Files: Created `plan.md` (553 lines), `research.md` (comprehensive), `data-model.md` (entity definitions), `quickstart.md` (12-section guide), `contracts/docusaurus-config.yaml` (schema). Updated `CLAUDE.md` with Docusaurus conventions.
- 🔁 Next prompts: Use `/sp.tasks` to generate phase-based task list for textbook implementation. Tasks should be organized by module (1-4), with Module 1 as foundational phase, followed by parallel Module 2-4 implementation. Include Capstone Project tasks after all modules. Use `/sp.implement` to execute tasks once generated.
- 🧠 Reflection: Planning phase successfully bridges specification (what to build) with implementation (how to build). Research.md provides verified API reference for all technical content, satisfying Constitution Principle II (Technical Accuracy). Data model creates shared vocabulary for content entities, enabling consistent chapter creation. Docusaurus configuration schema defines navigation structure upfront, preventing rework. Quickstart guide codifies 5-part pedagogical structure, ensuring constitutional compliance during content creation. Estimated 10-14 week effort aligns with spec SC-009 (maps to university course). Critical path identifies Module 1 (ROS 2) as foundational dependency for Modules 2-4, enabling parallel work after foundation complete.

## Evaluation notes (flywheel)

- Failure modes observed: None - all planning phases completed successfully. Constitution Check initially deferred API verification to Phase 0, then satisfied after research completion.
- Graders run and results (PASS/FAIL): Constitution Check - PASS (all 6 principles + content standards + quality gates). API Verification - PASS (all 8 research tasks completed with official doc links). Data Model - PASS (9 entities defined with relationships and validation rules). Quickstart Guide - PASS (12 sections cover full contributor workflow).
- Prompt variant (if applicable): N/A - standard planning workflow executed
- Next experiment (smallest change to try): During `/sp.tasks` generation, validate that task organization supports parallel module development after foundational phase. Test task breakdown enables independent chapter creation (one contributor can work on Module 2 while another works on Module 3). Ensure exercise tasks include solution creation and rubric development in same phase to maintain 1:1 relationship.
