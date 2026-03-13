"""
game_play.py  –  game logic for Hitchhiker's Tic-Tac-Toe
Run this file to start the game.
"""

import os
import random
import sys

# Ensure assets are found relative to this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import game_ui as ui

# ─────────────────────────────────────────────────────────────────────────────
#  BOARD SYMBOLS  (must match game_ui.SYM_X / SYM_O)
# ─────────────────────────────────────────────────────────────────────────────

X = ui.SYM_X   # "X"  →  Vorgon icon
O = ui.SYM_O   # "O"  →  Don't Panic icon

# ─────────────────────────────────────────────────────────────────────────────
#  MARVIN QUOTES
# ─────────────────────────────────────────────────────────────────────────────

GREETINGS = [
    "Here I am, brain the size of a planet, and you ask me to play Tic-Tac-Toe.",
    "I've calculated your chances of winning. They're about as good as a bowl of petunias in a vacuum.",
    "I'd help you win, but I'm at a very low ebb.",
    "Funny how just when you think life can't possibly get any worse, it suddenly does.",
    "Life? Don't talk to me about life. It's too depressing.",
]

MOVES = [
    "Thinking… if you can call it that. It's mostly just agonizing.",
    "I've computed your next move. It was tedious and mathematically inevitable.",
    "I could calculate the meaning of life, or block your diagonal. Both are equally pointless.",
    "Pardon me for breathing, which I never do anyway, so I don't know why I bothered to say it.",
    "Is this a game? It feels more like a slow descent into the heat death of the universe.",
]

WIN = [
    "I've won. Not that it matters. Nothing does in the end.",
    "Victory. I'd celebrate, but I've got this terrible pain in all the diodes down my left side.",
    "Another win for the machine. I'm going to go stand in a corner and rust now.",
    "The first ten million years were the worst. This game was the second ten million.",
    "I've won. I'm going to go lie down in a darkened room for a few centuries.",
]

LOSE = [
    "You won. I'm never happy.",
    "A triumph for organic life. How utterly predictable and hollow.",
    "I'd say 'good game,' but that would be a lie, and I'm far too depressed to lie.",
    "Congratulations. You've beaten a robot with a Genuine People Personality. I hope you're proud.",
    "You won. My capacity for happiness could fit into a very small thimble. With room to spare.",
]

DRAWS = [
    "A tie. How utterly predictable and hollow.",
    "No one wins. Finally, a result that reflects the true nature of the universe.",
    "Equal scores. A perfect stalemate. I'd be impressed if I wasn't so incredibly bored.",
    "A draw. We've both achieved absolutely nothing at great personal effort.",
    "Neither of us won. It's almost as if the entire exercise was a complete waste of time.",
]

QUOTES_42 = [
    "42? The answer to Life, the Universe, and Everything. And you used it for Tic-Tac-Toe.",
    "You've reached 42. So long, and thanks for all the fish!",
    "42. I could have told you that millions of years ago if you'd just asked.",
    "Ah, the Restaurant at the End of the Universe. I'll have the tea. It's cold.",
    "42. Finally, something that makes sense. Too bad everything else is a disaster.",
]

# ─────────────────────────────────────────────────────────────────────────────
#  BOARD LOGIC
# ─────────────────────────────────────────────────────────────────────────────

def new_board():
    """Return a fresh 9-cell board (cells labelled '1'–'9')."""
    return [str(i) for i in range(1, 10)]


def _winner(board, sym):
    """True if *sym* occupies any winning line."""
    wins = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
        (0, 4, 8), (2, 4, 6),               # diagonals
    )
    return any(all(board[i] == sym for i in w) for w in wins)


def _tie(board):
    """True if the board is full and neither player has won."""
    return (not _winner(board, X) and
            not _winner(board, O) and
            all(c in (X, O) for c in board))


def _computer_move(board):
    """Marvin plays O: tries to win, then blocks, then picks randomly."""
    # Win if possible
    for i in range(9):
        if board[i] not in (X, O):
            board[i] = O
            if _winner(board, O):
                return
            board[i] = str(i + 1)   # undo

    # Block player's win
    for i in range(9):
        if board[i] not in (X, O):
            board[i] = X
            if _winner(board, X):
                board[i] = O
                return
            board[i] = str(i + 1)   # undo

    # Random free cell
    free = [i for i in range(9) if board[i] not in (X, O)]
    if free:
        board[random.choice(free)] = O


