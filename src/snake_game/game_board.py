"""GameBoard class for managing the game grid."""

from typing import Tuple
from .types import Position


class GameBoard:
    """Manages the game board grid and boundary validation."""
    
    def __init__(self, width: int = 20, height: int = 20):
        """Initialize the game board with specified dimensions.
        
        Args:
            width: Board width in cells (default: 20)
            height: Board height in cells (default: 20)
        """
        self.width = width
        self.height = height
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if a position is within board boundaries.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_dimensions(self) -> Tuple[int, int]:
        """Get the board dimensions.
        
        Returns:
            Tuple of (width, height)
        """
        return (self.width, self.height)
