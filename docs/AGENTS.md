# Agent Instructions & Development Guidelines

This document serves as the primary instruction manual for any AI agent or developer working on this project. It defines the protocols for documentation, decision-making, and the development lifecycle.

## Core Philosophy
**"Document Intent Before Implementation"**

We expect the version control system to tell the story of change over time, but the `docs/` directory must be sufficient to re-implement the feature using agentic coding methods without the existing source code.

## Documentation Standards

### 1. Architectural Decision Records (ADRs)
**Location:** `docs/architecture/ADR-XXX-title.md`

Every significant architectural choice must be documented as an ADR. This ensures that future agents understand *why* a decision was made, not just *what* was implemented.

**Format:**
- **Title**: Short and descriptive.
- **Status**: Proposed, Accepted, Deprecated, or Superseded.
- **Context**: The problem we are solving and the forces at play.
- **Decision**: The choice we made.
- **Consequences**: The positive and negative implications of this decision.

### 2. Specifications
**Location:** `docs/specs/SPEC-XXX-title.md` (Create directory if needed)

Before writing code for a complex feature, create a specification document. This defines the "What" and "How" at a high level.

**Content:**
- **Goal**: What are we trying to achieve?
- **User Stories**: Who is this for and what do they need?
- **Technical Design**: Data models, API signatures, UI components.
- **Verification**: How will we know it works?

### 3. Development Journal
**Location:** `docs/JOURNAL.md`

A running log of the development process, capturing the "stream of consciousness" of the project's evolution. This is distinct from the git log as it captures the *reasoning* and *context* of the day-to-day work.

**Entries should include:**
- **Date/Time**: When the entry was made.
- **Context**: What are we working on?
- **Intent**: (Before Code) What do we plan to do and why?
- **Conclusion**: (After Code) What changed and how was it verified?

### 4. Agent Context
**Location:** `docs/agent_context/`

To preserve the evolutionary narrative and context for AI agents, we maintain the following artifacts in version control:
- `task.md`: The current master task list.
- `implementation_plan.md`: The technical design for the active task.
- `walkthrough.md`: Verification results for the most recent changes.

Agents should read and update these files to maintain state across sessions.

## Development Workflow

1.  **Define Intent (The "Pre-Commit")**:
    - **Action**: Update `docs/JOURNAL.md`.
    - **Content**: Define the "Intent", "Scope", and "Rationale" of the upcoming change.
    - **Goal**: Signal to the team (and future self) what is about to happen *before* touching the code.

2.  **Plan**:
    - Check `docs/roadmap.md` and `task.md`.
    - Create/Update a Specification or ADR if the task involves design decisions.

3.  **Implement**:
    - Write code that adheres to the `AGENTS.md` (root) technical conventions.
    - Keep changes atomic and focused.

4.  **Verify**:
    - Run tests.
    - Verify against the Specification.

5.  **Conclude (The "Post-Commit")**:
    - **Action**: Update `docs/JOURNAL.md`.
    - **Content**: Summarize "Changes", "Verification Results", and "Next Steps".
    - **Goal**: Close the loop on the cycle.

6.  **Document**:
    - Update `README.md` if user-facing changes occurred.

## Project Vision: The Universal Knowledge Base

**Goal**: Provide a self-contained and flexible environment for users to create their own knowledge bases from disparate sources.

**Scope:**
- **Multi-Source Ingestion**: Support ChatGPT, Claude, Gemini, and arbitrary file uploads.
- **Intelligent Management**: Automatic tagging, de-duplication, and organization.
- **Agentic RAG**: Custom tools for working with the local knowledge base.
- **Web Interface**: A rich UI for browsing and searching.
- **Extensibility**: Potential MCP service to expose this knowledge base to other tools.
