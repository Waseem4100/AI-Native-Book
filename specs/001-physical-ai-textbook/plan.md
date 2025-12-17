# Implementation Plan: Physical AI & Humanoid Robotics Textbook

**Branch**: `001-physical-ai-textbook` | **Date**: 2025-12-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-physical-ai-textbook/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create a complete, publish-ready Docusaurus textbook titled "Physical AI & Humanoid Robotics" that teaches students how to design, simulate, and deploy AI-powered humanoid robots. The textbook consists of 4 modules (ROS 2, Simulation, Isaac, VLA), a Capstone Project, and supporting materials (glossary, exercises, solutions). Each chapter follows a 5-part pedagogical structure (learning objectives, explanation, code examples, exercises, comprehension questions) and must be independently testable. All code examples must execute without errors in ROS 2 Humble + Gazebo 11 or Isaac Sim environments.

**Technical Approach**: Use Docusaurus 3.x static site generator to create modular, version-controlled educational content. Each module maps to a Docusaurus docs subdirectory with index page, chapter files, and exercises. Content follows Constitution principles for modularity (one chapter = one file, <3000 words), technical accuracy (all APIs verified), and pedagogical structure (5 mandatory components per chapter).

## Technical Context

**Language/Version**: Markdown (.md/.mdx) for textbook content; Python 3.10+ for all code examples; Node.js 18+ for Docusaurus
**Primary Dependencies**: Docusaurus 3.x (static site generator), React 18+ (Docusaurus UI), Prism (syntax highlighting), Mermaid (diagrams)
**Storage**: Filesystem (Git repository) - no database required. Content stored as markdown files in `/docs/` directory.
**Testing**: Manual verification of code examples in target environments (ROS 2 Humble, Gazebo 11, Isaac Sim 2023.1+); Docusaurus build validation (`npm run build`); Link checker for cross-references
**Target Platform**: Static website deployed to GitHub Pages (or equivalent hosting). Students access via web browser. Code examples run locally on student machines (Ubuntu 22.04 recommended).
**Project Type**: Documentation site (Docusaurus) - uses docs-only mode with sidebar navigation
**Performance Goals**: Docusaurus build completes in <5 minutes; site loads in <3 seconds on standard broadband; search results return in <500ms
**Constraints**:
- All code must execute in ROS 2 Humble + Gazebo 11 or Isaac Sim without modification (per spec FR-003)
- Chapters cannot exceed 3000 words without subdivision (Constitution Principle I)
- No external image files - diagrams must be Mermaid or ASCII art (per spec FR-009)
- All APIs must be verified against official documentation (Constitution Principle II)
- Content must be GitHub Pages compatible (no server-side processing)
**Scale/Scope**:
- 4 modules with ~20-25 total chapters (estimated 5-7 chapters per module)
- 1 Capstone Project document
- ~30-40 exercises across all modules
- ~20-30 code examples per module (80-120 total)
- Glossary with ~100-150 robotics terms
- Target audience: ~1000s of students (static site scales infinitely)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Content Modularity
- ✅ **PASS**: One chapter = one file design
- ✅ **PASS**: Chapters limited to <3000 words (to be enforced during writing)
- ✅ **PASS**: Self-contained chapters with explicit cross-references
- ✅ **PASS**: Module structure supports non-linear learning paths

### Principle II: Technical Accuracy (NON-NEGOTIABLE)
- ⚠️ **DEFER TO PHASE 0**: All ROS 2 APIs, Isaac features, Gazebo physics must be researched and verified against official documentation
- ✅ **PASS**: Specification requires verification of all code examples (FR-003, FR-008)
- ⚠️ **ACTION REQUIRED**: Create verification checklist for each API/framework used

### Principle III: Docusaurus Standards
- ✅ **PASS**: Docusaurus 3.x selected as platform
- ✅ **PASS**: Front-matter required for all content files (FR-004)
- ✅ **PASS**: Mermaid and ASCII art for diagrams (FR-009)
- ✅ **PASS**: GitHub Pages deployment specified

