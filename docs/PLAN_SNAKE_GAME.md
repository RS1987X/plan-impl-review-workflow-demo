# Plan: Snake Game Implementation

**Status:** Planning Phase  
**Created:** 2026-01-29  
**Scope:** Classic snake game with modern features

---

## 1. Project Overview

Build a classic snake game with clean architecture, comprehensive tests, and a simple terminal-based UI. The game should be playable, maintainable, and serve as a demonstration of the planner/implementer/reviewer workflow.

### Goals
- Implement core snake game mechanics
- Provide smooth, responsive controls
- Track and display score
- Support multiple difficulty levels
- Clean separation of concerns (game logic, rendering, input)

### Non-Goals (for initial release)
- Graphical UI (terminal only for Phase 1)
- Multiplayer functionality
- Online leaderboards
- Sound effects
- Power-ups or special items

---

## 2. Phases

### Phase 1: Core Gameplay (MVP)
- Grid-based game board
- Snake movement (4 directions)
- Food spawning
- Collision detection (walls, self)
- Score tracking
- Game over state

### Phase 2: Polish & Features (Post-MVP)
- Difficulty levels (speed adjustment)
- Pause/resume functionality
- High score persistence
- Better terminal rendering (colors, borders)

### Phase 3: Testing & Documentation (Final)
- Comprehensive unit tests
- Integration tests
- Performance tests
- User documentation

---

## 3. Technical Architecture

### Core Components

#### GameBoard
- **Responsibility:** Maintains grid state, bounds checking
- **Data:** 2D grid representation, dimensions
- **Methods:** 
  - `is_valid_position(x, y) -> bool`
  - `get_dimensions() -> (width, height)`

#### Snake
- **Responsibility:** Snake state, movement, growth
- **Data:** Body segments (list of coordinates), current direction
- **Methods:**
  - `move(direction) -> None`
  - `grow() -> None`
  - `get_head_position() -> (x, y)`
  - `get_body() -> List[(x, y)]`
  - `collides_with_self() -> bool`

#### Food
- **Responsibility:** Food placement and tracking
- **Data:** Current food position
- **Methods:**
  - `spawn(board, snake) -> None` - Place food in valid empty position
  - `get_position() -> (x, y)`

#### GameEngine
- **Responsibility:** Game loop, state management, rule enforcement
- **Data:** GameBoard, Snake, Food, score, game state (running/paused/game_over)
- **Methods:**
  - `start() -> None`
  - `tick() -> None` - Process one game update
  - `handle_input(direction) -> None`
  - `check_collisions() -> None`
  - `get_state() -> GameState`

#### Renderer
- **Responsibility:** Display game state to terminal
- **Methods:**
  - `render(game_state) -> None`
  - `clear_screen() -> None`
  - `display_game_over(score) -> None`

#### InputHandler
- **Responsibility:** Capture and validate user input
- **Methods:**
  - `get_input() -> Optional[Direction]`
  - `configure_terminal() -> None`
  - `restore_terminal() -> None`

---

## 4. Game Rules & Mechanics

### Grid Layout
- Default size: 20x20 cells
- Coordinate system: (0,0) is top-left
- Walls are solid boundaries (collision = game over)

### Snake Mechanics
- Initial length: 3 segments
- Initial position: Center of board
- Initial direction: Right
- Speed: Configurable tick rate (default: 10 ticks/second)

