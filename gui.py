import customtkinter as ctk
from board import Board
import math
from PIL import Image, ImageTk
from customtkinter import CTkImage
import os

# Keep global references to prevent garbage collection
_images = {}

class GomokuGUI:
    """
    GUI for Gomoku game using CustomTkinter
    """
    
    def __init__(self, root, board_size=16, cell_size=45):
        """
        Initialize the GUI.
        
        Args:
            root: CustomTkinter root window
            board_size (int): Size of the board
            cell_size (int): Size of each cell in pixels
        """
        global _images
        self.root = root
        self.root.title("Gomoku")
        
        # Make sure the root window is clear from any previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.board = Board(15)  # Only 15x15 playable
        self.cell_size = cell_size
        self.canvas_size = cell_size * board_size + 110
        self.margin = 30
        
        # Load player stone images FIRST
        assets_dir = os.path.join(os.path.dirname(__file__), 'Assets')
        p1_path = os.path.join(assets_dir, 'Player1.png')
        p2_path = os.path.join(assets_dir, 'Player2.png')
        img_size = cell_size - 6
        
        # Load and process images, storing in global dictionary
        player1_img = Image.open(p1_path).resize((img_size, img_size), Image.LANCZOS)
        player2_img = Image.open(p2_path).resize((img_size, img_size), Image.LANCZOS)
        
        _images['player1_img'] = player1_img
        _images['player2_img'] = player2_img
        
        # Create CTk images
        self.tk_player1_img = CTkImage(light_image=player1_img, size=(img_size, img_size))
        self.tk_player2_img = CTkImage(light_image=player2_img, size=(img_size, img_size))
        
        # Create Tk images for canvas
        self.tk_player1_img_canvas = ImageTk.PhotoImage(player1_img)
        self.tk_player2_img_canvas = ImageTk.PhotoImage(player2_img)
        
        # Store CTk images
        _images['tk_player1_img'] = self.tk_player1_img
        _images['tk_player2_img'] = self.tk_player2_img
        _images['tk_player1_img_canvas'] = self.tk_player1_img_canvas
        _images['tk_player2_img_canvas'] = self.tk_player2_img_canvas
        
        # Load and process background image
        bg2_path = os.path.join(assets_dir, 'Background2.png')
        bg_img = Image.open(bg2_path).convert('RGBA').resize((self.canvas_size, self.canvas_size), Image.LANCZOS)
        # Decrease opacity to 60%
        alpha = bg_img.split()[3]
        alpha = alpha.point(lambda p: int(p * 0.6))
        bg_img.putalpha(alpha)
        self.bg_img_canvas = ImageTk.PhotoImage(bg_img)
        
        # Store background image
        _images['bg_img'] = bg_img
        _images['bg_img_canvas'] = self.bg_img_canvas
        
        # Set up the color theme
        ctk.set_appearance_mode("dark")  # Options: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")
        
        # Create frames
        self.create_frames()
        
        # Style control frame for neon look
        self.control_frame.configure(
            fg_color="#181c2b",  # dark, semi-transparent
            corner_radius=18
        )
        
        # Create canvas for board
        self.create_board_canvas()
        
        # Create side panel with controls
        self.create_control_panel()
        
        # Draw the initial board
        self.draw_board()
        
    def create_frames(self):
        """Create main frames for the UI"""
        # Main frame with two columns (takes up the entire window)
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#0a1026", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)
        
        # Layout frames for board and controls
        self.board_frame = ctk.CTkFrame(self.main_frame, fg_color="#0a1026", corner_radius=0)
        self.board_frame.pack(side="left", fill="both", padx=10, pady=10)
        
        # Right frame for controls
        self.control_frame = ctk.CTkFrame(self.main_frame, fg_color="#181c2b", corner_radius=18)
        self.control_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
    def create_board_canvas(self):
        """Create the canvas for drawing the board"""
        self.canvas = ctk.CTkCanvas(
            self.board_frame, 
            width=self.canvas_size, 
            height=self.canvas_size,
            bg="#0a1026",  # Neon dark blue background
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Bind click event to canvas
        self.canvas.bind("<Button-1>", self.handle_click)
        
    def create_control_panel(self):
        """Create control panel with game information and buttons"""
        # Game info
        self.info_frame = ctk.CTkFrame(self.control_frame, fg_color="#181c2b")
        self.info_frame.pack(fill="x", padx=10, pady=10)
        
        # Player turn label and image
        self.turn_frame = ctk.CTkFrame(self.info_frame, fg_color="#181c2b")
        self.turn_frame.pack(pady=(10, 0))
        
        self.turn_label = ctk.CTkLabel(
            self.turn_frame, 
            text="Player 1", 
            font=("Arial", 16, "bold"),
            text_color="#fff"
        )
        self.turn_label.pack(side="left", padx=(0, 8))
        
        self.turn_img_label = ctk.CTkLabel(self.turn_frame, text="")
        self.turn_img_label.pack(side="left")
        
        self.status_label = ctk.CTkLabel(
            self.info_frame, 
            text="Player 1's Turn",
            font=("Arial", 14),
            text_color="#00eaff"
        )
        self.status_label.pack(pady=(0, 10))
        
        # Control buttons
        self.button_frame = ctk.CTkFrame(self.control_frame, fg_color="#181c2b")
        self.button_frame.pack(fill="x", padx=10, pady=10)
        
        self.reset_button = ctk.CTkButton(
            self.button_frame,
            text="New Game",
            command=self.reset_game,
            font=("Arial", 14, "bold"),
            height=40,
            fg_color="#00eaff",
            hover_color="#00b8d4",
            text_color="black"
        )
        self.reset_button.pack(fill="x", pady=5)
        
        self.undo_button = ctk.CTkButton(
            self.button_frame,
            text="Undo Move",
            command=self.undo_move,
            font=("Arial", 14, "bold"),
            height=40,
            fg_color="#00eaff",
            hover_color="#00b8d4",
            text_color="black"
        )
        self.undo_button.pack(fill="x", pady=5)
        
        # Add Main Menu button
        self.menu_button = ctk.CTkButton(
            self.button_frame,
            text="Main Menu",
            command=self.return_to_menu,
            font=("Arial", 14, "bold"),
            height=40,
            fg_color="#FFD700",  # Gold color
            hover_color="#FFC000",
            text_color="black"
        )
        self.menu_button.pack(fill="x", pady=5)
        
    def return_to_menu(self):
        """Return to the main menu with smooth transition"""
        # Similar to how the main menu transitions to the game, use a smooth transition
        def go_to_menu():
            # Import here to avoid circular imports
            from main_menu import main_menu
            
            # Clear all widgets from the root window
            for widget in self.root.winfo_children():
                widget.destroy()
                
            # Call main_menu with the existing root window
            main_menu(root=self.root)
        
        # Schedule the transition with a slight delay for visual feedback
        self.root.after(100, go_to_menu)
        
    def draw_board(self):
        """Draw the board with grid lines and stones"""
        self.canvas.delete("all")
        # Draw background image
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_img_canvas)
        # Draw neon border
        border_color = "#FFD700"  # neon gold
        border_width = 10  # thicker for glow
        self.canvas.create_rectangle(
            self.margin - border_width//2, self.margin - border_width//2,
            self.margin + 15 * self.cell_size + border_width//2,
            self.margin + 15 * self.cell_size + border_width//2,
            outline=border_color, width=border_width
        )
        # Draw 16x16 grid lines in neon orange
        grid_color = "#FFB300"  # neon orange
        for i in range(16):
            # Horizontal
            self.canvas.create_line(
                self.margin, 
                self.margin + i * self.cell_size,
                self.margin + 15 * self.cell_size,
                self.margin + i * self.cell_size,
                width=2, fill=grid_color
            )
            # Vertical
            self.canvas.create_line(
                self.margin + i * self.cell_size,
                self.margin,
                self.margin + i * self.cell_size,
                self.margin + 15 * self.cell_size,
                width=2, fill=grid_color
            )
        # Draw star points (for 15x15 board)
        if self.board.size == 15:
            star_points = [(3, 3), (3, 7), (3, 11), 
                          (7, 3), (7, 7), (7, 11),
                          (11, 3), (11, 7), (11, 11)]
        else:
            star_points = []
        for row, col in star_points:
            x = self.margin + col * self.cell_size
            y = self.margin + row * self.cell_size
            radius = 7
            self.canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                fill="#8b5c2a", outline="#8b5c2a"  # saddle brown
            )
        # Draw stones only in 1-15 (inner 15x15)
        for row in range(1, 15):
            for col in range(1, 15):
                stone = self.board.board[row][col]
                if stone != Board.EMPTY:
                    self.draw_stone(row, col, stone)
        # Highlight winning stones if game is over
        if self.board.game_over and self.board.winning_stones:
            for row, col in self.board.winning_stones:
                x = self.margin + col * self.cell_size
                y = self.margin + row * self.cell_size
                radius = self.cell_size // 2 - 8
                self.canvas.create_oval(
                    x - radius - 2, y - radius - 2,
                    x + radius + 2, y + radius + 2,
                    outline="#ff00cc",
                    width=2
                )
        self.update_status()
        self.update_turn_indicator()
    
    def draw_stone(self, row, col, stone):
        """Draw a stone on the board using player images"""
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        # Center the image
        if stone == Board.BLACK:
            self.canvas.create_image(x, y, image=self.tk_player1_img_canvas)
        else:
            self.canvas.create_image(x, y, image=self.tk_player2_img_canvas)
    
    def update_status(self):
        """Update the status label based on game state"""
        if self.board.game_over:
            if self.board.winner == Board.BLACK:
                self.status_label.configure(text="Player 1 Wins!")
            else:
                self.status_label.configure(text="Player 2 Wins!")
        else:
            if self.board.current_player == Board.BLACK:
                self.status_label.configure(text="Player 1's Turn")
            else:
                self.status_label.configure(text="Player 2's Turn")
    
    def handle_click(self, event):
        """Handle click event on canvas"""
        if self.board.game_over:
            return
        col = round((event.x - self.margin) / self.cell_size)
        row = round((event.y - self.margin) / self.cell_size)
        # Only allow play in 1-14 (inner 15x15)
        if 1 <= row < 15 and 1 <= col < 15:
            if self.board.make_move(row, col):
                self.draw_board()
    
    def reset_game(self):
        """Reset the game"""
        self.board.reset()
        self.draw_board()
        self.update_turn_indicator()
    
    def undo_move(self):
        """Undo the last move"""
        if self.board.undo_move():
            self.draw_board()
            self.update_turn_indicator()
    
    def update_turn_indicator(self):
        """Update the turn label and image to show Player 1/2 and their stone image"""
        if self.board.current_player == Board.BLACK:
            self.turn_label.configure(text="Player 1")
            self.turn_img_label.configure(image=self.tk_player1_img)
            self.turn_img_label.image = self.tk_player1_img
        else:
            self.turn_label.configure(text="Player 2")
            self.turn_img_label.configure(image=self.tk_player2_img)
            self.turn_img_label.image = self.tk_player2_img