### Principle IV: Pedagogical Structure
- ✅ **PASS**: 5-part chapter structure mandated (FR-002)
- ✅ **PASS**: Learning objectives, exercises, and comprehension questions required
- ✅ **PASS**: Progressive difficulty (foundational to advanced)
- ✅ **PASS**: Real-world robotics applications anchor concepts

### Principle V: Version Control Ready
- ✅ **PASS**: One chapter = one file design
- ✅ **PASS**: Atomic commits per pedagogical unit specified
- ✅ **PASS**: Git repository structure defined
- ✅ **PASS**: Branching strategy documented in Constitution

### Principle VI: Physical AI Focus
- ✅ **PASS**: All modules focus on ROS 2, simulation, Isaac, and VLA
- ✅ **PASS**: Humanoid robotics use cases throughout
- ✅ **PASS**: Simulation-to-real transfer addressed (FR-014)
- ✅ **PASS**: Generic AI/ML content excluded unless robot-control applicable

### Content Standards
- ✅ **PASS**: Code Quality - PEP 8, rclpy best practices, commented URDF (per Constitution)
- ⚠️ **DEFER TO PHASE 0**: Simulation Fidelity - Must research physics engine parameters, RTX settings
- ✅ **PASS**: Exercise Design - Time estimates (15min/1hr/3hrs), progressive difficulty (FR-013)
- ✅ **PASS**: Terminology Consistency - Glossary required (FR-016)

### Quality Gates
- ✅ **PASS**: Code execution validation required before merge
- ✅ **PASS**: Learning objective mapping to comprehension questions
- ✅ **PASS**: No verification placeholders in final content
- ✅ **PASS**: Front-matter completeness checks
- ✅ **PASS**: Cross-reference path validation

### Overall Constitution Compliance
**Status**: ✅ **CONDITIONALLY PASSED** - Proceed to Phase 0 research with actions:
1. Research and document all ROS 2 APIs, Isaac features, Gazebo parameters to satisfy Principle II
2. Create API verification checklist template
3. Research simulation fidelity parameters (physics engines, RTX settings, sensor noise models)

No complexity violations identified. All content requirements align with Constitution principles.

## Project Structure

### Documentation (this feature)

