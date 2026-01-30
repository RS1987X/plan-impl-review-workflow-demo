# Architecture

This document is a maintainer-oriented map of the codebase: what the components are, how they fit together, and where to start when debugging or adding features.

## System Overview

- **Entry point:** `src/main.py`
- **Core game logic:** `src/snake_game/`
- **Tests:** `tests/unit/` and `tests/integration/`

## Modules (Snake)

- `snake_game/game_engine.py`: orchestrates state transitions and applies game rules per tick.
- `snake_game/snake.py`: owns snake body, movement, growth, and self-collision checks.
- `snake_game/game_board.py`: board dimensions and bounds/position validation.
- `snake_game/food.py`: food placement/spawning (must avoid snake).
- `snake_game/renderer.py`: terminal rendering (UI only; logic should remain elsewhere).
- `snake_game/input_handler.py`: terminal input parsing (UI only; logic should remain elsewhere).
- `snake_game/types.py`: shared enums and data types.

## State Model

Document the authoritative game state(s) and transitions here.

- RUNNING → PAUSED → RUNNING
- RUNNING → GAME_OVER

## Debugging Playbook (quick)

- Unit tests: `python -m pytest tests/unit -q`
- Integration tests: `python -m pytest tests/integration -q`
- Run game: `python src/main.py`

## Adding Features (guidelines)

- Keep game rules in `game_engine.py` and pure model classes.
- Keep terminal I/O concerns isolated to `renderer.py` and `input_handler.py`.
- Prefer adding/adjusting unit tests for new rules before extending rendering.
