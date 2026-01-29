"""Renderer class for displaying game state to terminal."""

import sys
from typing import TYPE_CHECKING
from .types import GameState

if TYPE_CHECKING:
    from .game_engine import GameEngine


# ANSI color codes
class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'


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
    
    def render(self, engine: 'GameEngine', high_score: int = 0) -> None:
        """Render the current game state.
        
        Args:
            engine: The game engine containing state to render
            high_score: The high score to display
        """
        self.clear_screen()
        
        # Display score and high score
        print(f"Score: {engine.get_score():<10}High Score: {high_score}")
        print()
        
        # Check if paused
        if engine.get_state() == GameState.PAUSED:
            self._render_paused(engine, high_score)
            return
        
        # Get game state
        board = engine.board
        snake_body = set(engine.snake.get_body())
        snake_head = engine.snake.get_head_position()
        food_pos = engine.food.get_position()
        
        # Draw top border (blue)
        print(f"{Colors.BLUE}╔" + "═" * board.width + f"╗{Colors.RESET}")
        
        # Draw board
        for y in range(board.height):
            print(f"{Colors.BLUE}║{Colors.RESET}", end="")
            for x in range(board.width):
                pos = (x, y)
                if pos == snake_head:
                    print(f"{Colors.GREEN}@{Colors.RESET}", end="")
                elif pos in snake_body:
                    print(f"{Colors.GREEN}○{Colors.RESET}", end="")
                elif pos == food_pos:
                    print(f"{Colors.RED}•{Colors.RESET}", end="")
                else:
                    print(" ", end="")
            print(f"{Colors.BLUE}║{Colors.RESET}")
        
        # Draw bottom border (blue)
        print(f"{Colors.BLUE}╚" + "═" * board.width + f"╝{Colors.RESET}")
        
        # Display controls
        print(f"\nControls: Arrow Keys or WASD | {Colors.YELLOW}P: Pause{Colors.RESET} | Q: Quit")
    
    def _render_paused(self, engine: 'GameEngine', high_score: int) -> None:
        """Render the paused game state.
        
        Args:
            engine: The game engine containing state to render
            high_score: The high score to display
        """
        # Get game state
        board = engine.board
        snake_body = set(engine.snake.get_body())
        snake_head = engine.snake.get_head_position()
        food_pos = engine.food.get_position()
        
        # Draw top border (blue)
        print(f"{Colors.BLUE}╔" + "═" * board.width + f"╗{Colors.RESET}")
        
        # Draw board with dimmed colors
        for y in range(board.height):
            print(f"{Colors.BLUE}║{Colors.RESET}", end="")
            for x in range(board.width):
                pos = (x, y)
                if pos == snake_head:
                    print(f"{Colors.GREEN}@{Colors.RESET}", end="")
                elif pos in snake_body:
                    print(f"{Colors.GREEN}○{Colors.RESET}", end="")
                elif pos == food_pos:
                    print(f"{Colors.RED}•{Colors.RESET}", end="")
                else:
                    print(" ", end="")
            print(f"{Colors.BLUE}║{Colors.RESET}")
        
        # Draw bottom border (blue)
        print(f"{Colors.BLUE}╚" + "═" * board.width + f"╝{Colors.RESET}")
        
        # Display PAUSED message
        print(f"\n{Colors.YELLOW}{Colors.BOLD}        *** PAUSED ***{Colors.RESET}")
        print(f"\nControls: {Colors.YELLOW}P: Resume{Colors.RESET} | Q: Quit")
    
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