```text
specs/001-physical-ai-textbook/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (already exists)
├── research.md          # Phase 0 output - API verification, best practices
├── data-model.md        # Phase 1 output - Content entities (Module, Chapter, Exercise, etc.)
├── quickstart.md        # Phase 1 output - Docusaurus setup guide for contributors
├── contracts/           # Phase 1 output - Docusaurus config schemas
│   └── docusaurus-config.yaml  # Sidebar structure, navigation schema
├── checklists/
│   └── requirements.md  # Quality validation checklist (already exists)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
docs/
├── intro.md                    # Homepage - textbook overview, prerequisites
├── glossary.md                 # Robotics terminology reference
├── module-1-ros2/
│   ├── index.md                # Module 1 overview + learning path
│   ├── ch1-middleware.md       # ROS 2 fundamentals
│   ├── ch2-nodes-topics.md     # Communication patterns
│   ├── ch3-services-actions.md # Advanced ROS 2 interactions
│   ├── ch4-rclpy-control.md    # Python humanoid joint control
│   ├── ch5-urdf-modeling.md    # Humanoid robot modeling
│   └── exercises/
│       ├── ex1-first-node.md
│       ├── ex2-publisher-subscriber.md
│       └── ex3-urdf-humanoid.md
├── module-2-simulation/
│   ├── index.md
│   ├── ch1-digital-twin.md     # What is a Digital Twin?
│   ├── ch2-gazebo-physics.md   # Physics engine deep dive
│   ├── ch3-unity-interaction.md # Unity for HRI
│   ├── ch4-sensor-simulation.md # LiDAR, depth, RGB, IMU
│   ├── ch5-complete-simulation.md # Building full humanoid sim
│   └── exercises/
│       ├── ex1-gazebo-world.md
│       ├── ex2-sensor-setup.md
│       └── ex3-unity-scene.md
├── module-3-isaac/
│   ├── index.md
│   ├── ch1-intro-isaac.md      # NVIDIA Isaac overview
│   ├── ch2-isaac-sim.md        # Photorealistic training data
│   ├── ch3-isaac-ros.md        # Perception stack
│   ├── ch4-vslam.md            # Visual SLAM + depth
│   ├── ch5-nav2.md             # Path planning for humanoids
│   ├── ch6-ai-brain.md         # AI-controlled humanoid brain
│   └── exercises/
│       ├── ex1-isaac-setup.md
│       ├── ex2-vslam-demo.md
│       └── ex3-nav2-humanoid.md
├── module-4-vla/
│   ├── index.md
│   ├── ch1-vla-intro.md        # VLA: Future of robotics
│   ├── ch2-whisper.md          # Voice commands
│   ├── ch3-llm-ros2.md         # LLM → ROS 2 translation
│   ├── ch4-cognitive-planning.md # Task decomposition
│   ├── ch5-integration.md      # Vision + Language + Action
│   └── exercises/
│       ├── ex1-whisper-setup.md
│       ├── ex2-llm-actions.md
│       └── ex3-full-pipeline.md
├── capstone/
│   ├── project-overview.md     # "The Autonomous Humanoid Assistant"
│   ├── architecture.md         # System design diagrams
│   ├── implementation.md       # Step-by-step guide
│   ├── evaluation.md           # Rubric and testing
│   └── optional-hardware.md    # Sim-to-real deployment
└── appendix/
    ├── prerequisites.md        # Linux, Python, ROS 2 setup
    ├── troubleshooting.md      # Common errors
    └── resources.md            # External learning materials

solutions/
├── module-1/
│   ├── ex1-first-node.py
│   ├── ex2-publisher-subscriber.py
│   └── ex3-urdf-humanoid.urdf
├── module-2/
│   └── ...
├── module-3/
│   └── ...
├── module-4/
│   └── ...
└── capstone/
    └── full-solution/          # Complete Capstone implementation

docusaurus.config.js            # Docusaurus configuration
sidebars.js                     # Sidebar navigation structure
package.json                    # Node dependencies (Docusaurus 3.x)
README.md                       # Contributor setup guide
```

**Structure Decision**: Docusaurus documentation site structure selected because:
1. **Educational content focus**: Docs-only mode perfect for textbook format
2. **Modular organization**: Each module maps to a subdirectory with clear hierarchy
3. **Version control friendly**: One chapter = one markdown file enables clean diffs
4. **GitHub Pages deployment**: Native support for static site hosting
5. **Search and navigation**: Built-in search, sidebar, and breadcrumbs enhance learning
6. **Constitution alignment**: Structure directly maps to Constitution's mandatory module layout

Solutions stored separately in `/solutions/` (not under `/docs/`) to prevent accidental exposure to students before they complete exercises.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations - Constitution Check passed. No complexity justification required.

## Phase 0: Research & API Verification

**Purpose**: Resolve all technical unknowns and verify APIs against official documentation to satisfy Constitution Principle II (Technical Accuracy).

### Research Tasks

1. **ROS 2 Humble API Verification**
   - Research: rclpy API for node creation, publishers, subscribers, services, actions
   - Research: QoS profiles and lifecycle node patterns
   - Research: URDF/SDF syntax for humanoid joints and sensors
   - Research: RViz2 visualization tools
   - **Output**: Document verified APIs with official doc links

2. **Gazebo 11 Physics Parameters**
   - Research: Physics engine options (ODE, Bullet, Simbody)
   - Research: Time step configuration and real-time factors
   - Research: Joint types (revolute, prismatic, fixed) and control plugins
   - Research: Sensor plugins (ray, depth camera, IMU, camera)
   - **Output**: Document physics parameters with examples

3. **Unity Robotics Integration**
   - Research: Unity Robotics Hub and ROS-TCP-Connector
   - Research: URDF Importer for Unity
   - Research: Rendering pipelines (URP/HDRP) for HRI visualization
   - Research: Sensor noise models in Unity
   - **Output**: Document Unity-ROS 2 integration patterns

