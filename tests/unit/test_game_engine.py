"""Unit tests for the GameEngine class."""

import pytest
from src.snake_game.game_engine import GameEngine
from src.snake_game.types import Direction, GameState


class TestGameEngine:
    """Test suite for GameEngine class."""
    
    def test_game_initialization(self):
        """Test that game initializes correctly."""
        engine = GameEngine()
        
        assert engine.board is not None
        assert engine.snake is not None
        assert engine.food is not None
        assert engine.score == 0
        assert engine.state == GameState.RUNNING
        assert engine.food.get_position() is not None  # Food spawned
    
    def test_game_custom_board_size(self):
        """Test game initialization with custom board size."""
        engine = GameEngine(board_width=15, board_height=15)
        
        width, height = engine.board.get_dimensions()
        assert width == 15
        assert height == 15
    
    def test_tick_moves_snake(self):
        """Test that tick moves snake forward."""
        engine = GameEngine()
        initial_head = engine.snake.get_head_position()
        
        engine.tick()
        
        new_head = engine.snake.get_head_position()
        assert new_head != initial_head
    
    def test_handle_input_changes_direction(self):
        """Test that handle_input changes snake direction."""
        engine = GameEngine()
        
        engine.handle_input(Direction.UP)
        engine.tick()
        
        # Snake should move up
        assert engine.snake.direction == Direction.UP
    
    def test_handle_input_prevents_reversal(self):
        """Test that handle_input prevents direction reversal."""
        engine = GameEngine()
        initial_direction = engine.snake.direction
        
        # Try to reverse direction (from RIGHT to LEFT)
        engine.handle_input(Direction.LEFT)
        
        # Direction should not change
        assert engine.snake.direction == initial_direction
    
    def test_wrap_around_right_wall(self):
        """Test that snake wraps to left side when hitting right wall."""
        engine = GameEngine(board_width=10, board_height=10)
        
        # Position snake at right edge
        engine.snake.body = [(9, 5), (8, 5), (7, 5)]
        engine.snake.direction = Direction.RIGHT
        
        # Move toward wall
        engine.tick()
        
        # Should wrap to left side (x=0)
        assert engine.snake.get_head_position() == (0, 5)
        assert engine.state == GameState.RUNNING
    
    def test_wrap_around_left_wall(self):
        """Test that snake wraps to right side when hitting left wall."""
        engine = GameEngine(board_width=10, board_height=10)
        
        # Position snake at left edge
        engine.snake.body = [(0, 5), (1, 5), (2, 5)]
        engine.snake.direction = Direction.LEFT
        
        # Move toward wall
        engine.tick()
        
        # Should wrap to right side (x=9)
        assert engine.snake.get_head_position() == (9, 5)
        assert engine.state == GameState.RUNNING
    
    def test_wrap_around_top_wall(self):
        """Test that snake wraps to bottom when hitting top wall."""
        engine = GameEngine(board_width=10, board_height=10)
        
        # Position snake at top edge
        engine.snake.body = [(5, 0), (5, 1), (5, 2)]
        engine.snake.direction = Direction.UP
        
        # Move toward wall
        engine.tick()
        
        # Should wrap to bottom (y=9)
        assert engine.snake.get_head_position() == (5, 9)
        assert engine.state == GameState.RUNNING
    
    def test_wrap_around_bottom_wall(self):
        """Test that snake wraps to top when hitting bottom wall."""
        engine = GameEngine(board_width=10, board_height=10)
        
        # Position snake at bottom edge
        engine.snake.body = [(5, 9), (5, 8), (5, 7)]
        engine.snake.direction = Direction.DOWN
        
        # Move toward wall
        engine.tick()
        
        # Should wrap to top (y=0)
        assert engine.snake.get_head_position() == (5, 0)
        assert engine.state == GameState.RUNNING
    
    def test_no_game_over_on_wall_hit(self):
        """Test that game continues after wall hit (wrap-around happens)."""
        engine = GameEngine(board_width=10, board_height=10)
        
        # Position snake near right wall
        engine.snake.body = [(8, 5), (7, 5), (6, 5)]
        engine.snake.direction = Direction.RIGHT
        
        # Move to edge and beyond
        engine.tick()  # Position (9, 5)
        assert engine.state == GameState.RUNNING
        
        engine.tick()  # Position (0, 5) - wrapped
        assert engine.state == GameState.RUNNING
        assert engine.snake.get_head_position()[0] == 0
    
    def test_self_collision_ends_game(self):
        """Test that self-collision ends the game."""
        engine = GameEngine(board_width=10, board_height=10)
        
        # Manually create a snake in a position where next move will collide
        # Snake forms an L shape, moving into its own body
        engine.snake.body = [(5, 5), (4, 5), (3, 5), (3, 6), (4, 6), (5, 6), (6, 6)]
        engine.snake.direction = Direction.DOWN
        engine.snake._grow_pending = False  # Ensure no pending growth
        
        # Do a tick which will move and check collisions
        engine.tick()
        
        # Game should be over due to self-collision
        assert engine.state == GameState.GAME_OVER
    
    def test_food_consumption_increases_score(self):
        """Test that eating food increases score."""
        engine = GameEngine()
        
        # Position snake head at food location
        food_pos = engine.food.get_position()
        dx, dy = engine.snake.direction.value
        engine.snake.body = [
            (food_pos[0] - dx, food_pos[1] - dy),
            (food_pos[0] - 2*dx, food_pos[1] - 2*dy),
            (food_pos[0] - 3*dx, food_pos[1] - 3*dy)
        ]
        
        initial_score = engine.score
        engine.tick()
        
        assert engine.score == initial_score + 10
    
    def test_food_consumption_grows_snake(self):
        """Test that eating food makes snake grow."""
        engine = GameEngine()
        
        # Position snake near food
        food_pos = engine.food.get_position()
        dx, dy = engine.snake.direction.value
        
        # Position snake one step before food
        engine.snake.body = [
            (food_pos[0] - dx, food_pos[1] - dy),
            (food_pos[0] - 2 * dx, food_pos[1] - 2 * dy),
            (food_pos[0] - 3 * dx, food_pos[1] - 3 * dy)
        ]
        
        # Tick to eat food (growth is pending after this)
        engine.tick()
        
        # Verify food was eaten
        assert engine.get_score() == 10
        
        # Growth happens on next move
        engine.tick()
        
        # Now snake should have grown
        assert len(engine.snake.get_body()) == 4
    
    def test_food_consumption_spawns_new_food(self):
        """Test that eating food spawns new food."""
        engine = GameEngine()
        
        # Position snake head at food location
        food_pos = engine.food.get_position()
        dx, dy = engine.snake.direction.value
        engine.snake.body = [
            (food_pos[0] - dx, food_pos[1] - dy),
            (food_pos[0] - 2*dx, food_pos[1] - 2*dy),
            (food_pos[0] - 3*dx, food_pos[1] - 3*dy)
        ]
        
        engine.tick()
        
        # New food should be spawned
        new_food_pos = engine.food.get_position()
        assert new_food_pos is not None
        assert new_food_pos != food_pos or engine.state == GameState.GAME_OVER
    
    def test_score_tracking(self):
        """Test that score tracks correctly through multiple foods."""
        engine = GameEngine()
        
        # Simulate eating 3 foods
        for i in range(3):
            food_pos = engine.food.get_position()
            dx, dy = engine.snake.direction.value
            engine.snake.body[0] = (food_pos[0] - dx, food_pos[1] - dy)
            engine.tick()
            
            if engine.state == GameState.GAME_OVER:
                break
        
        # Score should be at least 30 if we successfully ate 3 foods
        if engine.state == GameState.RUNNING:
            assert engine.score >= 30
    
    def test_get_state(self):
        """Test getting game state."""
        engine = GameEngine()
        
        assert engine.get_state() == GameState.RUNNING
    
    def test_get_score(self):
        """Test getting current score."""
        engine = GameEngine()
        engine.score = 50
        
        assert engine.get_score() == 50
    
    def test_restart_resets_game(self):
        """Test that restart resets game state."""
        engine = GameEngine()
        
        # Play for a bit
        engine.score = 30
        engine.state = GameState.GAME_OVER
        
        # Restart
        engine.restart()
        
        assert engine.score == 0
        assert engine.state == GameState.RUNNING
        assert len(engine.snake.get_body()) == 3
        assert engine.food.get_position() is not None
    
    def test_tick_does_not_update_when_game_over(self):
        """Test that tick doesn't update when game is over."""
        engine = GameEngine()
        engine.state = GameState.GAME_OVER
        
        head_before = engine.snake.get_head_position()
        engine.tick()
        head_after = engine.snake.get_head_position()
        
        assert head_before == head_after
    
    def test_handle_input_ignored_when_game_over(self):
        """Test that input is ignored when game is over."""
        engine = GameEngine()
        engine.state = GameState.GAME_OVER
        
        direction_before = engine.snake.direction
        engine.handle_input(Direction.UP)
        
        assert engine.snake.direction == direction_before
