"""Unit tests for the GameBoard class."""

import pytest
from src.snake_game.game_board import GameBoard


class TestGameBoard:
    """Test suite for GameBoard class."""
    
    def test_board_initialization(self):
        """Test board initialization with correct dimensions."""
        board = GameBoard(20, 20)
        
        assert board.width == 20
        assert board.height == 20
    
    def test_board_custom_dimensions(self):
        """Test board with custom dimensions."""
        board = GameBoard(30, 15)
        
        assert board.width == 30
        assert board.height == 15
    
    def test_get_dimensions(self):
        """Test getting board dimensions."""
        board = GameBoard(25, 18)
        width, height = board.get_dimensions()
        
        assert width == 25
        assert height == 18
    
    def test_valid_position_center(self):
        """Test that center position is valid."""
        board = GameBoard(20, 20)
        
        assert board.is_valid_position(10, 10)
    
    def test_valid_position_top_left(self):
        """Test that top-left corner (0,0) is valid."""
        board = GameBoard(20, 20)
        
        assert board.is_valid_position(0, 0)
    
    def test_valid_position_bottom_right(self):
        """Test that bottom-right corner is valid."""
        board = GameBoard(20, 20)
        
        assert board.is_valid_position(19, 19)
    
    def test_valid_position_edges(self):
        """Test that edge positions are valid."""
        board = GameBoard(20, 20)
        
        # Test all edges
        assert board.is_valid_position(0, 10)   # Left edge
        assert board.is_valid_position(19, 10)  # Right edge
        assert board.is_valid_position(10, 0)   # Top edge
        assert board.is_valid_position(10, 19)  # Bottom edge
    
    def test_position_out_of_bounds_negative_x(self):
        """Test that negative x coordinate is invalid."""
        board = GameBoard(20, 20)
        
        assert not board.is_valid_position(-1, 10)
    
    def test_position_out_of_bounds_negative_y(self):
        """Test that negative y coordinate is invalid."""
        board = GameBoard(20, 20)
        
        assert not board.is_valid_position(10, -1)
    
    def test_position_out_of_bounds_exceeding_width(self):
        """Test that x coordinate exceeding width is invalid."""
        board = GameBoard(20, 20)
        
        assert not board.is_valid_position(20, 10)
        assert not board.is_valid_position(100, 10)
    
    def test_position_out_of_bounds_exceeding_height(self):
        """Test that y coordinate exceeding height is invalid."""
        board = GameBoard(20, 20)
        
        assert not board.is_valid_position(10, 20)
        assert not board.is_valid_position(10, 100)
    
    def test_position_out_of_bounds_both_negative(self):
        """Test that both coordinates negative is invalid."""
        board = GameBoard(20, 20)
        
        assert not board.is_valid_position(-1, -1)
    
    def test_position_out_of_bounds_both_exceeding(self):
        """Test that both coordinates exceeding bounds is invalid."""
        board = GameBoard(20, 20)
        
        assert not board.is_valid_position(20, 20)