4. **NVIDIA Isaac Sim & Isaac ROS**
   - Research: Isaac Sim 2023.1+ installation and RTX requirements
   - Research: USD format for robot models
   - Research: Domain randomization parameters
   - Research: Isaac ROS GEMs (hardware-accelerated perception nodes)
   - Research: Isaac ROS VSLAM and visual odometry
   - **Output**: Document Isaac setup and accelerated pipelines

5. **Navigation2 (Nav2) Configuration**
   - Research: Nav2 behavior trees for humanoid locomotion
   - Research: Costmap configuration for bipedal robots
   - Research: AMCL (localization) and path planning algorithms
   - Research: Nav2 recovery behaviors
   - **Output**: Document Nav2 configuration for humanoids

6. **Whisper & LLM Integration**
   - Research: OpenAI Whisper API for voice transcription
   - Research: LLM APIs (GPT-4, Claude, or open-source alternatives)
   - Research: Prompt engineering for task decomposition
   - Research: LLM → ROS 2 action mapping patterns
   - **Output**: Document voice-to-action pipeline architecture

7. **Docusaurus 3.x Best Practices**
   - Research: Docs-only mode configuration
   - Research: Sidebar structure and versioning
   - Research: Mermaid diagram integration
   - Research: Code block syntax highlighting (Python, YAML, XML)
   - Research: GitHub Pages deployment workflow
   - **Output**: Document Docusaurus setup and conventions

