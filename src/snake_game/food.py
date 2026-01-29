"""Food class for managing food spawning and position."""

import random
from typing import Optional, TYPE_CHECKING
from .types import Position

if TYPE_CHECKING:
    from .game_board import GameBoard
    from .snake import Snake


class Food:
    """Manages food position and spawning logic."""
    
    def __init__(self):
        """Initialize food with no position."""
        self._position: Optional[Position] = None
    
    def get_position(self) -> Optional[Position]:
        """Get the current food position.
        
        Returns:
            Current food position or None if not spawned
        """
        return self._position
    
    def spawn(self, board: 'GameBoard', snake: 'Snake') -> None:
        """Spawn food at a random valid empty position.
        
        Args:
            board: The game board
            snake: The snake (to avoid placing food on it)
            
        Raises:
            RuntimeError: If no valid position is available (board full)
        """
        # Get all valid positions on the board
        all_positions = [
            (x, y)
            for x in range(board.width)
            for y in range(board.height)
        ]
        
        # Filter out positions occupied by snake
        snake_positions = set(snake.get_body())
        valid_positions = [
            pos for pos in all_positions 
            if pos not in snake_positions
        ]
        
        # Check if any valid position exists
        if not valid_positions:
            raise RuntimeError("No valid position for food spawn - board is full!")
        
        # Randomly select a position
        self._position = random.choice(valid_positions)
