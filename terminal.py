import numpy as np
from board import Board
from ai import get_best_move
import os
import time

class GomokuTerminal:
    def __init__(self):
        self.board = Board(15)
        self.game_mode = None
        self.ai_depth = 2
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_board(self):
        """Print the board with coordinates"""
        print("\n   " + " ".join(f"{i:2}" for i in range(15)))
        
        for row in range(15):
            print(f"{row:2} ", end="")
            for col in range(15):
                cell = self.board.board[row][col]
                if cell == Board.BLACK:
                    print(" X ", end="")
                elif cell == Board.WHITE:
                    print(" O ", end="")
                else:
                    print(" _ ", end="")
            print()
    
    def get_human_move(self):
        """Get valid move input from human player"""
        while True:
            try:
                move = input("Enter your move as 'row col' (0-14): ").strip().split()
                if len(move) != 2:
                    print("Please enter exactly two numbers separated by space")
                    continue
                    
                row, col = map(int, move)
                if 0 <= row <= 14 and 0 <= col <= 14:
                    # Convert to 0-based internal coordinates
                    return row, col
                else:
                    print("Numbers must be between 0 and 14")
            except ValueError:
                print("Please enter valid numbers")
    
    def make_ai_move(self, use_alphabeta=True):
        """Make AI move using the specified algorithm"""
        print(f"\n{'Alpha-Beta' if use_alphabeta else 'MiniMax'} AI is thinking...")
        start_time = time.time()
        
        move, _ = get_best_move(
            self.board, 
            self.ai_depth, 
            self.board.current_player, 
            use_alphabeta
        )
        
        think_time = time.time() - start_time
        print(f"AI placed at {move[0]}, {move[1]} (took {think_time:.1f}s)")
        self.board.make_move(*move)
    
    def select_game_mode(self):
        """Let user select game mode"""
        self.clear_screen()
        print("GOMOKU - Terminal Version")
        print("\nSelect game mode:")
        print("1. Human vs MiniMax AI")
        print("2. Human vs Alpha-Beta AI")
        print("3. MiniMax AI vs Alpha-Beta AI")
        
        while True:
            choice = input("Enter choice (1-3): ")
            if choice in ['1', '2', '3']:
                return int(choice)
            print("Invalid choice, please enter 1, 2 or 3")
    
    def play(self):
        """Main game loop"""
        mode = self.select_game_mode()
        
        # Game modes:
        # 1 = Human (Black) vs MiniMax (White)
        # 2 = Human (Black) vs Alpha-Beta (White)
        # 3 = MiniMax (Black) vs Alpha-Beta (White)
        
        while not self.board.game_over:
            self.clear_screen()
            self.print_board()
            
            if mode == 3:  # AI vs AI
                input("\nPress Enter for next move...")
                use_alphabeta = (self.board.current_player == Board.WHITE)
                self.make_ai_move(use_alphabeta)
                continue
                
            if (mode == 1 and self.board.current_player == Board.WHITE) or \
               (mode == 2 and self.board.current_player == Board.WHITE):
                # AI's turn
                use_alphabeta = (mode == 2)
                self.make_ai_move(use_alphabeta)
            else:
                # Human's turn
                print(f"\nYour turn ({'Black (X)' if self.board.current_player == Board.BLACK else 'White (O)'})")
                while True:
                    row, col = self.get_human_move()
                    if self.board.make_move(row, col):
                        break
                    print("Invalid move - try again")
        
        # Game over
        self.clear_screen()
        self.print_board()
        
        if self.board.is_draw:
            print("\nGame ended in a draw!")
        else:
            winner = "Black (X)" if self.board.winner == Board.BLACK else "White (O)"
            print(f"\n{winner} wins!")
        
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    game = GomokuTerminal()
    game.play()