import customtkinter as ctk
import os
from PIL import Image
from customtkinter import CTkImage
import sys

def start_human_vs_human():
    import gui
    gui.start_game()

def main_menu():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
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
    
    # Create a frame to hold everything
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

    def fade_out_in_and_load_game():
        alpha = 1.0
        def fade_out():
            nonlocal alpha
            alpha -= 0.08
            if alpha > 0:
                root.attributes('-alpha', alpha)
                root.after(15, fade_out)
            else:
                # Clear all widgets from root
                for widget in root.winfo_children():
                    widget.destroy()
                from gui import start_game
                start_game(root)
                fade_in()
        def fade_in():
            nonlocal alpha
            alpha += 0.08
            if alpha < 1.0:
                root.attributes('-alpha', alpha)
                root.after(15, fade_in)
            else:
                root.attributes('-alpha', 1.0)
        root.attributes('-alpha', 1.0)
        fade_out()

    btn1 = ctk.CTkButton(menu_frame, text="Human vs Human", font=btn_font, height=50, 
                         fg_color=btn_fg, hover_color=btn_hover, text_color="black", 
                         command=fade_out_in_and_load_game)
    btn1.pack(fill="x", padx=40, pady=10)

    btn2 = ctk.CTkButton(menu_frame, text="AI vs Human", font=btn_font, height=50, 
                         fg_color=btn_fg, hover_color=btn_hover, text_color="black", 
                         command=None, state="normal")
    btn2.pack(fill="x", padx=40, pady=10)

    btn3 = ctk.CTkButton(menu_frame, text="AI vs AI", font=btn_font, height=50, 
                         fg_color=btn_fg, hover_color=btn_hover, text_color="black", 
                         command=None, state="normal")
    btn3.pack(fill="x", padx=40, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_menu()