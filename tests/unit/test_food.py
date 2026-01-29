"""Unit tests for the Food class."""

import pytest
from src.snake_game.food import Food
from src.snake_game.game_board import GameBoard
from src.snake_game.snake import Snake
from src.snake_game.types import Direction


class TestFood:
    """Test suite for Food class."""
    
    def test_food_initialization(self):
        """Test food initializes with no position."""
        food = Food()
        
        assert food.get_position() is None
    
    def test_food_spawn_valid_position(self):
        """Test that food spawns at a valid position."""
        board = GameBoard(20, 20)
        snake = Snake((10, 10), initial_length=3)
        food = Food()
        
        food.spawn(board, snake)
        pos = food.get_position()
        
        assert pos is not None
        assert board.is_valid_position(pos[0], pos[1])
    
    def test_food_spawn_avoids_snake(self):
        """Test that food doesn't spawn on snake body."""
        board = GameBoard(20, 20)
        snake = Snake((10, 10), initial_length=3)
        food = Food()
        
        snake_positions = set(snake.get_body())
        
        # Spawn food multiple times to check randomness
        for _ in range(10):
            food.spawn(board, snake)
            pos = food.get_position()
            
            assert pos not in snake_positions
    
    def test_food_spawn_randomness(self):
        """Test that food spawns at different positions (statistical test)."""
        board = GameBoard(20, 20)
        snake = Snake((10, 10), initial_length=3)
        
        positions = set()
        for _ in range(20):
            food = Food()
            food.spawn(board, snake)
            positions.add(food.get_position())
        
        # Should have multiple different positions (very high probability)
        assert len(positions) > 5
    
    def test_food_spawn_small_board(self):
        """Test food spawning on a small board."""
        board = GameBoard(5, 5)
        snake = Snake((2, 2), initial_length=3, initial_direction=Direction.RIGHT)
        food = Food()
        
        food.spawn(board, snake)
        pos = food.get_position()
        
        assert pos is not None
        assert board.is_valid_position(pos[0], pos[1])
        assert pos not in snake.get_body()
    
    def test_food_spawn_no_valid_position(self):
        """Test that RuntimeError is raised when board is full."""
        # Create a very small board
        board = GameBoard(2, 2)
        # Create a snake that fills the entire board
        snake = Snake((0, 0), initial_length=1)
        
        # Manually fill the snake to cover all positions
        snake.body = [(0, 0), (1, 0), (0, 1), (1, 1)]
        
        food = Food()
        
        with pytest.raises(RuntimeError, match="No valid position"):
            food.spawn(board, snake)
    
    def test_food_get_position_after_spawn(self):
        """Test getting food position after spawning."""
        board = GameBoard(20, 20)
        snake = Snake((10, 10), initial_length=3)
        food = Food()
        
        food.spawn(board, snake)
        pos1 = food.get_position()
        pos2 = food.get_position()
        
        # Position should remain consistent
        assert pos1 == pos2
    
    def test_food_respawn_changes_position(self):
        """Test that respawning can change food position."""
        board = GameBoard(20, 20)
        snake = Snake((10, 10), initial_length=3)
        food = Food()
        
        food.spawn(board, snake)
        pos1 = food.get_position()
        
        # Respawn multiple times
        different_position_found = False
        for _ in range(20):
            food.spawn(board, snake)
            pos2 = food.get_position()
            if pos1 != pos2:
                different_position_found = True
                break
        
        # Should find a different position at some point
        assert different_position_found
