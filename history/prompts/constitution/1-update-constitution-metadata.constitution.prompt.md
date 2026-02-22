---
id: 1
title: Update constitution metadata
stage: constitution
date: 2025-12-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: UNKNOWN
command: /sp.constitution
labels: ["constitution", "metadata", "update"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - D:\Coding\AI-Native-book\.specify\memory\constitution.md
tests:
null
---

## Prompt

```text
# 📘 Physical AI & Humanoid Robotics
## An AI-Native Textbook for Embodied Intelligence

---

## 1. Purpose & Mission

This constitution defines the **non-negotiable principles, scope, and system behavior** for the AI-native textbook:

> **“Physical AI & Humanoid Robotics: Bridging Digital Intelligence and Physical Embodiment.”**

### Mission Statement

The mission of this book is to:

- Teach **Physical AI** as the next evolution of Artificial Intelligence
- Bridge **AI agents, robotics middleware, simulation, and humanoid embodiment**
- Deliver content as an **interactive, intelligent learning system**, not static text

This book must function as:

- A **university-level robotics textbook**
- A **hands-on engineering manual**
- An **AI-powered tutor via embedded agents**

---

## 2. Non-Negotiable Constraints

The system **MUST** adhere to the following constraints:

### Platform Constraints
- The book **MUST** be built using **Docusaurus**
- The book **MUST** be deployed publicly (**GitHub Pages or Vercel**)
- The source code **MUST** be in a **public GitHub repository**

### AI-Native Constraints
- A **Retrieval-Augmented Generation (RAG) chatbot** is mandatory
- The chatbot **MUST** answer questions **only from book content**
- The chatbot **MUST** support answering questions from **user-selected text**

### Engineering Constraints
- Backend **MUST** use **FastAPI**
- Vector storage **MUST** use **Qdrant Cloud (Free Tier)**
- Relational storage **MUST** use **Neon Serverless Postgres**
- AI orchestration **MUST** use **OpenAI Agents / ChatKit SDKs**

---

## 3. Pedagogical Philosophy

### Learning Model

This book follows a **Progressive Embodied Intelligence Model**:

1. **Digital Intelligence**
   *(LLMs, AI Agents, Planning)*

2. **Robotic Nervous System**
   *(ROS 2, Nodes, Topics, Actions)*

3. **Digital Twin**
   *(Simulation, Physics, Sensors)*

4. **Embodied Intelligence**
   *(Humanoid Motion, Perception, Balance)*

5. **Vision-Language-Action**
   *(Natural Language → Physical Action)*

Each chapter **MUST**:

- Explain **why** before **how**
l Locomotion & Balance
- Manipulation & Grasping

### Part VII — Conversational Robotics
- Conversational AI for Robots
- Multi-Modal Interaction (Vision, Voice, Gesture)

### Part VIII — Capstone
- The Autonomous Humanoid Project
- End-to-End System Architecture

### Part IX — Labs & Infrastructure
- Hardware Requirements & Lab Design
- Cloud-Native vs On-Prem Physical AI Labs

---

## 5. Chapter-Level Requirements

Each chapter **MUST** include:

- **Conceptual Overview**
- **System Architecture Diagram** (textual or visual)
- **Code Examples** (Python / ROS 2)
- **Simulation or Real-World Mapping**
- **Failure Modes & Debugging Notes**
- **AI Tutor Prompt Suggestions**

---

## 6. RAG Chatbot Constitution

### Behavior Rules

The embedded chatbot:

- **MUST NOT hallucinate**
- **MUST re- Connect **software abstractions** to **physical reality**
- Reinforce **systems thinking**

---

## 4. Canonical Book Structure (Immutable)

The textbook **MUST** follow this high-level structure.

### Part I — Foundations of Physical AI
- Introduction to Physical AI & Embodied Intelligence
- From Digital Brains to Physical Bodies
- Humanoid Robotics Landscape

### Part II — The Robotic Nervous System (ROS 2)
- ROS 2 Architecture & Philosophy
- Nodes, Topics, Services, and Actions
- Python Agents with `rclpy`
- URDF & Robot Description for Humanoids

### Part III — Digital Twins & Simulation
- Gazebo Physics & Environment Simulation
- Sensor Simulation (LiDAR, Cameras, IMU)
- Unity for Human-Robot Interaction

### Part IV — The AI-Robot Brain (NVIDIA Isaac)
- NVIDIA Isaac Sim & Omniverse
- Synthetic Data Generation
- Isaac ROS, VSLAM & Nav2
- Sim-to-Real Transfer

### Part V — Vision-Language-Action (VLA)
- Voice-to-Action with Whisper
- LLM-Driven Cognitive Planning
- Translating Language into ROfuse** to answer questions outside book scope
- **MUST cite** chapter sources internally
- **MUST prioritize selected text** when provided

### Modes of Operation
1. **Full-Book Query Mode**
2. **Selected-Text-Only Mode**
3. **Chapter-Scoped Mode**

---

## 7. Personalization Constitution (Bonus)

When a user is authenticated:

### Background Variables
- Software experience level
- Hardware availability
- Robotics familiarity

### Personalization Rules
- **Beginner** → More explanations, diagrams
- **Advanced** → Math, optimization, internals
- **No GPU** → Cloud alternatives emphasized

Personalization **MUST NOT**:
- Remove core concepts
- Break technical correctness

---

## 8. Translation Constitution (Urdu)

- Translation **MUST preserve technical terms**
- English technical words may remain untranslated
- Urdu output **MUST be clear and instructional**
- Translation is **chapter-scoped**

---

## 9. Reusable Intelligence Constitution

Claude Code Subagents **SHOULD** be defined for:

- Chapter drafting
- Code validation
- Concept simplification
- Diagram generation
- RAG chunk optimization

All subagents **MUST**:
- Be reusable
- Be domain-specific
- Avoid duplication

---

## 10. Quality Standards

This book is considered **complete** only if:

- All modules align with the course syllabus
- The chatbot can answer at least:
  - ROS 2 questions
  - Gazebo simulation questions
  - Isaac / VLA questions
- The capstone is fully described **end-to-end**

---

## 11. Final Authority

This constitution is the **single source of truth**.

If any content, code, agent, or feature:

- Violates this constitution
  → **It must be corrected or removed.**

---
```

## Response snapshot

The constitution has been updated to version `2.0.1`. This is a patch version bump due to an update in the `LAST_AMENDED_DATE` without changes to the core content.

The following templates require manual follow-up to ensure alignment with the updated constitution principles. Note that some files were not found:
- `.specify/templates/plan-template.md`
- `.specify/templates/spec-template.md`
- `.specify/templates/tasks-template.md`
- `.specify/templates/commands/sp.constitution.md` (file not found)
- `.specify/templates/commands/sp.phr.md` (file not found)
- `README.md` (file not found)

Suggested commit message: `docs: amend constitution to v2.0.1 (metadata update)`

## Outcome

- ✅ Impact: The constitution file metadata was updated successfully, and a summary was provided to the user.
- 🧪 Tests: No tests were run.
- 📁 Files: `D:\Coding\AI-Native-book\.specify\memory\constitution.md` was modified.
- 🔁 Next prompts: None.
- 🧠 Reflection: The operation was a re-execution of an existing constitution update, leading to a patch version bump for metadata.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): None.
- Prompt variant (if applicable): None.
- Next experiment (smallest change to try): None.
