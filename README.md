# Gemini Skills: Automated Development Orchestration

## Introduction
This repository demonstrates how to use Gemini CLI skills to automate a complete software development lifecycle (SDLC) using a "Master Agent" pattern. It showcases a system where a central orchestrator manages specialized agents to handle different phases of development, from requirements gathering to deployment.

## The Pipeline
The project follows a structured 6-stage pipeline:
1.  **Task Understanding**: Analyzes the request and generates `TASK_REQUIREMENTS.md`.
2.  **Strategy**: Develops an implementation plan in `TASK_APPROACH.md`.
3.  **Implementation**: Executes the code changes and documents them in `IMPLEMENTATION_SUMMARY.md`.
4.  **Verification**: Runs tests and checks to ensure quality, producing `VERIFICATION_REPORT.md`.
5.  **Final Review**: A human-in-the-loop or high-level agent review producing `FINAL_REVIEW.md`.
6.  **GitHub Push**: Automates the final commit and push to the repository, documented in `PUSH_SUMMARY.md`.

## How it Works (Gemini Skills)

### .gemini/agents
These are the specialist agents, each defined with specific roles and responsibilities. They are invoked by the Master Agent to perform discrete tasks within the pipeline.
- **task-understanding-agent**: Focuses on clarity and scope.
- **task-approach-agent**: Architectures the solution.
- **write-code-agent**: Handles the actual coding.
- **verify-agent**: Ensures correctness and standards.
- **final-review-agent**: Provides the final quality gate.
- **push-to-github-agent**: Manages the release.

### .gemini/skills
Domain knowledge and specific capabilities are encapsulated as skills. For example, `coding-standards` defines the style and quality rules that the agents must follow.

### GEMINI.md
This is the master "instruction manual" for the orchestrator. It defines the pipeline flow, the hard gates between stages, and how agents should interact with the shared state in `.gemini/workspace/`.

## Commands Used (The Playbook)
To trigger the automated workflow, the user typically initiates a request through the Gemini CLI:
```bash
gemini "Implement a new feature or fix a bug..."
```
The Master Agent then interprets `GEMINI.md` and begins invoking the sub-agents internally using commands like:
```bash
gemini --agent task-understanding-agent "context..."
```

## Log & Trace Sections

### Log: Task Understanding
[Insert Screenshot of Agent Log Here]

### Log: Strategy (Task Approach)
[Insert Screenshot of Agent Log Here]

### Log: Implementation
[Insert Screenshot of Agent Log Here]

### Log: Verification
[Insert Screenshot of Agent Log Here]

### Log: Final Review
[Insert Screenshot of Agent Log Here]

### Log: GitHub Push
[Insert Screenshot of Agent Log Here]

## The "Live" Example
The repository contains a FastAPI Rate Limiter implementation which was developed and verified using this automated pipeline. This serves as a real-world example of the system's capability to handle complex tasks.

## Recreation Guide
To set up your own Master Agent orchestrator:
1.  **Clone the Repository**: `git clone <repo-url>`
2.  **Configure Agents**: Define your specialists in `.gemini/agents/`.
3.  **Define Skills**: Add domain-specific knowledge in `.gemini/skills/`.
4.  **Set Up the Orchestrator**: Customize `GEMINI.md` to define your desired SDLC pipeline.
5.  **Run**: Use the Gemini CLI to start your automated development tasks.
