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

### Log:

<img width="1758" height="1188" alt="Image 10-05-26 at 6 44 PM" src="https://github.com/user-attachments/assets/4e697b10-bd43-42f5-bc54-949ddaadc713" />


<img width="1686" height="785" alt="Image 10-05-26 at 6 52 PM (1)" src="https://github.com/user-attachments/assets/cd04212a-9290-4711-8b1a-e24c19be897a" />

### Log: Push
<img width="1558" height="156" alt="Image 10-05-26 at 7 46 PM" src="https://github.com/user-attachments/assets/583a978d-e199-40ac-854e-9a66d0751687" />


## The "Live" Example
The repository contains a FastAPI Rate Limiter implementation which was developed and verified using this automated pipeline. This serves as a real-world example of the system's capability to handle complex tasks.

### Recreation Guide: Setting Up Your Own Orchestrator

**Step 1: Initialize the Workspace**
Run the following command in your terminal to set up the necessary directory structure for the pipeline:
```bash
mkdir -p .gemini/workspace .gemini/agents .gemini/skills
```

**Step 2: Define the Subagents**
Drop your agent definition files into the `.gemini/agents/` directory. Subagents are defined as Markdown files that specify their persona, tools, and responsibilities.

**Step 3: Create or Install the Skills**
Drop your skill directories into the `.gemini/skills/` folder. A skill is simply a directory containing a `SKILL.md` file along with any optional bundled assets. If you do not want to scaffold the files manually, you can ask the built-in `skill-creator` to handle the directory structure and boilerplate for you.

**Step 4: Set the Master Orchestration Rules**
Add your Master Agent orchestration rules to the `GEMINI.md` file in the root of your project. Because this file is loaded on every request, it is the exact right place for pipeline governance and routing instructions.

**Step 5: Run the Pipeline**
Start an interactive session by running the `gemini` command. Give it your initial task, and the pipeline will run. Each agent reads from and writes to `.gemini/workspace/`, creating a fully inspectable audit trail as the pipeline executes.
