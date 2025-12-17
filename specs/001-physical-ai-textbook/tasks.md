# Tasks: Physical AI & Humanoid Robotics Textbook

**Input**: Design documents from `/specs/001-physical-ai-textbook/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Organization**: Tasks are grouped by user story (Module 1-4, Capstone) to enable independent implementation and testing of each module.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)
- Include exact file paths in descriptions

## Path Conventions

- **Docs**: `docs/` at repository root
- **Solutions**: `solutions/` at repository root (NOT under docs/)
- **Static assets**: `static/` for minimal assets only
- Paths shown below use absolute paths from repository root

---

## Phase 1: Project Setup & Infrastructure

**Purpose**: Initialize Docusaurus project and create foundational structure

### Docusaurus Initialization

- [ ] T001 Initialize Docusaurus 3.x project with docs-only mode configuration
- [ ] T002 Configure `docusaurus.config.js` with Physical AI metadata, GitHub Pages deployment
- [ ] T003 Create `sidebars.js` with complete navigation structure from contracts/docusaurus-config.yaml
- [ ] T004 Install and configure Mermaid plugin for diagram support
- [ ] T005 Configure Prism for syntax highlighting (Python, Bash, YAML, XML)
- [ ] T006 [P] Create `package.json` with all dependencies (Docusaurus, React, Mermaid)
- [ ] T007 [P] Set up GitHub Actions workflow for automated deployment (`.github/workflows/deploy.yml`)

### Project Structure Setup

- [ ] T008 Create `docs/` directory structure for all 4 modules + capstone + appendix
- [ ] T009 Create `solutions/` directory structure (module-1/ through module-4/, capstone/)
- [ ] T010 [P] Create `static/img/` directory for favicon and minimal branding assets
- [ ] T011 [P] Create `README.md` with contributor setup instructions (reference quickstart.md)

**Checkpoint**: Docusaurus project initializes successfully with `npm start`, blank site loads

---

## Phase 2: Foundational Content (Blocking Prerequisites)

**Purpose**: Core infrastructure content that MUST be complete before ANY module can be implemented

**⚠️ CRITICAL**: No module work can begin until this phase is complete

### Homepage & Navigation

- [ ] T012 Create `docs/intro.md` (homepage) with textbook overview, target audience, prerequisites, learning outcomes
- [ ] T013 Create `docs/glossary.md` (glossary template) with initial 20 robotics terms (ROS 2, URDF, node, topic, service, action, etc.)
- [ ] T014 [P] Create CSS customizations in `src/css/custom.css` for Physical AI theme

### Appendix (Reference Materials)

- [ ] T015 Create `docs/appendix/prerequisites.md` (Linux basics, Python, ROS 2 Humble installation guide)
- [ ] T016 [P] Create `docs/appendix/troubleshooting.md` (common errors and solutions for ROS 2, Gazebo, Isaac)
- [ ] T017 [P] Create `docs/appendix/resources.md` (external learning materials, official docs links)

**Checkpoint**: Foundation ready - module implementation can now begin in parallel

---

## Phase 3: User Story 1 - Module 1: ROS 2 Foundations (Priority: P1) 🎯 MVP

**Goal**: Students master robot middleware, create ROS 2 nodes, control humanoid joints, build URDF models

**Independent Test**: Students complete module exercises (creating nodes, pub/sub, URDF) and control simulated humanoid joints

### Module 1 Index

- [ ] T018 [US1] Create `docs/module-1-ros2/index.md` (Module 1 overview, learning path, estimated duration 2-3 weeks)

### Module 1 Chapters

- [ ] T019 [US1] Write `docs/module-1-ros2/ch1-middleware.md` (ROS 2 middleware fundamentals, DDS, architecture)
  - 5-part structure: objectives, explanation, code (minimal node example), exercises ref, comprehension questions
  - Mermaid diagram: ROS 2 vs ROS 1 architecture comparison
  - Word count: ~2500 words

- [ ] T020 [US1] Write `docs/module-1-ros2/ch2-nodes-topics.md` (Nodes, topics, publisher/subscriber pattern)
  - 5-part structure with publisher/subscriber code examples
  - Mermaid diagram: Topic communication flow
  - Word count: ~2800 words

- [ ] T021 [US1] Write `docs/module-1-ros2/ch3-services-actions.md` (Services for request/response, Actions for long-running tasks)
  - 5-part structure with service client/server code, action server/client code
  - Mermaid diagram: Service vs Action comparison
  - Word count: ~2700 words

- [ ] T022 [US1] Write `docs/module-1-ros2/ch4-rclpy-control.md` (Python rclpy for humanoid joint control)
  - 5-part structure with shoulder joint controller code
  - Position vs velocity control explanation
  - Word count: ~2600 words

- [ ] T023 [US1] Write `docs/module-1-ros2/ch5-urdf-modeling.md` (URDF for humanoid robot modeling, visualization in RViz)
  - 5-part structure with simple humanoid URDF example
  - ASCII diagram: URDF link-joint hierarchy
  - Word count: ~2900 words

### Module 1 Exercises

- [ ] T024 [P] [US1] Create `docs/module-1-ros2/exercises/ex1-first-node.md` (30min guided: create minimal ROS 2 node)
- [ ] T025 [P] [US1] Create `docs/module-1-ros2/exercises/ex2-publisher-subscriber.md` (1hr intermediate: pub/sub for joint commands)
- [ ] T026 [P] [US1] Create `docs/module-1-ros2/exercises/ex3-urdf-humanoid.md` (2hrs open-ended: build basic humanoid URDF)

### Module 1 Solutions

- [ ] T027 [P] [US1] Write `solutions/module-1/ex1-first-node.py` (verified solution with rubric)
- [ ] T028 [P] [US1] Write `solutions/module-1/ex2-publisher-subscriber.py` (verified solution with rubric)
- [ ] T029 [P] [US1] Write `solutions/module-1/ex3-urdf-humanoid.urdf` (verified URDF with comments)

### Code Verification

- [ ] T030 [US1] Test all Module 1 code examples in ROS 2 Humble environment (ch1-ch5 code blocks)
- [ ] T031 [US1] Test all Module 1 solutions in ROS 2 Humble + Gazebo 11
- [ ] T032 [US1] Update glossary with Module 1 terms (25-30 new entries)

**Checkpoint**: Module 1 complete and independently testable. Students can create nodes, control joints, build URDF.

---

## Phase 4: User Story 2 - Module 2: Simulation with Gazebo & Unity (Priority: P2)

**Goal**: Students master physics simulation, sensor simulation, environment building for humanoids

**Independent Test**: Students build Gazebo world, simulate sensors (LiDAR, depth, IMU), create Unity HRI scene

### Module 2 Index

- [ ] T033 [US2] Create `docs/module-2-simulation/index.md` (Module 2 overview, learning path, estimated duration 2-3 weeks)

### Module 2 Chapters

- [ ] T034 [US2] Write `docs/module-2-simulation/ch1-digital-twin.md` (What is a Digital Twin? Simulation vs reality)
  - 5-part structure with simulation-to-real transfer explanation
  - Mermaid diagram: Digital Twin architecture
  - Word count: ~2400 words

- [ ] T035 [US2] Write `docs/module-2-simulation/ch2-gazebo-physics.md` (Gazebo 11 physics engine, ODE, time step, gravity, inertia)
  - 5-part structure with physics parameter configuration (SDF world file)
  - "Limitations" subsection on sim-to-real gap
  - Word count: ~2800 words

- [ ] T036 [US2] Write `docs/module-2-simulation/ch3-unity-interaction.md` (Unity for high-fidelity HRI visualization, ROS-TCP-Connector)
  - 5-part structure with Unity setup, URDF import, ROS 2 integration
  - Word count: ~2700 words

- [ ] T037 [US2] Write `docs/module-2-simulation/ch4-sensor-simulation.md` (LiDAR, depth camera, RGB camera, IMU simulation)
  - 5-part structure with sensor plugin configuration (SDF)
  - Mermaid diagram: Sensor data flow (sensor → ROS topic → processing)
  - Word count: ~2900 words

- [ ] T038 [US2] Write `docs/module-2-simulation/ch5-complete-simulation.md` (Building full humanoid simulation with sensors)
  - 5-part structure with complete Gazebo world + humanoid + sensors
  - Integration of all previous chapters
  - Word count: ~2800 words

### Module 2 Exercises

- [ ] T039 [P] [US2] Create `docs/module-2-simulation/exercises/ex1-gazebo-world.md` (1hr intermediate: build Gazebo world with obstacles)
- [ ] T040 [P] [US2] Create `docs/module-2-simulation/exercises/ex2-sensor-setup.md` (1hr intermediate: attach LiDAR and depth camera to humanoid)
- [ ] T041 [P] [US2] Create `docs/module-2-simulation/exercises/ex3-unity-scene.md` (2hrs open-ended: create Unity scene for HRI)

### Module 2 Solutions

- [ ] T042 [P] [US2] Write `solutions/module-2/ex1-gazebo-world.world` (verified SDF world file)
- [ ] T043 [P] [US2] Write `solutions/module-2/ex2-sensor-setup.urdf` (verified URDF with sensors)
- [ ] T044 [P] [US2] Write `solutions/module-2/ex3-unity-scene/` (Unity project directory with setup instructions)

### Code Verification

- [ ] T045 [US2] Test all Module 2 code examples in Gazebo 11 (physics configs, sensor plugins)
- [ ] T046 [US2] Test all Module 2 solutions in Gazebo 11 + Unity (if Unity available)
- [ ] T047 [US2] Update glossary with Module 2 terms (20-25 new entries: Gazebo, physics engine, sensors)

**Checkpoint**: Module 2 complete and independently testable. Students can simulate physics, sensors, HRI.

---

## Phase 5: User Story 3 - Module 3: NVIDIA Isaac for AI-Robot Brain (Priority: P3)

**Goal**: Students use Isaac Sim for photorealistic simulation, Isaac ROS for perception, Nav2 for path planning

**Independent Test**: Students set up Isaac Sim, run VSLAM, configure Nav2 for humanoid path planning

### Module 3 Index

- [ ] T048 [US3] Create `docs/module-3-isaac/index.md` (Module 3 overview, learning path, estimated duration 2-3 weeks, GPU requirements)

### Module 3 Chapters

- [ ] T049 [US3] Write `docs/module-3-isaac/ch1-intro-isaac.md` (NVIDIA Isaac overview, Isaac Sim vs Gazebo, RTX requirements)
  - 5-part structure with Isaac Sim installation guide
  - Mermaid diagram: Isaac ecosystem (Sim, ROS, Gym)
  - Word count: ~2500 words

- [ ] T050 [US3] Write `docs/module-3-isaac/ch2-isaac-sim.md` (Photorealistic simulation, USD format, domain randomization)
  - 5-part structure with URDF→USD conversion, synthetic data generation
  - "Limitations" subsection on RTX hardware requirements
  - Word count: ~2800 words

- [ ] T051 [US3] Write `docs/module-3-isaac/ch3-isaac-ros.md` (Isaac ROS perception stack, hardware acceleration, GEMs)
  - 5-part structure with Isaac ROS DNN inference example
  - Mermaid diagram: Isaac ROS pipeline (camera → preprocessing → DNN → output)
  - Word count: ~2700 words

- [ ] T052 [US3] Write `docs/module-3-isaac/ch4-vslam.md` (Visual SLAM with Isaac ROS, depth perception, odometry)
  - 5-part structure with VSLAM node launch, camera calibration
  - Word count: ~2800 words

- [ ] T053 [US3] Write `docs/module-3-isaac/ch5-nav2.md` (Nav2 path planning for humanoids, costmap config, behavior trees)
  - 5-part structure with Nav2 configuration for bipedal robots
  - Mermaid diagram: Nav2 stack (localization, planning, control)
  - Word count: ~2900 words

- [ ] T054 [US3] Write `docs/module-3-isaac/ch6-ai-brain.md` (AI-controlled humanoid brain, integrating perception + planning)
  - 5-part structure with complete Isaac Sim + Isaac ROS + Nav2 pipeline
  - Integration of all previous chapters
  - Word count: ~2800 words

### Module 3 Exercises

- [ ] T055 [P] [US3] Create `docs/module-3-isaac/exercises/ex1-isaac-setup.md` (1hr guided: install Isaac Sim, import humanoid)
- [ ] T056 [P] [US3] Create `docs/module-3-isaac/exercises/ex2-vslam-demo.md` (2hrs intermediate: run VSLAM with simulated camera)
- [ ] T057 [P] [US3] Create `docs/module-3-isaac/exercises/ex3-nav2-humanoid.md` (3hrs open-ended: configure Nav2 for humanoid navigation)

### Module 3 Solutions

- [ ] T058 [P] [US3] Write `solutions/module-3/ex1-isaac-setup.md` (step-by-step guide with screenshots/ASCII diagrams)
- [ ] T059 [P] [US3] Write `solutions/module-3/ex2-vslam-demo.py` (verified Isaac ROS VSLAM launch script)
- [ ] T060 [P] [US3] Write `solutions/module-3/ex3-nav2-humanoid.yaml` (verified Nav2 config for humanoid)

### Code Verification

- [ ] T061 [US3] Test all Module 3 code examples in Isaac Sim 2023.1+ (if GPU available; otherwise document requirements)
- [ ] T062 [US3] Test all Module 3 solutions in Isaac Sim + Isaac ROS
- [ ] T063 [US3] Update glossary with Module 3 terms (20-25 new entries: Isaac, VSLAM, Nav2, costmap)

**Checkpoint**: Module 3 complete and independently testable. Students can use Isaac for perception and navigation.

---

## Phase 6: User Story 4 - Module 4: Vision-Language-Action (VLA) (Priority: P4)

**Goal**: Students integrate LLMs with robotics, implement voice-to-action pipelines, complete Capstone Project

**Independent Test**: Students implement Whisper voice recognition, LLM task planning, ROS 2 action execution

### Module 4 Index

- [ ] T064 [US4] Create `docs/module-4-vla/index.md` (Module 4 overview, learning path, estimated duration 2-3 weeks)

### Module 4 Chapters

- [ ] T065 [US4] Write `docs/module-4-vla/ch1-vla-intro.md` (VLA overview: Vision + Language + Action convergence)
  - 5-part structure with VLA architecture explanation
  - Mermaid diagram: VLA pipeline (voice → LLM → actions → robot)
  - Word count: ~2400 words

- [ ] T066 [US4] Write `docs/module-4-vla/ch2-whisper.md` (OpenAI Whisper for voice commands, transcription)
  - 5-part structure with Whisper ROS 2 node example
  - Word count: ~2600 words

- [ ] T067 [US4] Write `docs/module-4-vla/ch3-llm-ros2.md` (LLM → ROS 2 action translation, GPT-4/Claude/open-source)
  - 5-part structure with LLM planner node (prompt engineering)
  - Word count: ~2800 words

- [ ] T068 [US4] Write `docs/module-4-vla/ch4-cognitive-planning.md` (Hierarchical task decomposition, LLM reasoning)
  - 5-part structure with task decomposition example ("bring me the red cup" → navigate, detect, grasp, place)
  - Mermaid diagram: Task hierarchy tree
  - Word count: ~2700 words

- [ ] T069 [US4] Write `docs/module-4-vla/ch5-integration.md` (Integrating Vision + Language + Action, computer vision object detection)
  - 5-part structure with full VLA pipeline code
  - Integration of all previous modules (ROS 2, simulation, Isaac, VLA)
  - Word count: ~2900 words

### Module 4 Exercises

- [ ] T070 [P] [US4] Create `docs/module-4-vla/exercises/ex1-whisper-setup.md` (1hr guided: set up Whisper ROS 2 node)
- [ ] T071 [P] [US4] Create `docs/module-4-vla/exercises/ex2-llm-actions.md` (2hrs intermediate: LLM task planner)
- [ ] T072 [P] [US4] Create `docs/module-4-vla/exercises/ex3-full-pipeline.md` (3hrs open-ended: complete voice-to-action pipeline)

### Module 4 Solutions

- [ ] T073 [P] [US4] Write `solutions/module-4/ex1-whisper-setup.py` (verified Whisper ROS 2 node)
- [ ] T074 [P] [US4] Write `solutions/module-4/ex2-llm-actions.py` (verified LLM planner node)
- [ ] T075 [P] [US4] Write `solutions/module-4/ex3-full-pipeline/` (complete VLA system with all components)

### Code Verification

- [ ] T076 [US4] Test all Module 4 code examples (Whisper transcription, LLM API calls)
- [ ] T077 [US4] Test all Module 4 solutions (voice input → action execution in simulation)
- [ ] T078 [US4] Update glossary with Module 4 terms (15-20 new entries: VLA, LLM, Whisper, prompt engineering)

**Checkpoint**: Module 4 complete and independently testable. Students can build voice-controlled robots with LLM planning.

---

## Phase 7: Capstone Project - "The Autonomous Humanoid Assistant"

**Goal**: Comprehensive final project integrating all 4 modules

**Independent Test**: Students complete Capstone, demonstrating voice-controlled humanoid that navigates, detects objects, and executes pick-and-place

### Capstone Documents

- [ ] T079 [US4] Write `docs/capstone/project-overview.md` (Capstone introduction, requirements, expected outcomes)
  - Project scope: voice command → task plan → navigation → object detection → pick-and-place
  - Estimated time: 15-20 hours
  - Word count: ~2500 words

- [ ] T080 [US4] Write `docs/capstone/architecture.md` (System architecture diagrams, component breakdown)
  - Mermaid diagrams: Overall system architecture, ROS 2 node graph, data flow
  - Component list: Whisper node, LLM planner, Nav2, object detector, grasp controller
  - Word count: ~2400 words

- [ ] T081 [US4] Write `docs/capstone/implementation.md` (Step-by-step implementation guide)
  - Phase 1: Voice input setup
  - Phase 2: LLM task planning
  - Phase 3: Navigation with Nav2
  - Phase 4: Object detection with Isaac ROS or OpenCV
  - Phase 5: Grasp execution
  - Phase 6: Integration and testing
  - Word count: ~2900 words

- [ ] T082 [US4] Write `docs/capstone/evaluation.md` (Evaluation rubric, testing procedures, grading criteria)
  - Rubric: Voice recognition (10 pts), Task planning (15 pts), Navigation (20 pts), Detection (20 pts), Grasp (20 pts), Integration (15 pts)
  - Word count: ~2000 words

- [ ] T083 [US4] Write `docs/capstone/optional-hardware.md` (Sim-to-real deployment guidance, real robot considerations)
  - Hardware requirements, calibration, safety considerations
  - Word count: ~1800 words

### Capstone Solutions

- [ ] T084 [US4] Write `solutions/capstone/full-solution/README.md` (complete Capstone implementation overview)
- [ ] T085 [US4] Write `solutions/capstone/full-solution/whisper_node.py` (voice input node)
- [ ] T086 [US4] Write `solutions/capstone/full-solution/llm_planner.py` (LLM task decomposition)
- [ ] T087 [US4] Write `solutions/capstone/full-solution/navigation_controller.py` (Nav2 integration)
- [ ] T088 [US4] Write `solutions/capstone/full-solution/object_detector.py` (computer vision detection)
- [ ] T089 [US4] Write `solutions/capstone/full-solution/grasp_controller.py` (pick-and-place execution)
- [ ] T090 [US4] Write `solutions/capstone/full-solution/main.py` (main integration script)
- [ ] T091 [US4] Write `solutions/capstone/full-solution/launch/capstone.launch.py` (ROS 2 launch file for all nodes)

### Code Verification

- [ ] T092 [US4] Test complete Capstone solution in simulation (Isaac Sim or Gazebo)
- [ ] T093 [US4] Verify all Capstone components integrate correctly
- [ ] T094 [US4] Document known limitations and troubleshooting tips in capstone/implementation.md

**Checkpoint**: Capstone Project complete. Students demonstrate full Physical AI stack (perception, planning, control, VLA).

---

## Phase 8: User Story 5 - Instructor Course Integration (Priority: P5)

**Purpose**: Ensure textbook is "course-ready" for instructors

### Instructor Materials

- [ ] T095 [P] [US5] Create instructor guide in `docs/instructor-guide.md` (course structure, lesson plans, time allocation)
- [ ] T096 [P] [US5] Document exercise time estimates in each module index.md (align with spec SC-009: 10-14 week course)
- [ ] T097 [P] [US5] Verify all solutions include grading rubrics (10-point scale for each exercise)

### Deployment & Access

- [ ] T098 [US5] Test GitHub Pages deployment workflow (`.github/workflows/deploy.yml`)
- [ ] T099 [US5] Verify Docusaurus build completes in <5 minutes (`npm run build`)
- [ ] T100 [US5] Test site loads in <3 seconds on standard broadband

**Checkpoint**: Textbook is instructor-ready and deployable.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Finalize textbook for publication

### Glossary Completion

- [ ] T101 [P] Finalize `docs/glossary.md` with all robotics terms from all modules (target: 120 terms)
- [ ] T102 [P] Alphabetize glossary entries
- [ ] T103 [P] Add cross-references between glossary terms

### Quality Assurance

- [ ] T104 Run link validation checker (no broken internal links)
- [ ] T105 Run word count validation (all chapters ≤ 3000 words)
- [ ] T106 Verify all code examples have language tags (Python, Bash, YAML, XML)
- [ ] T107 Verify all chapters include front-matter (title, description, sidebar_position)
- [ ] T108 Verify all Mermaid diagrams render correctly
- [ ] T109 Run spell check on all markdown files (add robotics terms to dictionary)

### Final Testing

- [ ] T110 Build Docusaurus site (`npm run build`) and verify no errors
- [ ] T111 Test all cross-references between chapters
- [ ] T112 Verify sidebar navigation matches contracts/docusaurus-config.yaml
- [ ] T113 Test search functionality (Algolia or local search)
- [ ] T114 Run quickstart.md validation (new contributor can add chapter in <30 minutes)

### Documentation

- [ ] T115 Update README.md with project overview, setup instructions, contribution guidelines
- [ ] T116 Create CONTRIBUTING.md with detailed contribution workflow (reference quickstart.md)
- [ ] T117 [P] Create LICENSE file (MIT or CC BY-SA for educational content)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Project Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational Content)**: Depends on Phase 1 completion - BLOCKS all modules
- **Phase 3 (Module 1)**: Depends on Phase 2 - FOUNDATIONAL (blocks Modules 2-4)
- **Phase 4 (Module 2)**: Depends on Phase 3 (Module 1) - can proceed after Module 1 complete
- **Phase 5 (Module 3)**: Depends on Phase 3 (Module 1) - can proceed after Module 1 complete (parallel with Module 2)
- **Phase 6 (Module 4)**: Depends on Phase 3 (Module 1) - can proceed after Module 1 complete (parallel with Modules 2-3)
- **Phase 7 (Capstone)**: Depends on Phases 3-6 (all modules) - requires all modules complete
- **Phase 8 (Instructor Integration)**: Depends on Phases 3-7 - can proceed once content complete
- **Phase 9 (Polish)**: Depends on all content phases - final cleanup

### Module Dependencies

- **Module 1 (ROS 2)**: MUST complete first - provides foundational knowledge for all other modules
- **Modules 2-4**: Can proceed in parallel after Module 1, but Module 4 (VLA) benefits from Module 3 (Isaac) completion
- **Capstone**: Requires all 4 modules complete

### Within Each Module

- Module index before chapters
- Chapters can be written in parallel (ch1-ch5 independent)
- Exercises can be created in parallel with chapters
- Solutions created immediately after corresponding exercise
- Code verification after all code examples and solutions complete
- Glossary updates after code verification

### Parallel Opportunities

- **Phase 1**: All tasks except T001-T003 (config files) can run in parallel
- **Phase 2**: Appendix documents (T015-T017) can run in parallel
- **Within Modules**: Chapters (after index), exercises, and solutions can all run in parallel
- **Modules 2-4**: Can be developed in parallel after Module 1 complete
- **Phase 9**: QA tasks (T104-T109), documentation (T115-T117) can run in parallel

---

## Parallel Example: Module 1 Chapter Creation

```bash
# Launch all Module 1 chapters in parallel (after index complete):
Task T019: "Write ch1-middleware.md"
Task T020: "Write ch2-nodes-topics.md"
Task T021: "Write ch3-services-actions.md"
Task T022: "Write ch4-rclpy-control.md"
Task T023: "Write ch5-urdf-modeling.md"

