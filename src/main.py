"""Main entry point for the Snake Game."""

import sys
import time
import select
from snake_game.game_engine import GameEngine
from snake_game.input_handler import InputHandler
from snake_game.renderer import Renderer
from snake_game.types import GameState


def main():
    """Run the snake game."""
    # Initialize game components
    engine = GameEngine()
    input_handler = InputHandler()
    renderer = Renderer()
    
    # Configure terminal
    input_handler.configure_terminal()
    
    try:
        # Game loop
        running = True
        tick_rate = 10  # 10 ticks per second
        tick_duration = 1.0 / tick_rate
        
        while running:
            start_time = time.time()
            
            if engine.get_state() == GameState.RUNNING:
                # Process input
                direction = input_handler.get_input()
                if direction:
                    engine.handle_input(direction)
                
                # Update game state
                engine.tick()
                
                # Render
                renderer.render(engine)
                
            elif engine.get_state() == GameState.GAME_OVER:
                # Display game over screen
                renderer.display_game_over(engine.get_score())
                
                # Wait for restart or quit
                while engine.get_state() == GameState.GAME_OVER:
                    # Check for input
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        char = sys.stdin.read(1)
                        if char in ('q', 'Q', '\x1b'):  # Quit
                            running = False
                            break
                        elif char in ('r', 'R'):  # Restart
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


if __name__ == "__main__":
    main()
