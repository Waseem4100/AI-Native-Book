# Physical AI Textbook Constitution

<!--
Sync Impact Report (Constitution v1.0.0):
- Version change: [TEMPLATE] → 1.0.0
- Initial constitution creation for AI-Native Textbook project
- Added principles: Content Modularity, Technical Accuracy, Docusaurus Standards, Pedagogical Structure, Version Control Ready, Physical AI Focus
- Added sections: Content Standards, Development Workflow, Governance
- Templates flagged for review:
  ✅ spec-template.md (aligned with modular content requirements)
  ✅ plan-template.md (aligned with constitution check references)
  ✅ tasks-template.md (aligned with independent testable components)
- Follow-up: None
- Rationale: New project initialization - all principles are foundational requirements
-->

## Core Principles

### I. Content Modularity
Every chapter MUST be self-contained, independently readable, and versioned. Chapters MUST NOT depend on forward references except where explicitly cross-referenced. Each module consists of multiple chapters, each chapter contains digestible sections. No chapter exceeds 3000 words without subdivision.

**Rationale**: Educational content must support non-linear learning paths and allow instructors to remix materials.

### II. Technical Accuracy (NON-NEGOTIABLE)
All robotics APIs, ROS 2 interfaces, NVIDIA Isaac features, and simulation physics MUST be verified against official documentation. No invented APIs, fake package names, or hallucinated parameters. When uncertain, mark with `[NEEDS VERIFICATION]` and cite source requirements.

**Rationale**: Inaccurate technical content in educational materials causes student frustration, wasted lab time, and loss of trust.

### III. Docusaurus Standards
Every content file MUST be Docusaurus-compatible (.md or .mdx), include proper front-matter (title, description, sidebar_position), and follow GitHub Pages deployment requirements. Code blocks MUST specify language for syntax highlighting. Diagrams MUST use Mermaid or ASCII art.

**Rationale**: Consistency enables automated deployment, searchability, and professional presentation.

### IV. Pedagogical Structure
Each chapter MUST include: (1) Learning Objectives, (2) Conceptual Explanation, (3) Code Examples, (4) Hands-On Exercises, (5) Comprehension Questions. Concepts progress from foundational to advanced. Real-world robotics applications anchor abstract concepts.

**Rationale**: Structured pedagogy maximizes retention and enables self-paced learning.

### V. Version Control Ready
Content MUST be granular (one chapter = one file), commit messages MUST reference chapter/module numbers, and changes MUST be reviewable by educators. Each commit represents a complete pedagogical unit (not mid-sentence edits).

**Rationale**: Multiple authors and reviewers require clean diff histories and atomic changes.

### VI. Physical AI Focus
All content MUST prioritize embodied intelligence, simulation-to-real transfer, and humanoid robotics use cases. Generic AI/ML content is OUT OF SCOPE unless directly applicable to robot control. Every module includes ROS 2 + simulation + real robot considerations.

**Rationale**: This textbook differentiates itself by bridging digital AI models with physical robotic systems.

## Content Standards

### Code Quality
- All Python code follows PEP 8
- ROS 2 code uses rclpy best practices (lifecycle nodes, QoS profiles)
- URDF/SDF models include comments explaining joint types and inertial properties
- Launch files use descriptive parameter names
- Every code block includes explanatory comments for students

### Simulation Fidelity
- Gazebo examples specify physics engine and time step
- Unity examples note rendering pipeline and sensor noise models
- Isaac Sim examples document RTX settings and domain randomization parameters
- All simulations include "Limitations" subsection explaining sim-to-real gap

### Exercise Design
- Exercises progress from guided (step-by-step) to open-ended projects
- Each exercise specifies expected time commitment (15min, 1hr, 3hrs)
- Capstone projects integrate multiple modules
- Solutions and rubrics stored separately in `/solutions/` (not in main chapters)

### Terminology Consistency
- "Humanoid robot" not "humanoid" alone
- "ROS 2" not "ROS2" or "ROS"
- "Isaac Sim" for simulation, "Isaac ROS" for accelerated nodes
- "Vision-Language-Action (VLA)" on first use, then "VLA"
- Glossary maintained in `/docs/glossary.md`

## Development Workflow

### Content Creation Process
1. **Specification**: Define chapter scope, learning objectives, prerequisites in `/specs/<module>-<chapter>/spec.md`
2. **Outline**: Create detailed section outline in `/specs/<module>-<chapter>/plan.md`
3. **Draft**: Write full chapter with placeholders for unverified APIs (`[NEEDS VERIFICATION]`)
4. **Verification**: Test all code examples in ROS 2 + simulation environment
5. **Review**: Educator review for pedagogy, technical accuracy, accessibility
6. **Integration**: Add to Docusaurus sidebar, update module index, cross-link related chapters

### Quality Gates
Before merging any chapter:
- [ ] All code examples execute without errors in target environment (ROS 2 Humble + Gazebo 11 or Isaac Sim)
- [ ] Learning objectives map to comprehension questions
- [ ] No `[NEEDS VERIFICATION]` or `[TODO]` markers remain
- [ ] Front-matter complete (title, description, sidebar_position, tags)
- [ ] Cross-references use correct relative paths
- [ ] Spell check passed (technical terms added to dictionary)

### Module Structure (Mandatory)
```
docs/
├── module-1-ros2/
│   ├── index.md              # Module overview + learning path
│   ├── ch1-middleware.md
│   ├── ch2-nodes-topics.md
│   ├── ch3-urdf-modeling.md
│   └── exercises/
│       └── ex1-first-node.md
├── module-2-simulation/
│   ├── index.md
│   ├── ch1-physics.md
│   └── ...
└── module-4-vla/
    ├── index.md
    ├── capstone-project.md
    └── ...
```

### Branching Strategy
- `main` = published textbook (GitHub Pages deployment)
- `module-<N>-draft` = work-in-progress module
- Feature branches: `chapter-<module>-<chapter>-<slug>` (e.g., `chapter-1-3-urdf-basics`)
- PRs require: (1) educator review, (2) technical accuracy check, (3) all quality gates passed

## Governance

### Constitution Authority
This constitution supersedes all previous content guidelines. Any content violating these principles MUST be rejected or revised before merge. Complexity not justified by pedagogical necessity is forbidden.

### Amendment Process
Constitution changes require:
1. Proposal with educational rationale
2. Review by lead instructor + technical architect
3. Version bump (MAJOR for removed principles, MINOR for new principles, PATCH for clarifications)
4. Migration plan for existing content
5. Update to all affected templates (spec, plan, tasks)

### Compliance Review
Every PR is checked against:
- Technical Accuracy (Principle II)
- Docusaurus Standards (Principle III)
- Pedagogical Structure (Principle IV)
- Physical AI Focus (Principle VI)

Violations are flagged in PR comments with specific constitution reference (e.g., "Violates Principle II: ROS API not verified").

### Complexity Justification
Any content addition requiring tools/dependencies beyond ROS 2 + Gazebo/Unity + Isaac MUST document:
- Educational necessity (which learning objective requires it?)
- Simpler alternatives rejected and why
- Impact on student setup burden

**Version**: 1.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16
