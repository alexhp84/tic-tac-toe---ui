# Tic-Tac-Toe with Marvin 🤖
A terminal Tic-Tac-Toe game featuring Marvin the Paranoid Android as the computer opponent, with various easter eggs and HHGTG references.
UI based version  in development

## What it does
- Offers two player modes - human vs human or human vs Marvin
- The first player chooses to go first or second
- Score tracking across multiple games
- Enter 42 during a game to reset the board without losing scores
- Reach a score of 42 for a surprise 🐟

## Requirements
- Python 3.x

## How to run

### Windows
1. Install Python from https://www.python.org/downloads/
2. Make sure to check "Add Python to PATH" during installation
3. Open Command Prompt and navigate to the project folder
```bash
cd path\to\tic-tac-toe
python tic-tac-toe.py
```

### Mac
1. Python 3 can be installed via https://www.python.org/downloads/ or Homebrew
```bash
brew install python3
```
2. Open Terminal and navigate to the project folder
```bash
cd path/to/tic-tac-toe
python3 tic-tac-toe.py
```

### Linux
1. Python 3 is usually pre-installed, if not:
```bash
sudo apt install python3
```
2. Navigate to the project folder
```bash
cd path/to/tic-tac-toe
python3 tic-tac-toe.py
```

## How to play
- Enter your name when prompted
- Choose your opponent and who goes first
    - If human v human, player 2 also provides their name
- Select squares 1-9 on your turn
- Enter the answer to the Ultimate Question to reset the current game
- Enter Y or N when asked to play again

## Notes
- Player 1 is always ❌, Player 2 is always ⭕
- Marvin will attempt to win or block before making a random move
- Scores reset when you exit the game

## Author
[alexhp84](https://github.com/alexhp84)
