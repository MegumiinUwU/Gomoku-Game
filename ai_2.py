import numpy as np
import time
from board import Board
from eval_fn import evaluation_state

def get_opponent(color):
    return Board.WHITE if color == Board.BLACK else Board.BLACK

# Use a transposition table to avoid recalculating positions
transposition_table = {}

def get_best_move(state, depth, ai_color, use_alphabeta=True):
    """
    Get the best move for the AI with iterative deepening
    
    Args:
        state: Current board state
        depth: Maximum search depth
        ai_color: AI player's color
        use_alphabeta: Whether to use alpha-beta pruning (default: True)
        
    Returns:
        tuple: (best_move, best_value)
    """
    # Reset move counter for this search
    global moves_calculated
    moves_calculated = 0
    
    pieces = sum(1 for row in state.board for cell in row if cell != Board.EMPTY)
    
    # Early game optimizations
    if pieces == 0:
        return first_move(state)
    if pieces == 1:
        return second_move(state)
    
    # Clear transposition table for a new search
    transposition_table.clear()
    
    best_move = None
    best_value = -float('inf')
    
    # Get candidate moves ordered by initial evaluation
    candidate_moves = get_top_moves(state, 10, ai_color)
    
    # No valid moves case
    if not candidate_moves:
        return (-1, -1), -float('inf')
    
    # Initialize with the first move
    best_move = candidate_moves[0][0]
    
    # Start timing logic
    start_time = time.time()
    time_limit = 5  # seconds
    
    # Start with depth=1 and increase until target depth
    for current_depth in range(1, depth + 1):            
        temp_best_move = None
        temp_best_value = -float('inf')
        depth_moves_calculated = 0  # Counter for moves at this depth
        
        # Search each candidate move
        for move, _ in candidate_moves:
            # Check time limit before evaluating each move
            if time.time() - start_time > time_limit:
                print(f"Time limit reached at depth {current_depth}")
                print(f"Total positions evaluated before timeout: {moves_calculated + depth_moves_calculated}")
                # Use the best move found at this depth if it's better than the previous best
                if temp_best_value > best_value:
                    return temp_best_move, temp_best_value
                else:
                    return best_move, best_value
            
            # Use in-place make_move/undo_move instead of deep copy
            state.make_move(*move)
            move_counter = MoveCounter()
            if use_alphabeta:
                value = alphaBetaPruning(state, -float('inf'), float('inf'), 
                                       current_depth - 1, ai_color, move_counter)
            else:
                value = minimax(state, current_depth - 1, ai_color, move_counter)
            state.undo_move()
            
            depth_moves_calculated += move_counter.count
            
            if value > temp_best_value:
                temp_best_value = value
                temp_best_move = move
        
        # Update best move with completed depth results
        best_value = temp_best_value
        best_move = temp_best_move
        
        # Print information about this depth
        print(f"Depth {current_depth}: Evaluated {depth_moves_calculated} positions")
        moves_calculated += depth_moves_calculated
        
        # Re-order candidate moves based on current evaluation
        candidate_moves = get_top_moves(state, 10, ai_color)
    
    # Print total moves calculated for this turn
    print(f"Total positions evaluated: {moves_calculated}")
    return best_move, best_value

class MoveCounter:
    """Simple class to track move count"""
    def __init__(self):
        self.count = 0
        
    def increment(self):
        self.count += 1

def get_state_hash(state):
    """Generate a hashable representation of the board state"""
    board_tuple = tuple(map(tuple, state.board))
    return (board_tuple, state.current_player)

def get_top_moves(state, n, ai_color):
    """Get the top n moves based on immediate evaluation (in-place)"""
    top_moves = []
    for move in state.get_valid_moves():
        state.make_move(*move)
        evaluation = evaluation_state(state, ai_color)
        state.undo_move()
        top_moves.append((move, evaluation))
    return sorted(top_moves, key=lambda x: x[1], reverse=True)[:n]

def alphaBetaPruning(state, alpha, beta, depth, ai_color, move_counter):
    """Alpha-beta pruning with transposition table (in-place, using make_move/undo_move)"""
    move_counter.increment()

    if depth == 0 or state.game_over:
        return evaluation_state(state, ai_color)

    state_hash = get_state_hash(state)
    if state_hash in transposition_table and transposition_table[state_hash][0] >= depth:
        return transposition_table[state_hash][1]

    maximizing = (state.current_player == ai_color)
    moves = state.get_valid_moves()
    if len(moves) > 5:
        move_values = []
        for move in moves:
            state.make_move(*move)
            move_values.append((move, evaluation_state(state, ai_color)))
            state.undo_move()
        if maximizing:
            moves = [m[0] for m in sorted(move_values, key=lambda x: x[1], reverse=True)]
        else:
            moves = [m[0] for m in sorted(move_values, key=lambda x: x[1])]

    if maximizing:
        value = -float('inf')
        for move in moves:
            state.make_move(*move)
            child_value = alphaBetaPruning(state, alpha, beta, depth - 1, ai_color, move_counter)
            state.undo_move()
            value = max(value, child_value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
    else:
        value = float('inf')
        for move in moves:
            state.make_move(*move)
            child_value = alphaBetaPruning(state, alpha, beta, depth - 1, ai_color, move_counter)
            state.undo_move()
            value = min(value, child_value)
            beta = min(beta, value)
            if alpha >= beta:
                break

    transposition_table[state_hash] = (depth, value)
    return value

def minimax(state, depth, ai_color, move_counter):
    """
    Minimax algorithm without alpha-beta pruning (in-place, using make_move/undo_move)
    """
    # Increment move counter
    move_counter.increment()

    if depth == 0 or state.game_over:
        return evaluation_state(state, ai_color)

    maximizing = (state.current_player == ai_color)

    if maximizing:
        value = -float('inf')
        for move in state.get_valid_moves():
            state.make_move(*move)
            value = max(value, minimax(state, depth - 1, ai_color, move_counter))
            state.undo_move()
        return value
    else:
        value = float('inf')
        for move in state.get_valid_moves():
            state.make_move(*move)
            value = min(value, minimax(state, depth - 1, ai_color, move_counter))
            state.undo_move()
        return value

def first_move(state):
    """Optimized first move function"""
    x = state.size // 2
    return (np.random.choice([x - 1, x, x + 1]), np.random.choice([x - 1, x, x + 1])), 1

def second_move(state):
    """Optimized second move function"""
    i, j = state.last_move
    size = state.size
    i2 = 1 if i <= size // 2 else -1
    j2 = 1 if j <= size // 2 else -1
    return (i + i2, j + j2), 2

# Initialize global counter
moves_calculated = 0