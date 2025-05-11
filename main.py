#!/usr/bin/env python3

"""
Gomoku Game
A traditional board game where players take turns placing stones on a grid with
the goal of getting five stones in a row (horizontally, vertically, or diagonally).
"""

import sys
import customtkinter as ctk
import os
from PIL import Image
from customtkinter import CTkImage

# Global variables to keep track of application state
_images = {}  # For storing image references
_current_frame = None  # Currently active frame

class GomokuApp:
    def __init__(self):
        # Set up the main application window
        self.root = ctk.CTk()
        self.root.title("Gomoku")
        self.window_width = 1180
        self.window_height = 650
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(False, False)
        
        # Set appearance theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Show the main menu first
        self.show_main_menu()
        
    def clear_window(self):
        """Clear all widgets from the root window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        """Show the main menu screen"""
        # First clear the window
        self.clear_window()
        
        # Then import and create the main menu
        from main_menu import create_main_menu
        create_main_menu(self.root, self.show_game)
    
    def show_game(self, game_mode="human_vs_human"):
        """Show the game screen"""
        # First clear the window
        self.clear_window()
        
        # Then import and create the game UI
        from gui import create_game_ui
        create_game_ui(self.root, self.show_main_menu, game_mode)
    
    def run(self):
        """Start the main application loop"""
        self.root.mainloop()

if __name__ == "__main__":
    # Create and run the application
    app = GomokuApp()
    app.run() 