# Launch all Module 1 exercises in parallel (after chapters):
Task T024: "Create ex1-first-node.md"
Task T025: "Create ex2-publisher-subscriber.md"
Task T026: "Create ex3-urdf-humanoid.md"

# Launch all Module 1 solutions in parallel (after exercises):
Task T027: "Write ex1-first-node.py"
Task T028: "Write ex2-publisher-subscriber.py"
Task T029: "Write ex3-urdf-humanoid.urdf"
```

---

## Implementation Strategy

### MVP First (Module 1 Only)

1. Complete Phase 1: Project Setup
2. Complete Phase 2: Foundational Content (homepage, glossary, appendix)
3. Complete Phase 3: Module 1 (ROS 2 Foundations)
4. **STOP and VALIDATE**: Test Module 1 independently, verify students can complete exercises
5. Deploy MVP to GitHub Pages for early feedback

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add Module 1 → Test independently → Deploy (MVP!)
3. Add Module 2 → Test independently → Deploy
4. Add Module 3 → Test independently → Deploy
5. Add Module 4 → Test independently → Deploy
6. Add Capstone → Test integration → Deploy
7. Polish & instructor materials → Final release

### Parallel Team Strategy

With multiple content creators:

1. Team completes Setup + Foundational together
2. Once Foundational done and Module 1 complete:
   - Creator A: Module 2 (Simulation)
   - Creator B: Module 3 (Isaac)
   - Creator C: Module 4 (VLA)
3. All creators: Capstone Project (collaborative)
4. Team: Polish & QA together

---

## Success Criteria (from Spec)

The textbook is complete when:

- **SC-001**: ✅ Students can create ROS 2 nodes controlling humanoid joints (Module 1 exercises pass)
- **SC-002**: ✅ Students can build Gazebo simulations with sensor-equipped humanoids (Module 2 exercises pass)
- **SC-003**: ✅ Students can configure Nav2 path planning in Isaac Sim (Module 3 exercises pass)
- **SC-004**: ✅ Students can implement voice-to-action pipelines (Module 4 exercises pass)
- **SC-005**: ✅ Students complete Capstone Project demonstrating autonomous humanoid assistant
- **SC-006**: ✅ Instructors deploy textbook to GitHub Pages in <30 minutes (T098-T100 pass)
- **SC-007**: ✅ 90% of code examples execute without errors (all code verification tasks pass)
- **SC-008**: ✅ Each module independently testable (checkpoints after each phase)
- **SC-009**: ✅ Textbook maps to 10-14 week university course (time estimates in module indexes)
- **SC-010**: ✅ Students articulate full Physical AI stack after completion (Capstone evaluation rubric)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to user story (US1-US5) for traceability
- Each module is independently completable and testable (checkpoints validate)
- Module 1 MUST complete before Modules 2-4 (foundational dependency)
- Capstone MUST complete after all modules (integration dependency)
- All code examples verified in target environments before merge
- Commit after each task or logical group (e.g., all Module 1 chapters)
- Stop at checkpoints to validate module independently before proceeding
- Estimated total: 117 tasks, 10-14 weeks with parallel execution

**Total Tasks**: 117
**Estimated Effort**: 10-14 weeks (matches spec SC-009)

---

## Task Execution Checklist (Per Task)

Before marking a task complete:

- [ ] Content follows 5-part pedagogical structure (if chapter)
- [ ] Word count ≤ 3000 words (if chapter)
- [ ] Front-matter complete (title, description, sidebar_position)
- [ ] Code examples include language tags and explanatory comments
- [ ] Mermaid diagrams render correctly
- [ ] No `[TODO]`, `[NEEDS VERIFICATION]`, or `{{PLACEHOLDER}}` markers
- [ ] Cross-references use correct relative paths
- [ ] File saved to exact path specified in task description
- [ ] Code examples verified in target environment (ROS 2 Humble, Gazebo, Isaac)
- [ ] Constitution principles satisfied (modularity, accuracy, standards, pedagogy, version control, focus)