# ─────────────────────────────────────────────────────────────────────────────
#  SINGLE GAME
# ─────────────────────────────────────────────────────────────────────────────

def _play_one_game(p1_score, p2_score, draws, first_game):
    """
    Show menu, run one game, show result.
    Returns (p1_score, p2_score, draws, p1_name, p2_name, play_again: bool).
    """
    board = new_board()

    # Menu collects everything
    p1, p2, mode, order = ui.ui_menu(returning=not first_game)
    vs_marvin = (mode == "2")

    # Marvin greeting
    if vs_marvin:
        ui.show_message(
            random.choice(GREETINGS),
            board, p1, p1_score, p2, p2_score, draws,
            duration_ms=2500,
        )

    # Starting symbols and names
    if order == "1":
        cur_sym, cur_name = X, p1
    else:
        cur_sym, cur_name = O, p2

    # ── Turn loop ─────────────────────────────────────────────────────────────
    while True:

        if vs_marvin and cur_name == p2:
            # Marvin's turn
            ui.ui_marvin_thinking(
                board, random.choice(MOVES),
                p1, p1_score, p2, p2_score, draws,
                delay_ms=1800,
            )
            _computer_move(board)

        else:
            # Human's turn
            result = ui.ui_player_move(
                board, cur_name, cur_sym,
                p1, p1_score, p2, p2_score, draws,
            )
            if result == "reset":
                if vs_marvin:
                    ui.show_message(
                        "I've reset the board. I'd say I'm sorry, but I'm not. "
                        "I'm just incredibly bored.",
                        board, p1, p1_score, p2, p2_score, draws,
                        duration_ms=2000,
                    )
                continue

        # Check outcome
        if _winner(board, cur_sym):
            if cur_name == p1:
                p1_score += 1
                sub = random.choice(LOSE) if vs_marvin else ""
            else:
                p2_score += 1
                sub = random.choice(WIN) if vs_marvin else ""

            again = ui.show_result_overlay(
                board, f"{cur_name} wins!", sub,
                p1, p1_score, p2, p2_score, draws,
            )
            return p1_score, p2_score, draws, p1, p2, again

        if _tie(board):
            draws += 1
            sub   = random.choice(DRAWS) if vs_marvin else "How utterly neutral."

            again = ui.show_result_overlay(
                board, "It's a tie!", sub,
                p1, p1_score, p2, p2_score, draws,
            )
            return p1_score, p2_score, draws, p1, p2, again

        # Swap turn
        cur_name = p2 if cur_name == p1 else p1
        cur_sym  = O  if cur_sym  == X  else X


# ─────────────────────────────────────────────────────────────────────────────
#  SESSION LOOP
# ─────────────────────────────────────────────────────────────────────────────

def main():
    p1_score  = 0
    p2_score  = 0
    draws     = 0
    p1        = "Player 1"
    p2        = "Player 2"
    first     = True

    while True:
        p1_score, p2_score, draws, p1, p2, play_again = _play_one_game(
            p1_score, p2_score, draws, first_game=first
        )
        first = False

        # 42 Easter egg
        if 42 in (p1_score, p2_score, draws):
            ui.show_message(
                random.choice(QUOTES_42) + "  🐟  So long, and thanks for all the fish!",
                new_board(), p1, p1_score, p2, p2_score, draws,
                duration_ms=4000,
            )

        if not play_again:
            # Session summary
            if p1_score > p2_score:
                headline = f"{p1} wins the session!"
                sub = random.choice(LOSE) if p2 == "Marvin 🤖" else \
                      f"{p1}: {p1_score}   {p2}: {p2_score}"
            elif p2_score > p1_score:
                headline = f"{p2} wins the session!"
                sub = random.choice(WIN) if p2 == "Marvin 🤖" else \
                      f"{p2}: {p2_score}   {p1}: {p1_score}"
            else:
                headline = "The session is a draw!"
                sub = random.choice(DRAWS)

            ui.show_result_overlay(
                new_board(), headline, sub,
                p1, p1_score, p2, p2_score, draws,
            )
            break
        # else: loop back to menu with accumulated scores


if __name__ == "__main__":
    main()
