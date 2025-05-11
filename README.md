# To Do

- [x] Fix that main window closes when transferring to other window (not smooth UI)
- [x] Fix the image on main menu
- [x] Make the AI algorithms
- [ ] Test all






# Gomoku Game

A classic board game where players take turns placing stones on a grid, aiming to be the first to form an unbroken chain of five stones horizontally, vertically, or diagonally.



## Requirements

- Python 3.6+
- CustomTkinter 5.2.1+
- packaging 
- pillow

## Installation

1. Clone or download this repository.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:

```bash
python main.py
```

2. Game Rules:
   - Black always plays first
   - Players take turns placing stones on intersections of the grid
   - The first player to form an unbroken row of five stones wins
   - No moves can be made after a player has won

## Controls

- Click on the board to place a stone
- Use the "New Game" button to reset the game
- Use the "Undo Move" button to take back the last move
- Use the "Main Menu" button to return to the main menu

## Recent Fixes

- Fixed window transition between main menu and game screens
- Fixed image handling to prevent TkInter errors
- Improved UI consistency and performance

## License

This project is open source and available under the MIT License. 