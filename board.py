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
        self.is_draw = False
        self.moves_history = []
        self.winning_stones = []  # Track winning stones
        self.move_count = 0  # Counter for total moves made
    
    def reset(self):
        """Reset the board to initial state."""
        self.board = [[self.EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = self.BLACK
        self.last_move = None
        self.game_over = False
        self.winner = None
        self.is_draw = False
        self.moves_history = []
        self.winning_stones = []  # Reset winning stones
        self.move_count = 0  # Reset move counter
    
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
        self.move_count += 1  # Increment move counter
        
        # Check if the game is over
        if self.check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
            return True
        
        # Check for draw - if all 196 positions (14x14 grid) are filled
        if self.move_count >= 196:  # 14x14 playable grid
            self.game_over = True
            self.is_draw = True
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
        for row in range(1, 15):  
            for col in range(1, 15):  
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
        self.is_draw = False
        self.move_count -= 1  # Decrement move counter
        
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
        
    def copy(self):
        """Return a deep copy of the board state for AI search."""
        import copy
        new_board = Board(self.size)
        new_board.board = copy.deepcopy(self.board)
        new_board.current_player = self.current_player
        new_board.last_move = self.last_move if self.last_move is None else tuple(self.last_move)
        new_board.game_over = self.game_over
        new_board.winner = self.winner
        new_board.is_draw = self.is_draw
        new_board.moves_history = list(self.moves_history)
        new_board.winning_stones = list(self.winning_stones)
        new_board.move_count = self.move_count
        return new_board

    def next(self, move):
        """Return a new Board with the move applied (for AI search)."""
        new_board = self.copy()
        new_board.make_move(*move)
        return new_board 