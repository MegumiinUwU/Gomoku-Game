import customtkinter as ctk
import os
from PIL import Image
from customtkinter import CTkImage

# Keep global references to prevent garbage collection
_images = {}

def create_main_menu(root, show_game_callback):
    """
    Create the main menu UI
    
    Args:
        root: The root CTk window
        show_game_callback: Function to call to transition to the game
    """
    global _images
    
    # Set the window title
    root.title("Gomoku - Main Menu")
    
    # Calculate window dimensions
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    
    # Load background image
    assets_dir = os.path.join(os.path.dirname(__file__), 'Assets')
    bg2_path = os.path.join(assets_dir, 'Background1.png')
    
    # Load the image once
    bg_img = Image.open(bg2_path).convert('RGBA').resize((window_width, window_height), Image.LANCZOS)
    # Apply transparency
    alpha = bg_img.split()[3]
    alpha = alpha.point(lambda p: int(p * 0.8))
    bg_img.putalpha(alpha)
    
    # Create CTkImage (proper way for CustomTkinter)
    ctk_bg_img = CTkImage(light_image=bg_img, dark_image=bg_img, size=(window_width-80, window_height-80))
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

    # Button callbacks
    def start_human_vs_human():
        show_game_callback("human_vs_human")
        
    def show_ai_vs_human_menu():
        create_ai_selection_menu(root, show_game_callback, "human")
        
    def show_ai_vs_ai_menu():
        create_ai_selection_menu(root, show_game_callback, "ai")

    # Create buttons
    btn1 = ctk.CTkButton(menu_frame, text="Human vs Human", font=btn_font, height=50, 
                         fg_color=btn_fg, hover_color=btn_hover, text_color="black", 
                         command=start_human_vs_human)
    btn1.pack(fill="x", padx=40, pady=10)

    btn2 = ctk.CTkButton(menu_frame, text="AI vs Human", font=btn_font, height=50, 
                         fg_color=btn_fg, hover_color=btn_hover, text_color="black", 
                         command=show_ai_vs_human_menu, state="normal")
    btn2.pack(fill="x", padx=40, pady=10)

    btn3 = ctk.CTkButton(menu_frame, text="AI vs AI", font=btn_font, height=50, 
                         fg_color=btn_fg, hover_color=btn_hover, text_color="black", 
                         command=show_ai_vs_ai_menu, state="normal")
    btn3.pack(fill="x", padx=40, pady=10)

def create_ai_selection_menu(root, show_game_callback, opponent_type):
    """
    Create a menu for selecting AI algorithm
    
    Args:
        root: The root CTk window
        show_game_callback: Function to call to transition to the game
        opponent_type: Type of opponent (human or ai)
    """
    global _images
    
    # First, clear the window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Set the window title
    root.title("Gomoku - AI Selection")
    
    # Calculate window dimensions
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    
    # Use the same background image from main menu if it exists, or load it
    if 'bg_img' not in _images or 'ctk_bg_img' not in _images:
        # Load background image
        assets_dir = os.path.join(os.path.dirname(__file__), 'Assets')
        bg2_path = os.path.join(assets_dir, 'Background1.png')
        
        # Load the image once
        bg_img = Image.open(bg2_path).convert('RGBA').resize((window_width, window_height), Image.LANCZOS)
        # Apply transparency
        alpha = bg_img.split()[3]
        alpha = alpha.point(lambda p: int(p * 0.8))
        bg_img.putalpha(alpha)
        
        # Create CTkImage
        ctk_bg_img = CTkImage(light_image=bg_img, dark_image=bg_img, size=(window_width-80, window_height-80))
        # Store reference
        _images['bg_img'] = bg_img
        _images['ctk_bg_img'] = ctk_bg_img
    else:
        ctk_bg_img = _images['ctk_bg_img']
    
    # Create a frame to hold everything
    main_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="transparent")
    main_frame.pack(fill="both", expand=True)
    
    # Create a label for the background with CTkImage
    bg_label = ctk.CTkLabel(main_frame, text="", image=ctk_bg_img, fg_color="#0a1026")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Main frame for menu
    menu_frame = ctk.CTkFrame(main_frame, fg_color="#181c2b", corner_radius=18, width=400, height=450)
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Different title based on mode
    if opponent_type == "human":
        title_text = "Select AI Algorithm"
    else:
        title_text = "Select AI Matchup"
        
    title_label = ctk.CTkLabel(menu_frame, text=title_text, font=("Arial", 26, "bold"), text_color="#FFD700")
    title_label.pack(pady=(30, 20))

    btn_font = ("Arial", 18, "bold")
    btn_fg = "#00eaff"
    btn_hover = "#00b8d4"

    # Button callbacks
    def start_with_minmax():
        if opponent_type == "human":
            show_game_callback("ai_vs_human_minmax")
        else:
            # This case would be for AI vs AI
            show_game_callback("ai_vs_ai_minmax")
        
    def start_with_alphabeta():
        if opponent_type == "human":
            show_game_callback("ai_vs_human")  # Default AI uses alpha-beta
        else:
            # This case would be for AI vs AI
            show_game_callback("ai_vs_ai")  # Default AI vs AI uses alpha-beta
    
    def return_to_main_menu():
        # Instead of calling create_main_menu directly, use the same pattern as in GomokuApp
        # First clear the window
        for widget in root.winfo_children():
            widget.destroy()
        
        # Then call create_main_menu
        create_main_menu(root, show_game_callback)

    # Create buttons with text depending on mode
    if opponent_type == "human":
        btn1_text = "Human vs MiniMax"
        btn2_text = "Human vs Alpha-Beta"
    else:
        btn1_text = "MiniMax vs Alpha-Beta"
        btn2_text = "Alpha-Beta vs Alpha-Beta"
    
    # Create buttons
    btn1 = ctk.CTkButton(menu_frame, text=btn1_text, font=btn_font, height=50, 
                         fg_color=btn_fg, hover_color=btn_hover, text_color="black", 
                         command=start_with_minmax)
    btn1.pack(fill="x", padx=40, pady=10)

    btn2 = ctk.CTkButton(menu_frame, text=btn2_text, font=btn_font, height=50, 
                         fg_color=btn_fg, hover_color=btn_hover, text_color="black", 
                         command=start_with_alphabeta)
    btn2.pack(fill="x", padx=40, pady=10)
    
    # Back button
    back_btn = ctk.CTkButton(menu_frame, text="Back to Main Menu", font=btn_font, height=50, 
                         fg_color="#FFD700", hover_color="#FFC000", text_color="black", 
                         command=return_to_main_menu)
    back_btn.pack(fill="x", padx=40, pady=(20, 10))

# For backward compatibility
def main_menu():
    print("WARNING: This function is deprecated. Use create_main_menu instead.")
    root = ctk.CTk()
    create_main_menu(root, lambda mode: print(f"Game mode selected: {mode}"))
    root.mainloop()

if __name__ == "__main__":
    print("WARNING: main_menu.py should not be run directly!")
    main_menu()