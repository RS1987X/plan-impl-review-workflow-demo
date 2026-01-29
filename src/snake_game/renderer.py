"""Renderer class for displaying game state to terminal."""

import sys
from typing import TYPE_CHECKING
from .types import GameState

if TYPE_CHECKING:
    from .game_engine import GameEngine


class Renderer:
    """Handles rendering of game state to the terminal."""
    
    def __init__(self):
        """Initialize the renderer."""
        pass
    
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        # ANSI escape code to clear screen and move cursor to home
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()
    
    def render(self, engine: 'GameEngine') -> None:
        """Render the current game state.
        
        Args:
            engine: The game engine containing state to render
        """
        self.clear_screen()
        
        # Display score
        print(f"Score: {engine.get_score()}\n")
        
        # Get game state
        board = engine.board
        snake_body = set(engine.snake.get_body())
        snake_head = engine.snake.get_head_position()
        food_pos = engine.food.get_position()
        
        # Draw top border
        print("╔" + "═" * board.width + "╗")
        
        # Draw board
        for y in range(board.height):
            print("║", end="")
            for x in range(board.width):
                pos = (x, y)
                if pos == snake_head:
                    print("@", end="")
                elif pos in snake_body:
                    print("○", end="")
                elif pos == food_pos:
                    print("•", end="")
                else:
                    print(" ", end="")
            print("║")
        
        # Draw bottom border
        print("╚" + "═" * board.width + "╝")
        
        # Display controls
        print("\nControls: Arrow Keys or WASD | Q: Quit")
    
    def display_game_over(self, score: int) -> None:
        """Display game over screen.
        
        Args:
            score: Final score to display
        """
        self.clear_screen()
        print("\n" + "=" * 40)
        print(" " * 15 + "GAME OVER")
        print("=" * 40)
        print(f"\n{'Final Score:':>20} {score}")
        print("\n" + "=" * 40)
        print("\nPress R to restart or Q to quit")
        sys.stdout.flush()
