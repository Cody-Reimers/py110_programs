import random
import time
import os

BASE_CHOICES = {
    "1-1": 30, "1-2": 10, "1-3": 30,
    "2-1": 10, "2-2": 80, "2-3": 10,
    "3-1": 30, "3-2": 10, "3-3": 30,
}
BOARD_LENGTH = 3
CENTER_COORDINATES = ("2-2",)
CROSS = "X"
DIAGONAL_BOARD_INDICES = {"left": (0, 4, 8), "right": (2, 4, 6)}
DISPLAY_IRREGULAR_INDICES = (2, 6)
DISPLAY_LENGTH = 9
EMPTY = " "
GAMES_IN_A_MATCH = 5
INDEX_SCALAR = 4
KNOT = "O"
QUIT = "q"
VALID_INPUTS = {
    "turn": "123",
    "players": "12",
    "faction": "ox",
    "new": "n",
    "difficulty": "eh",
}

DISPLAY_LINES = {
    "empty": [ ("|" if index in DISPLAY_IRREGULAR_INDICES else " ")
        for index in range(DISPLAY_LENGTH) ],
    "horizontal": [ ("+" if index in DISPLAY_IRREGULAR_INDICES else "-")
        for index in range(DISPLAY_LENGTH) ],
}
PLAYABLE_POSITIONS = BOARD_LENGTH ** 2
TURN_ORDERS = {
    "O": [ index % 2 == 0 for index in range(PLAYABLE_POSITIONS) ],
    "X": [ not (index % 2 == 0) for index in range(PLAYABLE_POSITIONS) ],
}

###############################################################################

#~~~~BASIC FUNCTIONALITY~~~~# 5 functions

def program_print(message):
    print(f"~~~~~~| {message}")

def critical_print(message):
    print("-" * 127)
    print(f"{message:^127}")
    print("-" * 127)

def board_print(message_list):
    os.system("clear")

    program_print("")

    for sublist in message_list:
        program_print(" " * 10 + "".join([ (element if isinstance(element, str)
            else element[0]) for element in sublist ]))

    program_print("")

def join_or(_list, seperator=", ", terminal_seperator= "and"):
    if len(_list) < 2:
        joined_items = ""

        for item in _list:
            joined_items += str(item)
    elif len(_list) == 2:
        joined_items = f"{str(_list[0])} {terminal_seperator} {_list[1]}"
    else:
        joined_items = seperator.join([ str(item) for item in _list[:-1] ])
        joined_items += f"{seperator}{terminal_seperator} {str(_list[-1])}"

    return joined_items

def get_user_input(state):
    valid_state_inputs = VALID_INPUTS[state] + QUIT

    while True:
        program_print("Valid choices are: " +
            join_or([ repr(char) for char in valid_state_inputs ]))
        choice = input("===> ").strip().casefold()

        if (len(choice) == 1) and choice in valid_state_inputs:
            return choice

        program_print("That's not a valid input!")

#~~~~SETUP AND BOARD MANAGEMENT~~~~# 5 functions

def wrap_settings(user_faction, opponent_faction, is_two_player_mode):
    settings = {}
    settings["user_faction"] = user_faction
    settings["opponent_faction"] = opponent_faction
    settings["is_two_player_mode"] = is_two_player_mode

    return settings

def initialize_choice_weights():
    return BASE_CHOICES.copy()

def setup_board():
    board = [ [ [EMPTY] for _ in range(BOARD_LENGTH) ]
        for _ in range(BOARD_LENGTH) ]

    return board

def setup_display(board):
    display = [ (DISPLAY_LINES["horizontal"][:] if index
        in DISPLAY_IRREGULAR_INDICES else DISPLAY_LINES["empty"][:])
        for index in range(DISPLAY_LENGTH) ]

    for i1 in range(BOARD_LENGTH):
        for i2 in range(BOARD_LENGTH):
            display[i1 * INDEX_SCALAR][i2 * INDEX_SCALAR] = board[i1][i2]

    return display

def mark_board(is_user_turn, board, row, column, settings):
    if is_user_turn:
        mark = settings["user_faction"]
    else:
        mark = settings["opponent_faction"]

    board[row][column][0] = mark

#~~~~COMPUTER DECISION MAKING~~~~# 6 functions

def user_adjustment(ai_choices, row, column, coordinate):
    x, y = [ int(number) for number in coordinate.split("-") ]
    weight = ai_choices[coordinate]

    if abs(row - x) + abs(column - y) == 0:
        ai_choices[coordinate] = 0
    elif abs(row - x) + abs(column - y) == 1:
        ai_choices[coordinate] = int(weight / 1.5)
    elif abs(row - x) + abs(column - y) == 2:
        ai_choices[coordinate] = int(weight * 1.2)
    elif abs(row - x) + abs(column - y) == 3:
        ai_choices[coordinate] = int(weight * 1.75)
    else:
        ai_choices[coordinate] = int(weight * 2.5)

