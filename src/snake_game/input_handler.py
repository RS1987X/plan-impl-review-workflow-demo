"""InputHandler class for capturing and processing user input."""

import sys
import select
from typing import Optional
from .types import Direction


class InputHandler:
    """Handles user input from keyboard."""
    
    def __init__(self):
        """Initialize the input handler."""
        self._configured = False
        self._old_settings = None
        
        # Try to import termios for Unix systems
        try:
            import termios
            import tty
            self._termios = termios
            self._tty = tty
            self._unix_terminal = True
        except ImportError:
            # Fall back for non-Unix systems
            self._unix_terminal = False
    
    def configure_terminal(self) -> None:
        """Configure terminal for raw input (Unix only)."""
        if self._unix_terminal and not self._configured:
            try:
                self._old_settings = self._termios.tcgetattr(sys.stdin)
                self._tty.setcbreak(sys.stdin.fileno())
                self._configured = True
            except Exception:
                # If configuration fails, continue without it
                pass
    
    def restore_terminal(self) -> None:
        """Restore terminal to original settings."""
        if self._unix_terminal and self._configured and self._old_settings:
            try:
                self._termios.tcsetattr(
                    sys.stdin, 
                    self._termios.TCSADRAIN, 
                    self._old_settings
                )
                self._configured = False
            except Exception:
                pass
    
    def get_input(self) -> Optional[Direction]:
        """Get user input and convert to direction.
        
        Returns:
            Direction if valid input received, None otherwise
        """
        # Check if input is available (non-blocking)
        if self._unix_terminal:
            # Use select for non-blocking input on Unix
            if select.select([sys.stdin], [], [], 0)[0]:
                char = sys.stdin.read(1)
            else:
                return None
        else:
            # For non-Unix, try to read without blocking
            try:
                import msvcrt
                if msvcrt.kbhit():
                    char = msvcrt.getch().decode('utf-8')
                else:
                    return None
            except ImportError:
                # No way to do non-blocking input
                return None
        
        # Map keys to directions
        key_map = {
            'w': Direction.UP,
            'W': Direction.UP,
            's': Direction.DOWN,
            'S': Direction.DOWN,
            'a': Direction.LEFT,
            'A': Direction.LEFT,
            'd': Direction.RIGHT,
            'D': Direction.RIGHT,
        }
        
        # Handle arrow keys (escape sequences on Unix)
        if char == '\x1b':  # ESC character
            # Read the next two characters for arrow keys
            if self._unix_terminal:
                next_chars = sys.stdin.read(2)
                if next_chars == '[A':
                    return Direction.UP
                elif next_chars == '[B':
                    return Direction.DOWN
                elif next_chars == '[C':
                    return Direction.RIGHT
                elif next_chars == '[D':
                    return Direction.LEFT
            # ESC key for quit handled in main loop
            return None
        
        return key_map.get(char)
    
    def should_quit(self, char: str) -> bool:
        """Check if user wants to quit.
        
        Args:
            char: Character to check
            
        Returns:
            True if quit key pressed
        """
        return char in ('q', 'Q', '\x1b')  # q, Q, or ESC
    
    def should_restart(self, char: str) -> bool:
        """Check if user wants to restart.
        
        Args:
            char: Character to check
            
        Returns:
            True if restart key pressed
        """
        return char in ('r', 'R')
