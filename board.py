class Board:
    """
    Gomoku Board class that handles game logic. 
    This will be used by GUI and can later be used by AI.
    """
    
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    
    def __init__(self, size=15):
        """
        Initialize the board with the given size.
        
        Args:
            size (int): Size of the board (default: 15x15)
        """
        self.size = size
        self.board = [[self.EMPTY for _ in range(size)] for _ in range(size)]
        self.current_player = self.BLACK
        self.last_move = None
        self.game_over = False
        self.winner = None
        self.moves_history = []
        self.winning_stones = []  # Track winning stones
    
    def reset(self):
        """Reset the board to initial state."""
        self.board = [[self.EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = self.BLACK
        self.last_move = None
        self.game_over = False
        self.winner = None
        self.moves_history = []
        self.winning_stones = []  # Reset winning stones
    
    def make_move(self, row, col):
        """
        Make a move on the board.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        # Check if the move is valid
        if not self.is_valid_move(row, col):
            return False
            
        # Make the move
        self.board[row][col] = self.current_player
        self.last_move = (row, col)
        self.moves_history.append((row, col, self.current_player))
        
        # Check if the game is over
        if self.check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
            return True
            
        # Switch player
        self.current_player = self.WHITE if self.current_player == self.BLACK else self.BLACK
        return True
    
    def is_valid_move(self, row, col):
        """
        Check if the move is valid.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            bool: True if move is valid, False otherwise
        """
        # Check if the game is already over
        if self.game_over:
            return False
            
        # Check if the position is within the board
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
            
        # Check if the position is empty
        return self.board[row][col] == self.EMPTY
    
    def check_win(self, row, col):
        """
        Check if the last move made at (row, col) wins the game.
        
        Args:
            row (int): Row index of the last move
            col (int): Column index of the last move
            
        Returns:
            bool: True if the player wins, False otherwise
        """
        player = self.board[row][col]
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)], # Diagonal \
            [(1, -1), (-1, 1)]  # Diagonal /
        ]
        
        for direction_pair in directions:
            count = 1  # Start with 1 for the current stone
            stones = [(row, col)]  # Track stones in this direction
            
            # Check both directions
            for dr, dc in direction_pair:
                r, c = row, col
                while True:
                    r += dr
                    c += dc
                    if not (0 <= r < self.size and 0 <= c < self.size) or self.board[r][c] != player:
                        break
                    count += 1
                    stones.append((r, c))
            
            if count >= 5:
                self.winning_stones = stones
                return True
                
        return False
    
    def get_valid_moves(self):
        """
        Get all valid moves.
        
        Returns:
            list: List of (row, col) tuples for all valid moves
        """
        if self.game_over:
            return []
            
        valid_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == self.EMPTY:
                    valid_moves.append((row, col))
                    
        return valid_moves
    
    def undo_move(self):
        """
        Undo the last move.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.moves_history:
            return False
            
        row, col, player = self.moves_history.pop()
        self.board[row][col] = self.EMPTY
        self.current_player = player
        self.game_over = False
        self.winner = None
        
        if self.moves_history:
            self.last_move = (self.moves_history[-1][0], self.moves_history[-1][1])
        else:
            self.last_move = None
            
        return True
    
    def get_board_state(self):
        """
        Get the current board state.
        
        Returns:
            list: 2D list representing the board
        """
        return [row[:] for row in self.board]
    
    def get_current_player(self):
        """
        Get the current player.
        
        Returns:
            int: Current player (BLACK or WHITE)
        """
        return self.current_player 