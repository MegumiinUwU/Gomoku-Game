import numpy as np
from board import Board
from eval_fn import evaluation_state

def get_opponent(color):
    return Board.WHITE if color == Board.BLACK else Board.BLACK


def get_best_move(state, depth, ai_color, use_alphabeta=True):
    """
    Get the best move for the AI
    
    Args:
        state: Current board state
        depth: Search depth
        ai_color: AI player's color
        use_alphabeta: Whether to use alpha-beta pruning (default: True)
        
    Returns:
        tuple: (best_move, best_value)
    """
    values = np.array(state.board)
    best_value = -float('inf')
    best_move = (-1, -1)
    pieces = np.count_nonzero(values != Board.EMPTY)

    if pieces == 0:
        return first_move(state)
    if pieces == 1:
        return second_move(state)

    top_moves = get_top_moves(state, 10, ai_color)

    for move_n_value in top_moves:
        move = move_n_value[0]
        if use_alphabeta:
            value = alphaBetaPruning(state.next(move), -float('inf'), float('inf'), depth - 1, ai_color)
        else:
            value = minimax(state.next(move), depth - 1, ai_color)
            
        if value > best_value:
            best_value = value
            best_move = move

    if best_move[0] == -1 and best_move[1] == -1:
        return top_moves[0]

    return best_move, best_value


def get_top_moves(state, n, ai_color):
    top_moves = []
    for move in state.get_valid_moves():
        next_state = state.copy()
        next_state.make_move(*move)
        evaluation = evaluation_state(next_state, ai_color)
        top_moves.append((move, evaluation))
    return sorted(top_moves, key=lambda x: x[1], reverse=True)[:n]


def alphaBetaPruning(state, alpha, beta, depth, ai_color):
    if depth == 0 or state.game_over:
        return evaluation_state(state, ai_color)

    maximizing = (state.current_player == ai_color)
    if maximizing:
        value = -float('inf')
        for move in state.get_valid_moves():
            next_state = state.copy()
            next_state.make_move(*move)
            value = max(value, alphaBetaPruning(next_state, alpha, beta, depth - 1, ai_color))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for move in state.get_valid_moves():
            next_state = state.copy()
            next_state.make_move(*move)
            value = min(value, alphaBetaPruning(next_state, alpha, beta, depth - 1, ai_color))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def minimax(state, depth, ai_color):
    """
    Minimax algorithm without alpha-beta pruning
    """
    if depth == 0 or state.game_over:
        return evaluation_state(state, ai_color)

    maximizing = (state.current_player == ai_color)
    
    if maximizing:
        # Maximizing player's turn
        value = -float('inf')
        for move in state.get_valid_moves():
            next_state = state.copy()
            next_state.make_move(*move)
            value = max(value, minimax(next_state, depth - 1, ai_color))
        return value
    else:
        # Minimizing player's turn
        value = float('inf')
        for move in state.get_valid_moves():
            next_state = state.copy()
            next_state.make_move(*move)
            value = min(value, minimax(next_state, depth - 1, ai_color))
        return value


def first_move(state):
    x = state.size // 2
    return (np.random.choice([x - 1, x, x + 1]), np.random.choice([x - 1, x, x + 1])), 1


def second_move(state):
    i, j = state.last_move
    size = state.size
    i2 = 1 if i <= size // 2 else -1
    j2 = 1 if j <= size // 2 else -1
    return (i + i2, j + j2), 2
