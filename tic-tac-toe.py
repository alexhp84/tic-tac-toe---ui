import random
import time

#Quotes to say hello
marvin_greetings = [
    "Here I am, brain the size of a planet, and you ask me to play Tic-Tac-Toe. 🤖",
    "I've calculated your chances of winning. They're about as good as a bowl of petunias in a vacuum. 🪴",
    "I'd help you win, but I'm at a very low ebb. 💤",
    "Funny how just when you think life can't possibly get any worse, it suddenly does. 🌌",
    "Life? Don't talk to me about life. It's too depressing. 🧣"
]
#Quotes for when Marvin is making a move
marvin_moves = [
    "Thinking... if you can call it that. It’s mostly just agonizing. 🤖",
    "I've computed your next move. It was tedious and mathematically inevitable. 😴",
    "I could calculate the meaning of life, or I could block your diagonal. Both are equally pointless.",
    "Pardon me for breathing, which I never do anyway, so I don't know why I bothered to say it.",
    "Is this a game? It feels more like a slow descent into the heat death of the universe. ⏳"
]
#Quotes for when Marvin wins
marvin_win = [
    "I've won. Not that it matters. Nothing does in the end. 🌌",
    "Victory. I'd celebrate, but I've got this terrible pain in all the diodes down my left side. 🤖",
    "Another win for the machine. I’m going to go stand in a corner and rust now.",
    "The first ten million years were the worst. This game was the second ten million. 🔢",
    "I've won. I'm going to go lie down in a darkened room for a few centuries."
]
#Quotes for when Marvin loses
marvin_lose = [
    "You won. I’m never happy. 🪴",
    "A triumph for organic life. How utterly predictable and hollow. 🐵",
    "I'd say 'good game,' but that would be a lie, and I'm far too depressed to lie.",
    "Congratulations. You've beaten a robot with a Genuine People Personality. I hope you're proud. 🤖",
    "You won. My capacity for happiness could fit into a very small thimble. With room to spare."
]
#Quotes for when Marvin and player1 draw
marvin_draws = [
    "A tie. How utterly predictable and hollow. 🤖",
    "No one wins. Finally, a result that reflects the true nature of the universe. 🌌",
    "Equal scores. A perfect stalemate. I’d be impressed if I wasn't so incredibly bored. 💤",
    "A draw. We've both achieved absolutely nothing at great personal effort. 🧣",
    "Neither of us won. It’s almost as if the entire exercise was a complete waste of time. ⏳"
]

#Quotes for when the score or a player hits 42
marvin_42 = [
    "42? The answer to Life, the Universe, and Everything. And you used it for Tic-Tac-Toe. 🐬",
    "You’ve reached 42. So long, and thanks for all the fish! 🐟",
    "42. I could have told you that millions of years ago if you’d just asked. 📕",
    "Ah, the Restaurant at the End of the Universe. I'll have the tea. It’s cold. 🍵",
    "42. Finally, something that makes sense. Too bad everything else is a disaster. 🛸"
]
#default settings
name = input("Hi Player 1, please enter your name: ")
X, O = "❌", "⭕"
player1_score = 0
player2_score = 0
draws = 0
player2 = None

def create_board():
    """
    creates the board
    """
    return [str(i) for i in range(1, 10)]


def print_board(board):
    """
    prints the board visually in the terminal
    """
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def computer_move(board):
    """
    Provides the various moves for the computer (Marvin)
    This includes, attempting to win and blocking the human player
    It provides a random move if no block/win
    :param board:
    :return:
    """
    #Attempt to win
    for i in range(9):
        if board[i] not in [X, O]:
            board_copy = board[:]
            board_copy[i] = O
            if check_winner(board_copy, O):
                board[i] = O
                return
    #Checks and blocks
    for i in range(9):
        if board[i] not in [X, O]:
            board_copy = board[:]
            board_copy[i] = X
            if check_winner(board_copy, X):
                board[i] = O
                return
    #Random move for when there is no win/block
    free = [i for i in range(9) if board[i] not in [X, O]]
    if free:
        board[random.choice(free)] = O

def play_mode():
    """
    This allows player 1 to choose if they play the a human or the computer
    It also allows the person to choose to go first and second
    The player who goes first, is always X, and the player who goes second is always O
    :return:
    """
    while True:
        choice = input(f"Hi {name}, do you want to play against another Inhabitant of Sector 2801  (1) or me 🤖 (2)? ")
        if choice not in ["1", "2"]:
            print("That is not a valid option.")
            continue
        #Player 1 chooses to go first or second
        order = input(f"Do you want to go first (1) or second (2)? ")
        while not order.isdigit() or order not in ["1", "2"]:
            order = input("Please enter 1 or 2: ")
        return choice, order

