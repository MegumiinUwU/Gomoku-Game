import customtkinter as ctk
import os
from PIL import Image
from customtkinter import CTkImage
import sys

# Keep global references to prevent garbage collection
_images = {}

def main_menu(root=None):
    global _images
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Check if there's already a root window
    if root is None:
        root = ctk.CTk()
        new_window = True
    else:
        # This is likely a callback from the game, use existing root
        new_window = False
        
        # Clear any existing widgets
        for widget in root.winfo_children():
            widget.destroy()
            
    root.title("Gomoku - Main Menu")
    window_width = 1180
    window_height = 650
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)

    # Load background image
    assets_dir = os.path.join(os.path.dirname(__file__), 'Assets')
    bg2_path = os.path.join(assets_dir, 'Background1.png')
    
    # Load the image once
    bg_img = Image.open(bg2_path).convert('RGBA').resize((window_width, window_height), Image.LANCZOS)
    # Apply transparency
    alpha = bg_img.split()[3]
    alpha = alpha.point(lambda p: int(p * 0.6))
    bg_img.putalpha(alpha)
    
    # Create CTkImage (proper way for CustomTkinter)
    ctk_bg_img = CTkImage(light_image=bg_img, dark_image=bg_img, size=(window_width, window_height))
    # Store reference to prevent garbage collection
    _images['bg_img'] = bg_img
    _images['ctk_bg_img'] = ctk_bg_img
    
    # Create a frame to hold everything - use corner_radius=0 for full coverage
    main_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="transparent")
    main_frame.pack(fill="both", expand=True)
    
    # Create a label for the background with CTkImage
    bg_label = ctk.CTkLabel(main_frame, text="", image=ctk_bg_img, fg_color="#0a1026")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover entire frame
    
    # Main frame for menu
    menu_frame = ctk.CTkFrame(main_frame, fg_color="#181c2b", corner_radius=18, width=400, height=350)
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = ctk.CTkLabel(menu_frame, text="GOMOKU", font=("Arial", 32, "bold"), text_color="#FFD700")
    title_label.pack(pady=(30, 20))

    btn_font = ("Arial", 18, "bold")
    btn_fg = "#00eaff"
    btn_hover = "#00b8d4"

    def fade_and_transition_to_game(game_mode="human_vs_human"):
        """Smooth transition to game with fade effect while keeping the window open"""
        # Simple transition by hiding the menu and loading the game
        def start_game():
            # Clear everything from root window
            for widget in root.winfo_children():
                widget.destroy()
                
            # Load the game in the same window
            load_game(game_mode)
        
        def load_game(mode):
            # Change the window title
            root.title("Gomoku - Game")
            
            if mode == "human_vs_human":
                # Import here to avoid circular imports
                from gui import GomokuGUI
                # Create the game in the existing window
                game = GomokuGUI(root)
            elif mode == "ai_vs_human":
                # Future implementation
                pass
            elif mode == "ai_vs_ai":
                # Future implementation
                pass
        
        # Schedule the transition with a slight delay for visual feedback
        menu_frame.update()
        root.after(100, start_game)

    btn1 = ctk.CTkButton(menu_frame, text="Human vs Human", font=btn_font, height=50, 
                         fg_color=btn_fg, hover_color=btn_hover, text_color="black", 
                         command=lambda: fade_and_transition_to_game("human_vs_human"))
    btn1.pack(fill="x", padx=40, pady=10)

    btn2 = ctk.CTkButton(menu_frame, text="AI vs Human", font=btn_font, height=50, 
                         fg_color=btn_fg, hover_color=btn_hover, text_color="black", 
                         command=lambda: fade_and_transition_to_game("ai_vs_human"), state="normal")
    btn2.pack(fill="x", padx=40, pady=10)

    btn3 = ctk.CTkButton(menu_frame, text="AI vs AI", font=btn_font, height=50, 
                         fg_color=btn_fg, hover_color=btn_hover, text_color="black", 
                         command=lambda: fade_and_transition_to_game("ai_vs_ai"), state="normal")
    btn3.pack(fill="x", padx=40, pady=10)

    # Only start mainloop if this is a new window
    if new_window:
        root.mainloop()

if __name__ == "__main__":
    main_menu()