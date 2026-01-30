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
  - `app.ts`: Main entry point for the TypeScript application.
  - **snake_game/**: Python implementation of Snake Game (Phase 1)
    - `game_board.py`: Game board and boundary management
    - `snake.py`: Snake state and movement logic
    - `food.py`: Food spawning and positioning
    - `game_engine.py`: Game orchestration and rule enforcement
    - `renderer.py`: Terminal UI rendering
    - `input_handler.py`: Keyboard input handling
    - `types.py`: Type definitions and enums
  - `main.py`: Snake game entry point
  - **types/**: TypeScript type definitions.
    - `index.ts`: Exports interfaces and types used throughout the application.

- **tests/**: Contains unit tests for the workflow scripts and application logic.
  - `workflow.test.ts`: Tests to ensure the scripts and application behave as expected.
  - **unit/**: Unit tests for Snake game components
    - `test_snake.py`: Snake class tests
    - `test_game_board.py`: GameBoard class tests
    - `test_food.py`: Food class tests
    - `test_game_engine.py`: GameEngine class tests
  - **integration/**: Integration tests
    - `test_full_game.py`: Full game flow tests

- `tsconfig.json`: TypeScript configuration file specifying compiler options.

- `package.json`: npm configuration file listing dependencies and scripts.

## Setup Instructions

### TypeScript Application

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-workflow-worktrees-test
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Review the documentation in `docs/AI_WORKFLOW_WORKTREES.md` for detailed workflow instructions.

### Snake Game (Python)

1. Ensure Python 3.8+ is installed:
   ```bash
   python3 --version
   ```

2. Create a virtual environment and install dev/test dependencies:
  ```bash
  python3 -m venv .venv
  ./.venv/bin/python -m pip install -U pip
  ./.venv/bin/python -m pip install -r requirements-dev.txt
  ```

## Usage Guidelines

### TypeScript Application

- Use the provided scripts in the `scripts/` directory to manage your worktrees effectively.
- Follow the roles outlined in the documentation to maintain a clean workflow.
- Run tests using the command:
  ```bash
  npm test
  ```

### Snake Game

#### Running the Game

To play the Snake game, run:

```bash
python3 src/main.py
```

**Controls:**
- **Arrow Keys** or **WASD**: Change snake direction
- **P**: Pause/Resume game
- **Q** or **ESC**: Quit game
- **R**: Restart game (when game over)

**Game Features:**
- Three difficulty levels (Easy, Medium, Hard) - selectable at start
- Colorized terminal display (snake=green, food=red, borders=blue)
- High score persistence across game sessions
- Pause/resume functionality

**Game Rules:**
- Snake starts at center of 20x20 grid with length 3
- Eat food (•) to grow and gain 10 points
- Snake wraps around walls (no game over on wall hit)
- Game ends when snake collides with itself

#### Running Tests

Run all tests:
```bash
./.venv/bin/python -m pytest tests/ -v
```

Run tests with coverage report:
```bash
./.venv/bin/python -m pytest tests/ --cov=src/snake_game --cov-report=term-missing
```

Run specific test files:
```bash
./.venv/bin/python -m pytest tests/unit/test_snake.py -v
./.venv/bin/python -m pytest tests/integration/test_full_game.py -v
```

#### Test Coverage

The Snake game implementation achieves **>90% code coverage** on core game logic:
- `snake.py`: 100% coverage
- `game_board.py`: 100% coverage
- `food.py`: 100% coverage
- `game_engine.py`: 97% coverage
- `types.py`: 100% coverage
- `high_score.py`: 82% coverage

Note: InputHandler and Renderer components are not covered by unit tests as they handle terminal I/O, which is tested through manual gameplay.

## Overview of the Workflow

This project implements a structured approach to software development using Git worktrees, allowing for efficient planning, implementation, and review processes. Each role is clearly defined to minimize context switching and enhance productivity.

## Snake Game Features

### ✅ Phase 1 Features (Implemented)
- 20x20 grid game board with wall wrap-around
- Snake movement in 4 directions (continuous motion)
- Food spawning at random valid positions
- Collision detection (self-collision ends game)
- Score tracking (+10 points per food)
- Snake growth when eating food
- Game over state with score display
- Terminal UI with box-drawing characters
- Keyboard controls (Arrow keys, WASD, Q, R)
- Direction reversal prevention
- Comprehensive unit and integration tests

### ✅ Phase 2 Features (Implemented)
- **Pause/Resume:** Press P to pause game, displays "PAUSED", P to resume
- **Difficulty Levels:** Easy/Medium/Hard selectable at game start (adjusts speed)
- **High Score Persistence:** Scores saved to file, survive restarts
- **Enhanced Rendering:** Colors for better readability
  - Snake: Green
  - Food: Red
  - Borders: Blue
  - Pause indicator: Yellow

### 📋 Phase 3 Features (Future)
- Multiplayer functionality
- Online leaderboards
- Sound effects
- GUI version