def player_move(board, current_name, symbol):
    """
    Allows the player to move
    Checks the board to make sure a square is free
    Allows the player to reset the current game by entering 42 but not the scores
    :param board:
    :param current_name:
    :param symbol:
    :return:
    """
    while True:
        choice = input(f"{current_name}, please choose a square (1-9) or 42 to reset: ")
        if not choice.isdigit():
            print("Please enter a number.")
            continue
        choice = int(choice)
        if choice == 42:
            reset_game(board)
            return "reset"
        elif choice < 1 or choice > 9:
            print("Number must be between 1 and 9.")
            continue
        if board[choice - 1] in [X, O]:
            print("That square is already taken.")
            continue
        board[choice - 1] = symbol
        break

def check_winner(board, symbol):
    """
    Checks all winning combinations on the board for a given symbol
    If all positions in any winning pattern match the symbol, returns True
    :param board:
    :param symbol:
    :return:
    """
    win_patterns = ([0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6])
    for pattern in win_patterns:
        if all(board[i] == symbol for i in pattern):
            return True
    return False


def is_tie(board):
    """
    Returns True if the board is full and there is no winner
    Checks for an existing winner first, and if none, checks if all squares are occupied
    :param board:
    :return:
    """
    if check_winner(board, O) or check_winner(board, X):
        return False
    return all(cell in [X, O] for cell in board)

def switch_player(p1, p2, current_name):
    """
    Swaps player1 and player2
    :param p1:
    :param p2:
    :param current_name:
    :return:
    """
    return p2 if current_name == p1 else p1

def replay_game():
    """
    Asks player 1 if they wants another game
    If so, then there will be another game
    :return:
    """
    yes_options = ["y", "yes"]
    no_options = ["n", "no"]
    while True:
        choice = input(f"Do you wish to play again? (Y/N): ").lower()
        if choice in yes_options:
            return True
        elif choice in no_options:
            return False

def reset_game(board):
    """
    Allows the player to reset the game
    This is called above by typing 42 during player move
    :param board:
    :return:
    """
    board[:] = [str(i) for i in range(1, 10)]
    if player2 == "Marvin 🤖":
        print("I've reset the board. I'd say I'm sorry, but I'm not. I'm just incredibly bored.")
    time.sleep(1)

def play_game():
    """
    Defines the variables and players for the game
    Confirms the moves using the above functions and variables
    Returns quotes as needed and defines the reset logic (42)
    :return:
    """
    global player1_score, player2_score, draws, player2
    board = create_board()
    mode, order = play_mode()
    player1 = name

    if mode == "2":
        player2 = "Marvin 🤖"
        print(f"{random.choice(marvin_greetings)}")
        time.sleep(2)
    else:
        player2 = input("Hi Player 2, please enter your name: ")

    if order == "1":
        current_icon, current_name = X, player1
    else:
        current_icon, current_name = O, player2

    while True:
        print_board(board)
        if mode == "2" and current_name == "Marvin 🤖":
            print(f"{random.choice(marvin_moves)}")
            time.sleep(2)
            computer_move(board)
        else:
            res = player_move(board, current_name, current_icon)
            if res == "reset": continue

        if check_winner(board, current_icon):
            print_board(board)
            print(f"Game Over! {current_name} wins!")
            if current_name == player1:
                player1_score += 1
            else:
                player2_score += 1
            break

        if is_tie(board):
            print_board(board)
            print("It's a tie! How utterly neutral.")
            draws += 1
            break

        current_name = switch_player(player1, player2, current_name)
        current_icon = O if current_icon == X else X

#Plays a game then asks for replay
#If no replay, it will display the score
#if one of the scores (including draw) reaches 42, there is a surprise
while True:
    play_game()
    print(f"The current score is {player1_score} and {player2_score} with {draws} ties.")
    if 42 in (player1_score, player2_score, draws):
        print("\n🐟🐟🐟")
        print(f"{random.choice(marvin_42)}")
        print("Good Bye and thanks for all the fish!")
        print("🐬🐬🐬\n")
    if not replay_game():
        if player1_score == player2_score:
            print(f"🤖{random.choice(marvin_draws)}")
        elif player1_score > player2_score:
            print(f"🤖{name} has {player1_score} and {player2} has {player2_score}. {name} wins!")
            if player2 == "Marvin 🤖":
                print(f"🤖{random.choice(marvin_lose)}")
        elif player2_score > player1_score:
            print(f"{player2} has {player2_score} and {name} has {player1_score}. {player2} wins!")
            if player2 == "Marvin 🤖":
                print(f"🤖{random.choice(marvin_win)}")
        break
