# AI Workflow Worktrees Test Project

This project is designed to implement and test the workflow described in the AI Workflow document. It utilizes Git worktrees to facilitate parallel roles for planning, implementing, and reviewing code changes.

## Project Structure

- **docs/**: Contains the documentation for the AI workflow.
  - `AI_WORKFLOW_WORKTREES.md`: Documentation outlining the roles, responsibilities, and processes involved in using Git worktrees.

- **scripts/**: Contains automation scripts for managing worktrees.
  - `create-worktrees.sh`: Script to automate the creation of Git worktrees.
  - `sync-worktrees.sh`: Script to synchronize worktrees with the latest changes from the main branch.
  - `remove-worktrees.sh`: Script to remove created worktrees and clean up directories.

- **src/**: Contains the source code for the application.
  - `app.ts`: Main entry point for the application.
  - **types/**: Contains type definitions.
    - `index.ts`: Exports interfaces and types used throughout the application.

- **tests/**: Contains unit tests for the workflow scripts and application logic.
  - `workflow.test.ts`: Tests to ensure the scripts and application behave as expected.

- `tsconfig.json`: TypeScript configuration file specifying compiler options.

- `package.json`: npm configuration file listing dependencies and scripts.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ai-workflow-worktrees-test
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Review the documentation in `docs/AI_WORKFLOW_WORKTREES.md` for detailed workflow instructions.

## Usage Guidelines

- Use the provided scripts in the `scripts/` directory to manage your worktrees effectively.
- Follow the roles outlined in the documentation to maintain a clean workflow.
- Run tests using the command:
  ```
  npm test
  ```

## Overview of the Workflow

This project implements a structured approach to software development using Git worktrees, allowing for efficient planning, implementation, and review processes. Each role is clearly defined to minimize context switching and enhance productivity.