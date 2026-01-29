"""GameEngine class for managing game state and rules."""

from .game_board import GameBoard
from .snake import Snake
from .food import Food
from .types import Direction, GameState, Position


class GameEngine:
    """Orchestrates game logic, state management, and rule enforcement."""
    
    def __init__(self, board_width: int = 20, board_height: int = 20):
        """Initialize the game engine.
        
        Args:
            board_width: Width of the game board (default: 20)
            board_height: Height of the game board (default: 20)
        """
        self.board = GameBoard(board_width, board_height)
        
        # Initialize snake at center of board
        center_x = board_width // 2
        center_y = board_height // 2
        self.snake = Snake((center_x, center_y), initial_length=3)
        
        self.food = Food()
        self.score = 0
        self.state = GameState.RUNNING
        
        # Spawn initial food
        self.food.spawn(self.board, self.snake)
    
    def tick(self) -> None:
        """Process one game update tick.
        
        This moves the snake, checks collisions, and updates game state.
        """
        if self.state != GameState.RUNNING:
            return
        
        # Move snake in current direction
        self.snake.move(self.snake.direction)
        
        # Check collisions
        self.check_collisions()
    
    def handle_input(self, direction: Direction) -> None:
        """Queue a direction change for the snake.
        
        Args:
            direction: New direction to move
        """
        if self.state == GameState.RUNNING:
            # Prevent reversing direction (checked here and also in snake.move)
            if direction != self.snake.direction.opposite():
                self.snake.direction = direction
    
    def check_collisions(self) -> None:
        """Check for all collision types and update game state accordingly."""
        head = self.snake.get_head_position()
        
        # Check wall collision
        if not self.board.is_valid_position(head[0], head[1]):
            self.state = GameState.GAME_OVER
            return
        
        # Check self collision
        if self.snake.collides_with_self():
            self.state = GameState.GAME_OVER
            return
        
        # Check food collision
        if head == self.food.get_position():
            self.score += 10
            self.snake.grow()
            
            # Spawn new food
            try:
                self.food.spawn(self.board, self.snake)
            except RuntimeError:
                # Board is full - victory condition
                self.state = GameState.GAME_OVER
    
    def get_state(self) -> GameState:
        """Get the current game state.
        
        Returns:
            Current GameState
        """
        return self.state
    
    def get_score(self) -> int:
        """Get the current score.
        
        Returns:
            Current score
        """
        return self.score
    
    def restart(self) -> None:
        """Restart the game with fresh state."""
        center_x = self.board.width // 2
        center_y = self.board.height // 2
        self.snake = Snake((center_x, center_y), initial_length=3)
        self.food = Food()
        self.score = 0
        self.state = GameState.RUNNING
        self.food.spawn(self.board, self.snake)