def ai_adjustment(ai_choices, row, column, coordinate):
    x, y = [ int(number) for number in coordinate.split("-") ]
    weight = ai_choices[coordinate]

    if abs(row - x) + abs(column - y) == 0:
        ai_choices[coordinate] = 0
    elif abs(row - x) + abs(column - y) == 1:
        ai_choices[coordinate] = int(weight * 2.5)
    elif abs(row - x) + abs(column - y) == 2:
        ai_choices[coordinate] = int(weight * 1.75)
    elif abs(row - x) + abs(column - y) == 3:
        ai_choices[coordinate] = int(weight * 1.2)
    else:
        ai_choices[coordinate] = int(weight / 1.5)

def adjust_ai_weights(settings, row, column, is_user_move):
    ai_choices = settings["ai_choices"]

    for coordinate in ai_choices.keys():
        if is_user_move:
            user_adjustment(ai_choices, row, column, coordinate)
        else:
            ai_adjustment(ai_choices, row, column, coordinate)

        if coordinate in CENTER_COORDINATES:
            ai_choices[coordinate] *= 2

def find_winning_move(marks, index, settings):
    marks = marks[:index] + settings["opponent_faction"] + marks[index + 1:]
    is_winning_move = bool(find_win_condition(marks)[0])

    if is_winning_move:
        return ((index // 3), (index % 3))

    return False

def find_blocking_move(marks, index, settings):
    marks = marks[:index] + settings["user_faction"] + marks[index + 1:]
    is_blocking_move = bool(find_win_condition(marks)[0])

    if is_blocking_move:
        return ((index // 3), (index % 3))

    return False

def find_override(board, settings):
    marks = "".join([ element[0] for row in board for element in row ])
    winning_override, blocking_override = False, False

    for index, char in enumerate(marks):
        if char in (CROSS, KNOT):
            continue

        winning_move = find_winning_move(marks, index, settings)
        blocking_move = find_blocking_move(marks, index, settings)

        if winning_move:
            winning_override = winning_move
        if blocking_move:
            blocking_override = blocking_move

    return winning_override or blocking_override

#~~~~RUNNING A TURN IN PLAY~~~~# 3 functions

def run_computer_turn(board, settings):
    program_print("Processing computer turn...")
    time.sleep(1.5)

    ai_choices = settings["ai_choices"]

    if settings["difficulty"] == "hard":
        override = find_override(board, settings)
        if override:
            return override

    choice = random.choices(list(ai_choices.keys()),
        weights=list(ai_choices.values()))[0]

    return [ int(number) - 1 for number in choice.split("-") ]

def run_player_turn(player, board):
    row, column = 0, 0

    program_print(F"It's your turn to make a move, {player}!")
    program_print("You'll be asked to select the row (top-to-bottom),")
    program_print("then the column (left-to-right) to leave your mark in.")

    while True:
        row = get_user_input("turn")
        if row == QUIT:
            return row, column

        column = get_user_input("turn")
        if column == QUIT:
            return row, column

        row, column = int(row) - 1, int(column) - 1

        if board[row][column][0] in (KNOT, CROSS):
            program_print("That square is already marked:")
            program_print("you need to pick a different one.")
        else:
            break

    return row, column

def control_turn(is_user_turn, board, settings):
    if is_user_turn and not settings["is_two_player_mode"]:
        row, column = run_player_turn("user", board)
        if QUIT in (row, column):
            return row, column
        adjust_ai_weights(settings, row + 1, column + 1, True)
    elif is_user_turn:
        row, column = run_player_turn("user", board)
    elif settings["is_two_player_mode"]:
        row, column = run_player_turn("guest", board)
    else:
        row, column = run_computer_turn(board, settings)
        adjust_ai_weights(settings, row + 1, column + 1, False)

    return row, column

#~~~~ENDING THE GAME~~~~# 9 functions

def check_if_full(marks):
    full_board = marks.isalpha()
    return full_board

def equivalent_faction_marks(mark1, mark2, mark3):
    return mark1 in (CROSS, KNOT) and (mark1 == mark2) and (mark2 == mark3)

def check_row(start, marks):
    mark1, mark2, mark3 = marks[start:start + BOARD_LENGTH]
    return equivalent_faction_marks(mark1, mark2, mark3)

def check_column(start, marks):
    mark1, mark2, mark3 = marks[start::BOARD_LENGTH]
    return equivalent_faction_marks(mark1, mark2, mark3)

def check_diagonals(marks):
    i1, i2, i3 = DIAGONAL_BOARD_INDICES["left"]
    mark1, mark2, mark3 = marks[i1], marks[i2], marks[i3]
    if equivalent_faction_marks(mark1, mark2, mark3):
        return "left", i2

    i1, i2, i3 = DIAGONAL_BOARD_INDICES["right"]
    mark1, mark2, mark3 = marks[i1], marks[i2], marks[i3]
    if equivalent_faction_marks(mark1, mark2, mark3):
        return "right", i2

    return False, 0

def find_win_condition(marks):
    for start in range(0, PLAYABLE_POSITIONS, BOARD_LENGTH):
        victorious = check_row(start, marks)

        if victorious:
            return "row", (start // BOARD_LENGTH)

    for start in range(0, BOARD_LENGTH):
        victorious = check_column(start, marks)

        if victorious:
            return "column", start

    return check_diagonals(marks)

def find_winner(marks, victory_style, victorious_index, settings):
    user_faction = settings["user_faction"]

    if victory_style == "row":
        if marks[victorious_index * BOARD_LENGTH] == user_faction:
            return "user"

    if victory_style == "column":
        if marks[victorious_index] == user_faction:
            return "user"

    if victory_style in ("left", "right"):
        if marks[victorious_index] == user_faction:
            return "user"

    return "opponent"

def report_endgame(style="tie", index=0, winner="",
    settings=None, victories=None):
    if style == "tie":
        program_print("Woops! Looks like the game is tied:")
        program_print("the board is filled up and there's no winner.")
    else:
        if winner == "opponent":
            winner = "guest" if settings["is_two_player_mode"] else "computer"

        if style in ("left", "right"):
            victory_location = f"the {style} diagonal"
        else:
            victory_location = f"{style} {index + 1}"

        program_print(f"The {winner} got 3 in a row at {victory_location}!")
        victories[winner] += 1

def manage_endgame(board, settings, victories):
    marks = "".join([ element[0] for row in board for element in row ])

    full_board = check_if_full(marks)
    victory_style, where_victory = find_win_condition(marks)

    if (full_board or victory_style) is False:
        return False

    if victory_style is False:
        report_endgame()
    else:
        winner = find_winner(marks, victory_style, where_victory, settings)

        report_endgame(victory_style, where_victory, winner,
            settings, victories)

    return True

#~~~~MAIN PROGRAM~~~~#

def main(user_faction, opponent_faction, is_two_player_mode):
    settings = wrap_settings(user_faction, opponent_faction,
        is_two_player_mode)

    if not settings["is_two_player_mode"]:
        program_print("Do you want the computer opponent to be")
        program_print("on the easier side or harder side?")
        difficulty_choice = get_user_input("difficulty")
        if difficulty_choice == QUIT:
            return
        settings["difficulty"] = "easy" if difficulty_choice == "e" else "hard"

    program_print("Initializing...")
    time.sleep(1)

    victories = {
        "user": 0,
        "guest" if settings["is_two_player_mode"] else "computer": 0,
    }

    while True:
        if not settings["is_two_player_mode"]:
            settings["ai_choices"] = initialize_choice_weights()
        board = setup_board()
        display = setup_display(board)
        turn_order = TURN_ORDERS[settings["user_faction"]]
        turn_number = 0

        board_print(display)

        while True:
            is_user_turn = turn_order[turn_number]
            row, column = control_turn(is_user_turn, board, settings)
            if QUIT in (row, column):
                break

            mark_board(is_user_turn, board, row, column, settings)

            board_print(display)

            game_over = manage_endgame(board, settings, victories)
            if game_over:
                break

            turn_number += 1

        if QUIT in (row, column):
            break

        program_print("The match scores are: ")
        program_print(" and ".join( [ f"{player}: {str(score)}" for
            player, score in victories.items() ]))

        if GAMES_IN_A_MATCH in victories.values():
            program_print("The winner of the match has been decided!")
            program_print("Would you like another match with these settings?")
            if get_user_input("new") == QUIT:
                break
        else:
            program_print("Reinitialize for a new game?")
            if get_user_input("new") == QUIT:
                break

        program_print("Reinitializing...")
        time.sleep(1)

###############################################################################

critical_print("Welcome, user! This is the Tic-Tac-Toe machine!")

program_print("This program will allow you to play Tic-Tac_toe either")
program_print("on your own or against a friend, just follow the prompts.")
program_print(f"At any time, you can enter \"{QUIT}\" to quit.")
program_print("And please, only enter a single character of input when asked.")

while True:
    program_print("Do you want to play as \"O\"s or \"X\"s? \"O\"s go first!")
    faction_choice = get_user_input("faction")
    if faction_choice == QUIT:
        break

    program_print("Do you want a single-player game or two-player game?")
    players_choice = int(get_user_input("players"))
    if players_choice == QUIT:
        break

    main((faction_choice.upper()),
        (CROSS if faction_choice == KNOT.casefold() else KNOT),
        (players_choice == 2))

    program_print("Would you like to start a new match?")
    program_print("Or would you like to quit the program?")
    if get_user_input("new") == QUIT:
        break

critical_print("Farewell!")
