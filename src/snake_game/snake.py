"""Snake class for managing snake state and behavior."""

from typing import List
from .types import Direction, Position


class Snake:
    """Manages snake state including body segments, direction, and movement."""
    
    def __init__(self, start_position: Position, initial_length: int = 3, 
                 initial_direction: Direction = Direction.RIGHT):
        """Initialize the snake.
        
        Args:
            start_position: Starting position (head) of the snake
            initial_length: Initial length of the snake (default: 3)
            initial_direction: Initial movement direction (default: RIGHT)
        """
        self.direction = initial_direction
        
        # Create body segments starting from head position
        # Body grows backwards from head in opposite direction
        dx, dy = initial_direction.value
        self.body: List[Position] = [
            (start_position[0] - i * dx, start_position[1] - i * dy)
            for i in range(initial_length)
        ]
        
        self._grow_pending = False
    
    def get_head_position(self) -> Position:
        """Get the position of the snake's head.
        
        Returns:
            Position of the head (first segment)
        """
        return self.body[0]
    
    def get_body(self) -> List[Position]:
        """Get all body segment positions.
        
        Returns:
            List of positions representing the snake body
        """
        return self.body.copy()
    
    def move(self, new_direction: Direction) -> None:
        """Move the snake one step in the given direction.
        
        Args:
            new_direction: Direction to move (validated against reversal)
        """
        # Prevent reversing direction
        if new_direction != self.direction.opposite():
            self.direction = new_direction
        
        # Calculate new head position
        dx, dy = self.direction.value
        head_x, head_y = self.get_head_position()
        new_head = (head_x + dx, head_y + dy)
        
        # Add new head
        self.body.insert(0, new_head)
        
        # Remove tail unless growth is pending
        if not self._grow_pending:
            self.body.pop()
        else:
            self._grow_pending = False
    
    def grow(self) -> None:
        """Mark snake to grow by one segment on next move."""
        self._grow_pending = True
    
    def collides_with_self(self) -> bool:
        """Check if the head collides with any body segment.
        
        Returns:
            True if head position overlaps with body, False otherwise
        """
        head = self.get_head_position()
        return head in self.body[1:]  # Check against body (excluding head)
