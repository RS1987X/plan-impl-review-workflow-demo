"""Type definitions for the Snake Game."""

from enum import Enum
from typing import Tuple

# Type alias for position coordinates
Position = Tuple[int, int]


class Direction(Enum):
    """Enumeration for movement directions."""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def opposite(self) -> 'Direction':
        """Return the opposite direction."""
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        return opposites[self]


class GameState(Enum):
    """Enumeration for game states."""
    RUNNING = "running"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"