8. **Educational Content Best Practices**
   - Research: Learning objective taxonomies (Bloom's)
   - Research: Exercise design patterns (guided → open-ended)
   - Research: Comprehension question strategies
   - Research: Code example commenting for beginners
   - **Output**: Document pedagogical patterns

### Research Consolidation

All findings will be consolidated in `research.md` with format:
- **Decision**: [Technology/pattern chosen]
- **Rationale**: [Why chosen for educational context]
- **Alternatives Considered**: [Other options evaluated]
- **Verification**: [Link to official documentation]
- **Example**: [Minimal code snippet demonstrating verified API]

**Acceptance Criteria for Phase 0**:
- [ ] All 8 research tasks completed
- [ ] Every API documented with official source link
- [ ] Example code snippets execute without errors
- [ ] `research.md` has zero `[NEEDS CLARIFICATION]` markers
- [ ] Constitution Principle II (Technical Accuracy) fully satisfied

## Phase 1: Content Design & Structure

**Prerequisites**: `research.md` complete with all APIs verified

### 1. Data Model (`data-model.md`)

Define content entities and relationships:

**Entities**:
- **Module**: Major learning unit (ROS 2, Simulation, Isaac, VLA)
  - Attributes: title, number, learning outcomes, prerequisites, estimated duration
  - Contains: multiple Chapters, Exercises subdirectory, index page
- **Chapter**: Self-contained learning unit within a module
  - Attributes: title, sidebar_position, word count, learning objectives, prerequisites
  - Contains: 5 required sections (objectives, explanation, code, exercises, questions)
  - Constraints: <3000 words, one file, no forward references without explicit cross-ref
- **Code Example**: Executable code snippet
  - Attributes: language, filename, line count, verified (bool), environment (ROS 2/Gazebo/Isaac)
  - Contains: code block, explanatory comments, expected output
  - Constraints: Must execute without errors, include language tag for syntax highlighting
- **Exercise**: Hands-on learning activity
  - Attributes: title, time estimate (15min/1hr/3hrs), difficulty (guided/intermediate/open-ended)
  - Contains: instructions, expected outcomes, hints
  - Relationships: has Solution (in `/solutions/`)
- **Solution**: Reference implementation for an Exercise
  - Attributes: filename, language, includes_rubric (bool)
  - Constraints: Stored separately from exercise, not visible in main textbook
- **Diagram**: Visual representation
  - Attributes: type (Mermaid/ASCII), caption, referenced_in (chapter IDs)
  - Constraints: No external images, must render in markdown
- **Comprehension Question**: Assessment item
  - Attributes: question text, type (multiple choice/short answer), answer key
  - Relationships: maps to Learning Objective
- **Learning Objective**: Measurable outcome for a chapter
  - Attributes: objective text, Bloom's taxonomy level, assessment method
  - Relationships: assessed by Comprehension Questions
- **Glossary Entry**: Robotics term definition
  - Attributes: term, definition, related terms, first introduced (chapter ID)
  - Constraints: Consistent terminology per Constitution standards

**Relationships**:
- Module (1) → (many) Chapters
- Module (1) → (many) Exercises
- Chapter (1) → (many) Code Examples
- Chapter (1) → (many) Learning Objectives
- Chapter (1) → (many) Comprehension Questions
- Exercise (1) → (1) Solution
- Learning Objective (1) → (many) Comprehension Questions
- Glossary Entry (many) ← (many) Chapters (cross-references)

**Validation Rules**:
- Chapter word count validated on commit (automated check)
- Code examples marked `verified: true` only after manual execution test
- Exercise time estimates sum to match module duration estimates
- All cross-references validated before merge (broken link check)

### 2. Docusaurus Configuration Schema (`contracts/docusaurus-config.yaml`)

Define sidebar structure and navigation:

```yaml
# Sidebar navigation schema for Physical AI Textbook
sidebar:
  - type: doc
    id: intro
    label: "Introduction"

  - type: category
    label: "Module 1: ROS 2 Foundations"
    collapsed: false
    items:
      - module-1-ros2/index
      - module-1-ros2/ch1-middleware
      - module-1-ros2/ch2-nodes-topics
      - module-1-ros2/ch3-services-actions
      - module-1-ros2/ch4-rclpy-control
      - module-1-ros2/ch5-urdf-modeling
      - type: category
        label: "Exercises"
        items:
          - module-1-ros2/exercises/ex1-first-node
          - module-1-ros2/exercises/ex2-publisher-subscriber
          - module-1-ros2/exercises/ex3-urdf-humanoid

  - type: category
    label: "Module 2: Simulation"
    collapsed: true
    items:
      - module-2-simulation/index
      - module-2-simulation/ch1-digital-twin
      - module-2-simulation/ch2-gazebo-physics
      - module-2-simulation/ch3-unity-interaction
      - module-2-simulation/ch4-sensor-simulation
      - module-2-simulation/ch5-complete-simulation
      - type: category
        label: "Exercises"
        items:
          - module-2-simulation/exercises/ex1-gazebo-world
          - module-2-simulation/exercises/ex2-sensor-setup
          - module-2-simulation/exercises/ex3-unity-scene

  - type: category
    label: "Module 3: Isaac AI Brain"
    collapsed: true
    items:
      - module-3-isaac/index
      - module-3-isaac/ch1-intro-isaac
      - module-3-isaac/ch2-isaac-sim
      - module-3-isaac/ch3-isaac-ros
      - module-3-isaac/ch4-vslam
      - module-3-isaac/ch5-nav2
      - module-3-isaac/ch6-ai-brain
      - type: category
        label: "Exercises"
        items:
          - module-3-isaac/exercises/ex1-isaac-setup
          - module-3-isaac/exercises/ex2-vslam-demo
          - module-3-isaac/exercises/ex3-nav2-humanoid

  - type: category
    label: "Module 4: Vision-Language-Action"
    collapsed: true
    items:
      - module-4-vla/index
      - module-4-vla/ch1-vla-intro
      - module-4-vla/ch2-whisper
      - module-4-vla/ch3-llm-ros2
      - module-4-vla/ch4-cognitive-planning
      - module-4-vla/ch5-integration
      - type: category
        label: "Exercises"
        items:
          - module-4-vla/exercises/ex1-whisper-setup
          - module-4-vla/exercises/ex2-llm-actions
          - module-4-vla/exercises/ex3-full-pipeline

  - type: category
    label: "Capstone Project"
    collapsed: true
    items:
      - capstone/project-overview
      - capstone/architecture
      - capstone/implementation
      - capstone/evaluation
      - capstone/optional-hardware

  - type: category
    label: "Appendix"
    collapsed: true
    items:
      - appendix/prerequisites
      - appendix/troubleshooting
      - appendix/resources

  - type: doc
    id: glossary
    label: "Glossary"

# Front-matter template for chapters
chapter_frontmatter:
  required_fields:
    - title: string
    - description: string (max 160 chars for SEO)
    - sidebar_position: integer
  optional_fields:
    - tags: array[string]
    - keywords: array[string]
    - sidebar_label: string (override for sidebar)

# Quality gate checks
quality_gates:
  - code_execution_test: true
  - link_validation: true
  - word_count_check: true (max 3000 per chapter)
  - front_matter_validation: true
  - api_verification_check: true
```

### 3. Contributor Quickstart Guide (`quickstart.md`)

Step-by-step guide for educators/contributors to set up development environment:

**Sections**:
1. Prerequisites (Node.js 18+, Git, code editor)
2. Repository setup (`git clone`, `npm install`)
3. Running local development server (`npm start`)
4. Project structure explanation
5. Creating a new chapter (template, front-matter, file naming)
6. Adding code examples (language tags, commenting standards)
7. Creating exercises and solutions
8. Diagram creation (Mermaid syntax, ASCII art examples)
9. Testing code examples (ROS 2 Humble setup, Gazebo, Isaac)
10. Quality checks (word count, link validation, build test)
11. Committing changes (atomic commits, branch naming)
12. Deploying to GitHub Pages (`npm run build`, `gh-pages` deployment)

**Output**: `quickstart.md` with all setup steps and examples

### Phase 1 Acceptance Criteria
- [ ] `data-model.md` defines all content entities with attributes and relationships
- [ ] `contracts/docusaurus-config.yaml` provides complete sidebar structure
- [ ] `quickstart.md` enables new contributor to add chapter in <30 minutes
- [ ] All document templates created (chapter, exercise, solution)
- [ ] Agent context updated with Docusaurus conventions

## Phase 1: Agent Context Update

**Action**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

This updates `CLAUDE.md` (or equivalent agent context file) with:
- Docusaurus project structure
- Markdown/MDX formatting conventions
- Front-matter requirements
- Mermaid diagram syntax
- Code example standards
- Exercise and solution patterns
- Quality gate reminders

**Note**: Manual additions between markers are preserved.

## Post-Phase 1: Constitution Check Re-evaluation

After Phase 1 design completion, re-check Constitution compliance:

### Principle II: Technical Accuracy (NON-NEGOTIABLE)
- ✅ **PASS**: All APIs verified in `research.md` with official doc links
- ✅ **PASS**: API verification checklist created
- ✅ **PASS**: Code example verification process documented

### Content Standards: Simulation Fidelity
- ✅ **PASS**: Physics engine parameters documented in `research.md`
- ✅ **PASS**: RTX settings and domain randomization researched
- ✅ **PASS**: Sensor noise models for Gazebo/Unity/Isaac documented

**Final Status**: ✅ **FULL COMPLIANCE** - Ready for `/sp.tasks` to generate implementation tasks

## Next Steps

1. **Phase 0 Complete**: Generate `research.md` with all API verification (see Research Tasks above)
2. **Phase 1 Complete**: Generate `data-model.md`, `contracts/docusaurus-config.yaml`, `quickstart.md`
3. **Agent Context Updated**: Run update script to add Docusaurus conventions to agent guidance
4. **Ready for Tasks**: Run `/sp.tasks` to generate actionable task list for textbook implementation
5. **Implementation**: Follow task-driven workflow to create all chapters, exercises, and supporting materials

**Critical Path**:
- Phase 0 (Research) → Phase 1 (Design) → `/sp.tasks` (Task Generation) → Implementation (Chapter Creation)
- Module 1 (ROS 2) must complete before Modules 2-4 (foundational dependency)
- Capstone Project depends on all modules being complete

**Estimated Effort**:
- Phase 0 Research: 2-3 days
- Phase 1 Design: 1-2 days
- Task Generation: 1 day
- Module 1 Implementation: 2-3 weeks
- Module 2 Implementation: 2-3 weeks
- Module 3 Implementation: 2-3 weeks
- Module 4 Implementation: 2-3 weeks
- Capstone Project: 1 week
- Review & Polish: 1-2 weeks
- **Total**: 10-14 weeks (matches spec SC-009: maps to 10-14 week university course)
