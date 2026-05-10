---
name: coding-standards
description: >
  Team coding standards, naming conventions, and architecture
  patterns. Activate when writing or reviewing implementation
  [cite_start]code to enforce project-specific style and structural rules [cite: 1, 103-104].
---

# Procedural Instructions
When writing code for this repository, you MUST adhere to the following rules:
1. Always use functional programming patterns where possible.
2. Structure modules by feature, not by type.
3. Co-locate test files next to their implementation files (e.g., `module.test.js`).
4. Ensure all error handling uses the centralized `AppError` class.