### Movement Rules
- Snake moves one cell per tick in current direction
- Direction changes are queued and applied at next tick
- Cannot reverse direction (e.g., can't go from RIGHT to LEFT directly)
- Movement is continuous (no stop state)

### Food Mechanics
- One food item on board at a time
- Spawns at random empty position
- When eaten:
  - Snake grows by 1 segment
  - Score increases by 10 points
  - New food spawns immediately

### Collision Detection
- **Wall collision:** Head touches border → game over
- **Self collision:** Head touches any body segment → game over
- **Food collision:** Head occupies same cell as food → eat food

### Scoring
- +10 points per food eaten
- Display current score during gameplay
- Display final score on game over

---

## 5. User Interface Specifications

### Terminal Display (Phase 1)

```
Score: 120                    High Score: 340

╔════════════════════════╗
║                        ║
║         •              ║
║                        ║
║      ○○○               ║
║      ○                 ║
║                        ║
║                        ║
╔════════════════════════╗

Controls: ↑↓←→  |  Q: Quit  |  P: Pause
```

### Display Symbols
- Snake head: `○` or `@`
- Snake body: `○`
- Food: `•` or `*`
- Empty cell: ` ` (space)
- Border: `╔═╗║╚╝` (box drawing characters)

### Controls
- Arrow keys: Change direction
- `W/A/S/D`: Alternative direction controls
- `P`: Pause/unpause
- `Q` or `ESC`: Quit game
- `R`: Restart (on game over)

---

## 6. Acceptance Criteria

### Must Have (Phase 1)
1. ✓ Snake moves continuously in current direction
2. ✓ Arrow keys/WASD change direction (no reversing)
3. ✓ Food spawns at random valid positions
4. ✓ Snake grows when eating food
5. ✓ Score increases by 10 per food
6. ✓ Game ends on wall collision
7. ✓ Game ends on self collision
8. ✓ Score is displayed during gameplay
9. ✓ Game over screen shows final score
10. ✓ User can quit at any time

### Nice to Have (Phase 2)
- Pause functionality
- Difficulty levels (speed variations)
- High score persistence (saved to file)
- Color-coded display (snake=green, food=red)

---

## 7. Edge Cases & Error Handling

### Edge Cases to Handle

1. **Rapid Direction Changes**
   - User presses multiple keys in quick succession
   - Solution: Queue only the latest valid direction per tick

2. **No Valid Food Spawn Position**
   - Snake fills entire board (theoretical win condition)
   - Solution: Treat as game over with victory message

3. **Terminal Resize**
   - User resizes terminal during gameplay
   - Solution: Phase 1 - ignore; Phase 2 - pause and prompt restart

4. **Input During Pause**
   - User presses arrow keys while paused
   - Solution: Ignore movement input, only accept unpause/quit

5. **First Move Reversal**
   - At game start, user immediately presses opposite direction
   - Solution: Prevent reversal same as during gameplay

### Error Handling

- **Terminal not supported:** Graceful error message, exit cleanly
- **Cannot configure terminal:** Fall back to basic input or exit with message
- **Invalid direction input:** Ignore, maintain current direction
- **File I/O errors (high score):** Log warning, continue without persistence

---

## 8. Test Plan

### Unit Tests

#### Snake Tests
- `test_snake_initial_state()` - Verify starting position, length, direction
- `test_snake_movement()` - Test movement in all 4 directions
- `test_snake_growth()` - Verify grow() adds segment correctly
- `test_snake_self_collision_detection()` - Various self-collision scenarios
- `test_snake_direction_reversal_prevention()` - Cannot reverse direction

#### GameBoard Tests
- `test_board_initialization()` - Correct dimensions
- `test_valid_position_checking()` - Boundary validation
- `test_position_out_of_bounds()` - Negative/exceeding coordinates

#### Food Tests
- `test_food_spawn_valid_position()` - Food spawns in empty cell
- `test_food_spawn_avoids_snake()` - Food not placed on snake
- `test_food_spawn_randomness()` - Distribution check (statistical)

#### GameEngine Tests
- `test_game_initialization()` - All components set up correctly
- `test_tick_moves_snake()` - Snake advances one cell per tick
- `test_food_consumption()` - Snake grows, score increases, new food spawns
- `test_wall_collision_ends_game()` - Game over on boundary hit
- `test_self_collision_ends_game()` - Game over on self hit
- `test_score_tracking()` - Score increments correctly
- `test_direction_queueing()` - Direction changes applied correctly

### Integration Tests

- `test_full_game_flow()` - Start, move, eat, collision, game over
- `test_multiple_food_consumption()` - Extended gameplay sequence
- `test_edge_to_edge_movement()` - Snake navigates entire board
- `test_maximum_length_snake()` - Fill board completely

### Performance Tests

- `test_tick_performance()` - Game loop maintains target tick rate
- `test_large_snake_performance()` - Performance with very long snake
- `test_collision_detection_performance()` - Efficient collision checks

---

## 9. File Structure

```
src/
  snake_game/
    __init__.py
    game_board.py      # GameBoard class
    snake.py           # Snake class
    food.py            # Food class
    game_engine.py     # GameEngine class
    renderer.py        # Renderer class
    input_handler.py   # InputHandler class
    types.py           # Direction enum, GameState enum, Position type
  main.py              # Entry point

tests/
  unit/
    test_snake.py
    test_game_board.py
    test_food.py
    test_game_engine.py
  integration/
    test_full_game.py
  performance/
    test_performance.py
```

---

## 10. Known Limitations & Trade-offs

### Terminal Dependency
- **Limitation:** Game only works in terminal environments with proper support
- **Trade-off:** Simplicity vs. accessibility; Phase 1 prioritizes simple implementation
- **Future:** Consider GUI version (pygame/tkinter) in later phase

### Frame Rate Consistency
- **Limitation:** Terminal rendering may have slight jitter on some systems
- **Trade-off:** Portability vs. smoothness; avoiding platform-specific optimizations
- **Mitigation:** Target conservative tick rate (10 Hz default)

### Input Handling
- **Limitation:** Terminal input is polled, not event-driven
- **Trade-off:** Simple implementation vs. instant responsiveness
- **Impact:** Slight input lag acceptable for snake game pace

### Single-threaded Design
- **Decision:** Game loop runs in single thread
- **Rationale:** Snake game logic is simple, no need for threading complexity
- **Benefit:** Easier to test, debug, and reason about

### No Persistence (Phase 1)
- **Limitation:** High scores lost on exit
- **Rationale:** Focus on core gameplay first
- **Future:** Add JSON/sqlite persistence in Phase 2

---

## 11. Dependencies

### Required
- Python 3.8+
- Standard library only for Phase 1:
  - `time` - Game loop timing
  - `random` - Food placement
  - `sys`, `tty`, `termios` - Terminal control (Unix)
  - `enum` - Type definitions
  - `dataclasses` - Data structures

### Testing
- `pytest` - Test framework
- `pytest-cov` - Coverage reporting

### Optional (Phase 2+)
- `colorama` - Cross-platform color support
- `blessed` - Advanced terminal handling

---

## 12. Success Metrics

A successful implementation should:

1. **Be playable** - User can complete multiple full games without crashes
2. **Be responsive** - Input lag < 100ms, maintains 10 FPS minimum
3. **Be correct** - All game rules enforced accurately
4. **Be tested** - >90% code coverage, all edge cases covered
5. **Be maintainable** - Clear separation of concerns, documented code

---

## 13. Implementation Notes for Implementer

When implementing, follow these constraints:

- **Phase 1 only:** Implement core gameplay only; skip pause, difficulty, persistence
- **Keep it simple:** Prefer clarity over cleverness
- **Test as you go:** Write tests alongside implementation
- **Terminal handling:** Use `tty`/`termios` for Unix; gracefully fail on Windows in Phase 1

### Suggested Implementation Order

1. Define types (Direction, Position, GameState)
2. Implement GameBoard (simplest component)
3. Implement Snake (core logic, well-tested)
4. Implement Food (simple, depends on Board + Snake)
5. Implement GameEngine (orchestration)
6. Implement InputHandler (terminal I/O)
7. Implement Renderer (display)
8. Wire up main.py (entry point)
9. Integration testing
10. Polish & bug fixes

---

## 14. Questions for Reviewer

During review, please validate:

- Are game rules implemented correctly per spec?
- Is the code structure clean and maintainable?
- Are edge cases properly handled?
- Is test coverage adequate (>90%)?
- Does the terminal rendering work on Linux/Mac?
- Is the gameplay feel right (speed, responsiveness)?

---

**End of Plan**
