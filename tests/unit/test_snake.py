"""Unit tests for the Snake class."""

import pytest
from src.snake_game.snake import Snake
from src.snake_game.types import Direction


class TestSnake:
    """Test suite for Snake class."""
    
    def test_snake_initial_state(self):
        """Test snake initialization with correct position, length, and direction."""
        snake = Snake((10, 10), initial_length=3, initial_direction=Direction.RIGHT)
        
        assert snake.get_head_position() == (10, 10)
        assert len(snake.get_body()) == 3
        assert snake.direction == Direction.RIGHT
        
        # Body should extend backwards from head
        body = snake.get_body()
        assert body[0] == (10, 10)  # Head
        assert body[1] == (9, 10)   # Body segment 1
        assert body[2] == (8, 10)   # Body segment 2
    
    def test_snake_movement_right(self):
        """Test snake movement to the right."""
        snake = Snake((10, 10), initial_length=3, initial_direction=Direction.RIGHT)
        snake.move(Direction.RIGHT)
        
        assert snake.get_head_position() == (11, 10)
        assert len(snake.get_body()) == 3  # Length unchanged without growth
    
    def test_snake_movement_up(self):
        """Test snake movement upward."""
        snake = Snake((10, 10), initial_length=3, initial_direction=Direction.RIGHT)
        snake.move(Direction.UP)
        
        assert snake.get_head_position() == (10, 9)
    
    def test_snake_movement_down(self):
        """Test snake movement downward."""
        snake = Snake((10, 10), initial_length=3, initial_direction=Direction.RIGHT)
        snake.move(Direction.DOWN)
        
        assert snake.get_head_position() == (10, 11)
    
    def test_snake_movement_left(self):
        """Test snake movement to the left."""
        snake = Snake((10, 10), initial_length=3, initial_direction=Direction.UP)
        snake.move(Direction.LEFT)
        
        assert snake.get_head_position() == (9, 10)
    
    def test_snake_growth(self):
        """Test snake growth mechanism."""
        snake = Snake((10, 10), initial_length=3, initial_direction=Direction.RIGHT)
        initial_length = len(snake.get_body())
        
        snake.grow()
        snake.move(Direction.RIGHT)
        
        assert len(snake.get_body()) == initial_length + 1
    
    def test_snake_multiple_growth(self):
        """Test multiple consecutive growths."""
        snake = Snake((10, 10), initial_length=3, initial_direction=Direction.RIGHT)
        
        for i in range(3):
            snake.grow()
            snake.move(Direction.RIGHT)
        
        assert len(snake.get_body()) == 6  # Initial 3 + 3 growth
    
    def test_snake_self_collision_detection(self):
        """Test self-collision detection."""
        snake = Snake((10, 10), initial_length=4, initial_direction=Direction.RIGHT)
        
        # Move in a pattern that causes self-collision
        snake.move(Direction.RIGHT)
        snake.grow()
        snake.move(Direction.RIGHT)
        snake.grow()
        snake.move(Direction.DOWN)
        snake.grow()
        snake.move(Direction.LEFT)
        snake.grow()
        snake.move(Direction.LEFT)
        snake.grow()
        snake.move(Direction.UP)  # Should collide with body
        
        assert snake.collides_with_self()
    
    def test_snake_no_self_collision_initially(self):
        """Test that snake doesn't collide with itself initially."""
        snake = Snake((10, 10), initial_length=3, initial_direction=Direction.RIGHT)
        
        assert not snake.collides_with_self()
    
    def test_snake_direction_reversal_prevention(self):
        """Test that snake cannot reverse direction."""
        snake = Snake((10, 10), initial_length=3, initial_direction=Direction.RIGHT)
        
        # Try to reverse from RIGHT to LEFT
        snake.move(Direction.LEFT)
        
        # Should still be moving RIGHT
        assert snake.direction == Direction.RIGHT
        assert snake.get_head_position() == (11, 10)  # Moved right, not left
    
    def test_snake_direction_change_allowed(self):
        """Test that snake can change to non-opposite directions."""
        snake = Snake((10, 10), initial_length=3, initial_direction=Direction.RIGHT)
        
        # Change to UP (perpendicular, should work)
        snake.move(Direction.UP)
        
        assert snake.direction == Direction.UP
        assert snake.get_head_position() == (10, 9)
    
    def test_snake_body_follows_head(self):
        """Test that body segments follow the head correctly."""
        snake = Snake((10, 10), initial_length=3, initial_direction=Direction.RIGHT)
        initial_body = snake.get_body()
        
        snake.move(Direction.RIGHT)
        new_body = snake.get_body()
        
        # New head should be at old head + direction
        assert new_body[0] == (11, 10)
        # Second segment should be at old head position
        assert new_body[1] == initial_body[0]
