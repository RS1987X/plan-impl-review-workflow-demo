"""Main entry point for the Snake Game."""

import sys
import time
from snake_game.game_engine import GameEngine
from snake_game.input_handler import InputHandler
from snake_game.renderer import Renderer
from snake_game.types import GameState, Difficulty
from snake_game.high_score import HighScoreManager


def select_difficulty() -> Difficulty:
    """Prompt user to select difficulty level.
    
    Returns:
        Selected Difficulty
    """
    print("=" * 40)
    print("       SNAKE GAME - Select Difficulty")
    print("=" * 40)
    print("\n1. Easy   (Slower speed)")
    print("2. Medium (Normal speed)")
    print("3. Hard   (Faster speed)")
    print("\nEnter your choice (1-3) or press Enter for Medium: ", end="", flush=True)
    
    choice = input().strip()
    
    if choice == '1':
        return Difficulty.EASY
    elif choice == '3':
        return Difficulty.HARD
    else:
        return Difficulty.MEDIUM


def wait_for_input(timeout=0.1):
    """Wait for keyboard input with platform-specific handling.
    
    Args:
        timeout: Maximum time to wait in seconds
        
    Returns:
        Input character or None
    """
    try:
        import select
        # Unix-like systems
        if select.select([sys.stdin], [], [], timeout)[0]:
            return sys.stdin.read(1)
    except (ImportError, OSError):
        # Windows or non-Unix systems - use basic approach
        # Note: This is a simplified version for the game to run
        pass
    return None


def main():
    """Run the snake game."""
    # Select difficulty level
    difficulty = select_difficulty()
    
    # Initialize game components
    engine = GameEngine()
    input_handler = InputHandler()
    renderer = Renderer()
    high_score_manager = HighScoreManager()
    
    # Configure terminal
    input_handler.configure_terminal()
    
    try:
        # Game loop
        running = True
        tick_rate = difficulty.get_tick_rate()
        tick_duration = 1.0 / tick_rate
        
        while running:
            start_time = time.time()
            
            if engine.get_state() == GameState.RUNNING:
                # Process input
                direction = input_handler.get_input()
                if direction:
                    engine.handle_input(direction)
                
                # Check for pause input
                char = wait_for_input(0)
                if char:
                    if input_handler.should_quit(char):
                        running = False
                        break
                    elif input_handler.should_pause(char):
                        engine.toggle_pause()
                
                # Update game state
                engine.tick()
                
                # Render
                renderer.render(engine, high_score_manager.get_high_score())
                
            elif engine.get_state() == GameState.PAUSED:
                # Render paused state
                renderer.render(engine, high_score_manager.get_high_score())
                
                # Wait for unpause or quit
                char = wait_for_input(0.1)
                if char:
                    if input_handler.should_quit(char):
                        running = False
                        break
                    elif input_handler.should_pause(char):
                        engine.toggle_pause()
                
            elif engine.get_state() == GameState.GAME_OVER:
                # Save high score
                high_score_manager.save(engine.get_score())
                
                # Display game over screen
                renderer.display_game_over(engine.get_score())
                
                # Wait for restart or quit
                while engine.get_state() == GameState.GAME_OVER:
                    # Check for input using helper function
                    char = wait_for_input(0.1)
                    if char:
                        if input_handler.should_quit(char):
                            running = False
                            break
                        elif input_handler.should_restart(char):
                            engine.restart()
                            break
            
            # Maintain tick rate
            elapsed = time.time() - start_time
            if elapsed < tick_duration:
                time.sleep(tick_duration - elapsed)
    
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        pass
    
    finally:
        # Restore terminal
        input_handler.restore_terminal()
        renderer.clear_screen()
        print("Thanks for playing!")
        print(f"High Score: {high_score_manager.get_high_score()}")


if __name__ == "__main__":
    main()
