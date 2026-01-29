"""High score persistence module."""

import os
import json
from pathlib import Path


class HighScoreManager:
    """Manages high score persistence to file."""
    
    def __init__(self, filename: str = ".snake_high_score.json"):
        """Initialize the high score manager.
        
        Args:
            filename: Name of the file to store high score (default: .snake_high_score.json)
        """
        # Store high score in user's home directory
        self.filepath = Path.home() / filename
        self.high_score = 0
        self.load()
    
    def load(self) -> int:
        """Load high score from file.
        
        Returns:
            The loaded high score, or 0 if file doesn't exist or error occurs
        """
        try:
            if self.filepath.exists():
                with open(self.filepath, 'r') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
        except (json.JSONDecodeError, IOError, OSError) as e:
            # Log warning but continue - don't crash the game
            print(f"Warning: Could not load high score: {e}")
            self.high_score = 0
        
        return self.high_score
    
    def save(self, score: int) -> None:
        """Save high score to file if it's higher than current high score.
        
        Args:
            score: The score to potentially save
        """
        if score > self.high_score:
            self.high_score = score
            try:
                with open(self.filepath, 'w') as f:
                    json.dump({'high_score': self.high_score}, f)
            except (IOError, OSError) as e:
                # Log warning but continue - don't crash the game
                print(f"Warning: Could not save high score: {e}")
    
    def get_high_score(self) -> int:
        """Get the current high score.
        
        Returns:
            Current high score
        """
        return self.high_score
