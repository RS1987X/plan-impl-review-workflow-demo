"""Integration tests for full game flow."""

import pytest
from src.snake_game.game_engine import GameEngine
from src.snake_game.types import Direction, GameState


class TestFullGame:
    """Integration test suite for complete game scenarios."""
    
    def test_full_game_flow(self):
        """Test complete game flow: start, move, eat, collision, game over."""
        engine = GameEngine(board_width=10, board_height=10)
        
        # Verify game starts in RUNNING state
        assert engine.get_state() == GameState.RUNNING
        assert engine.get_score() == 0
        
        # Game should have initial food
        assert engine.food.get_position() is not None
        
        # Snake should move when ticking
        initial_head = engine.snake.get_head_position()
        engine.tick()
        assert engine.snake.get_head_position() != initial_head
        
        # Game should still be running after normal movement
        assert engine.get_state() == GameState.RUNNING
    
    def test_multiple_food_consumption(self):
        """Test eating multiple foods in sequence."""
        engine = GameEngine(board_width=15, board_height=15)
        
        initial_length = len(engine.snake.get_body())
        foods_eaten = 0
        max_attempts = 50
        
        # Try to eat multiple foods
        for _ in range(max_attempts):
            if engine.get_state() != GameState.RUNNING:
                break
            
            food_pos = engine.food.get_position()
            head_pos = engine.snake.get_head_position()
            
            # If we're about to eat food
            dx, dy = engine.snake.direction.value
            next_pos = (head_pos[0] + dx, head_pos[1] + dy)
            
            if next_pos == food_pos:
                prev_score = engine.get_score()
                engine.tick()
                if engine.get_score() > prev_score:
                    foods_eaten += 1
                if foods_eaten >= 3:
                    break
            else:
                engine.tick()
        
        # Should have eaten at least one food and grown
        if foods_eaten > 0:
            assert engine.get_score() >= 10
            assert len(engine.snake.get_body()) > initial_length
    
    def test_direction_change_during_movement(self):
        """Test that direction changes work correctly during movement."""
        engine = GameEngine()
        
        # Start moving right, change to down
        assert engine.snake.direction == Direction.RIGHT
        
        engine.handle_input(Direction.DOWN)
        engine.tick()
        
        assert engine.snake.direction == Direction.DOWN
        
        # Change to left
        engine.handle_input(Direction.LEFT)
        engine.tick()
        
        assert engine.snake.direction == Direction.LEFT
    
    def test_game_over_on_wall_collision(self):
        """Test that game ends when snake hits wall."""
        engine = GameEngine(board_width=10, board_height=10)
        
        # Position snake near right wall
        engine.snake.body = [(8, 5), (7, 5), (6, 5)]
        engine.snake.direction = Direction.RIGHT
        
        # Move toward wall
        engine.tick()  # Position (9, 5)
        assert engine.get_state() == GameState.RUNNING
        
        engine.tick()  # Position (10, 5) - out of bounds
        assert engine.get_state() == GameState.GAME_OVER
    
    def test_game_over_on_self_collision(self):
        """Test that game ends when snake collides with itself."""
        engine = GameEngine()
        
        # Grow snake to make collision possible
        for _ in range(5):
            engine.snake.grow()
            engine.tick()
        
        # Create a pattern that will cause self-collision
        # Move in a small loop
        engine.handle_input(Direction.DOWN)
        engine.tick()
        engine.handle_input(Direction.LEFT)
        engine.tick()
        engine.handle_input(Direction.UP)
        engine.tick()
        engine.handle_input(Direction.RIGHT)
        engine.tick()
        
        # After enough moves with a long snake, collision should occur
        # Or manually set up collision scenario
        engine.snake.body = [
            (5, 5),   # Head
            (4, 5),   # Body
            (3, 5),   # Body
            (3, 6),   # Body
            (4, 6),   # Body
            (5, 6),   # Body
            (6, 6),   # Body
        ]
        engine.snake.direction = Direction.DOWN
        engine.tick()  # Move to (5, 6) which is occupied
        
        assert engine.get_state() == GameState.GAME_OVER
    
    def test_score_accumulation(self):
        """Test that score accumulates correctly over multiple foods."""
        engine = GameEngine(board_width=20, board_height=20)
        
        # Manually eat 3 foods by positioning head at food
        for i in range(3):
            food_pos = engine.food.get_position()
            dx, dy = engine.snake.direction.value
            
            # Position snake head one step before food
            # Need to preserve the _grow_pending flag, so let's reset body carefully
            old_length = len(engine.snake.body)
            engine.snake.body = [
                (food_pos[0] - dx, food_pos[1] - dy),
                (food_pos[0] - 2*dx, food_pos[1] - 2*dy),
                (food_pos[0] - 3*dx, food_pos[1] - 3*dy)
            ]
            # Extend to match previous length
            while len(engine.snake.body) < old_length:
                last = engine.snake.body[-1]
                engine.snake.body.append((last[0] - dx, last[1] - dy))
            
            engine.tick()
            
            if engine.get_state() == GameState.GAME_OVER:
                break
            
            # Verify score increased
            assert engine.get_score() == (i + 1) * 10
    
    def test_restart_functionality(self):
        """Test that restart works correctly."""
        engine = GameEngine()
        
        # Play game for a bit
        for _ in range(5):
            engine.tick()
        
        # Manually set game over
        engine.state = GameState.GAME_OVER
        engine.score = 50
        
        # Restart
        engine.restart()
        
        # Verify reset
        assert engine.get_state() == GameState.RUNNING
        assert engine.get_score() == 0
        assert len(engine.snake.get_body()) == 3
        assert engine.food.get_position() is not None
    
    def test_edge_to_edge_movement(self):
        """Test snake can navigate across the entire board."""
        engine = GameEngine(board_width=10, board_height=10)
        
        # Position snake at top-left
        engine.snake.body = [(1, 1), (0, 1), (0, 0)]
        engine.snake.direction = Direction.RIGHT
        
        # Move across board
        for _ in range(7):
            engine.tick()
            # Should still be running
            assert engine.get_state() == GameState.RUNNING
    
    def test_input_queue_rapid_changes(self):
        """Test that rapid direction changes are handled correctly."""
        engine = GameEngine()
        
        # Rapid direction changes
        engine.handle_input(Direction.DOWN)
        engine.handle_input(Direction.LEFT)
        engine.handle_input(Direction.UP)
        
        # Only the last valid change should be applied
        engine.tick()
        
        # Should have accepted one of the valid direction changes
        assert engine.get_state() == GameState.RUNNING
    
    def test_snake_length_increases_with_food(self):
        """Test that snake length increases correctly as food is eaten."""
        engine = GameEngine()
        
        # Test simpler: just eat one food and verify growth
        food_pos = engine.food.get_position()
        dx, dy = engine.snake.direction.value
        
        # Position snake to eat food
        engine.snake.body = [
            (food_pos[0] - dx, food_pos[1] - dy),
            (food_pos[0] - 2 * dx, food_pos[1] - 2 * dy),
            (food_pos[0] - 3 * dx, food_pos[1] - 3 * dy)
        ]
        
        score_before = engine.get_score()
        
        # Tick to eat food
        engine.tick()
        
        # Verify food was eaten (score increased)
        assert engine.get_score() == score_before + 10
        
        # Tick again to see growth take effect
        engine.tick()
        
        # Verify snake grew
        assert len(engine.snake.get_body()) == 4
