"""Unit tests for Phase 2 features: pause, difficulty, high score."""

import pytest
import os
import tempfile
from pathlib import Path
from src.snake_game.game_engine import GameEngine
from src.snake_game.types import GameState, Difficulty
from src.snake_game.high_score import HighScoreManager


class TestPauseFunctionality:
    """Test suite for pause/unpause functionality."""
    
    def test_pause_changes_state(self):
        """Test that pause changes state from RUNNING to PAUSED."""
        engine = GameEngine()
        assert engine.get_state() == GameState.RUNNING
        
        engine.pause()
        
        assert engine.get_state() == GameState.PAUSED
    
    def test_unpause_changes_state(self):
        """Test that unpause changes state from PAUSED to RUNNING."""
        engine = GameEngine()
        engine.pause()
        assert engine.get_state() == GameState.PAUSED
        
        engine.unpause()
        
        assert engine.get_state() == GameState.RUNNING
    
    def test_toggle_pause_from_running(self):
        """Test toggle_pause changes state from RUNNING to PAUSED."""
        engine = GameEngine()
        assert engine.get_state() == GameState.RUNNING
        
        engine.toggle_pause()
        
        assert engine.get_state() == GameState.PAUSED
    
    def test_toggle_pause_from_paused(self):
        """Test toggle_pause changes state from PAUSED to RUNNING."""
        engine = GameEngine()
        engine.pause()
        assert engine.get_state() == GameState.PAUSED
        
        engine.toggle_pause()
        
        assert engine.get_state() == GameState.RUNNING
    
    def test_tick_does_not_update_when_paused(self):
        """Test that tick does not move snake when paused."""
        engine = GameEngine()
        engine.pause()
        
        initial_head = engine.snake.get_head_position()
        engine.tick()
        
        # Snake should not have moved
        assert engine.snake.get_head_position() == initial_head
    
    def test_pause_does_not_affect_game_over_state(self):
        """Test that pause does not change game over state."""
        engine = GameEngine()
        engine.state = GameState.GAME_OVER
        
        engine.pause()
        
        assert engine.get_state() == GameState.GAME_OVER
    
    def test_unpause_does_not_affect_running_state(self):
        """Test that unpause does not affect already running state."""
        engine = GameEngine()
        assert engine.get_state() == GameState.RUNNING
        
        engine.unpause()
        
        assert engine.get_state() == GameState.RUNNING


class TestDifficultyLevels:
    """Test suite for difficulty level functionality."""
    
    def test_easy_difficulty_tick_rate(self):
        """Test that EASY difficulty has correct tick rate."""
        assert Difficulty.EASY.get_tick_rate() == 8
    
    def test_medium_difficulty_tick_rate(self):
        """Test that MEDIUM difficulty has correct tick rate."""
        assert Difficulty.MEDIUM.get_tick_rate() == 12
    
    def test_hard_difficulty_tick_rate(self):
        """Test that HARD difficulty has correct tick rate."""
        assert Difficulty.HARD.get_tick_rate() == 16
    
    def test_difficulty_enum_values(self):
        """Test that difficulty enum has all expected values."""
        assert Difficulty.EASY.value == 1
        assert Difficulty.MEDIUM.value == 2
        assert Difficulty.HARD.value == 3
    
    def test_difficulty_ordering(self):
        """Test that difficulty levels have increasing tick rates."""
        easy_rate = Difficulty.EASY.get_tick_rate()
        medium_rate = Difficulty.MEDIUM.get_tick_rate()
        hard_rate = Difficulty.HARD.get_tick_rate()
        
        assert easy_rate < medium_rate < hard_rate


class TestHighScorePersistence:
    """Test suite for high score persistence functionality."""
    
    def setup_method(self):
        """Set up test fixtures before each test."""
        # Use a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.test_filename = Path(self.temp_file.name).name
    
    def teardown_method(self):
        """Clean up test fixtures after each test."""
        # Remove temporary file
        try:
            os.unlink(self.temp_file.name)
        except FileNotFoundError:
            pass
    
    def test_high_score_manager_initialization(self):
        """Test that HighScoreManager initializes with zero score."""
        manager = HighScoreManager(filename=self.test_filename)
        assert manager.get_high_score() == 0
    
    def test_save_high_score(self):
        """Test saving a high score."""
        manager = HighScoreManager(filename=self.test_filename)
        
        manager.save(100)
        
        assert manager.get_high_score() == 100
    
    def test_save_higher_score_updates(self):
        """Test that saving a higher score updates the high score."""
        manager = HighScoreManager(filename=self.test_filename)
        manager.save(100)
        
        manager.save(150)
        
        assert manager.get_high_score() == 150
    
    def test_save_lower_score_does_not_update(self):
        """Test that saving a lower score does not update the high score."""
        manager = HighScoreManager(filename=self.test_filename)
        manager.save(100)
        
        manager.save(50)
        
        assert manager.get_high_score() == 100
    
    def test_load_high_score_from_file(self):
        """Test loading high score from file."""
        # Save a high score
        manager1 = HighScoreManager(filename=self.test_filename)
        manager1.save(200)
        
        # Create new manager and verify it loads the high score
        manager2 = HighScoreManager(filename=self.test_filename)
        
        assert manager2.get_high_score() == 200
    
    def test_load_nonexistent_file(self):
        """Test loading from nonexistent file returns 0."""
        # Use a filename that doesn't exist
        manager = HighScoreManager(filename='nonexistent_test_file_12345.json')
        
        assert manager.get_high_score() == 0
    
    def test_high_score_persists_across_instances(self):
        """Test that high score persists across manager instances."""
        manager1 = HighScoreManager(filename=self.test_filename)
        manager1.save(300)
        
        manager2 = HighScoreManager(filename=self.test_filename)
        manager2.save(250)  # Lower score should not update
        
        assert manager2.get_high_score() == 300
    
    def test_multiple_saves_keep_highest(self):
        """Test multiple saves keep the highest score."""
        manager = HighScoreManager(filename=self.test_filename)
        
        manager.save(50)
        manager.save(150)
        manager.save(100)
        manager.save(200)
        manager.save(75)
        
        assert manager.get_high_score() == 200


class TestInputHandlerPause:
    """Test suite for InputHandler pause detection."""
    
    def test_should_pause_lowercase_p(self):
        """Test that should_pause returns True for lowercase 'p'."""
        from src.snake_game.input_handler import InputHandler
        handler = InputHandler()
        
        assert handler.should_pause('p') is True
    
    def test_should_pause_uppercase_p(self):
        """Test that should_pause returns True for uppercase 'P'."""
        from src.snake_game.input_handler import InputHandler
        handler = InputHandler()
        
        assert handler.should_pause('P') is True
    
    def test_should_pause_other_keys(self):
        """Test that should_pause returns False for other keys."""
        from src.snake_game.input_handler import InputHandler
        handler = InputHandler()
        
        assert handler.should_pause('q') is False
        assert handler.should_pause('r') is False
        assert handler.should_pause('w') is False
        assert handler.should_pause('a') is False
