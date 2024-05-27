import random
import time

ACES = ("ace",)
ACE_VALUES = (1, 11)
BUST = 21
CARD_TYPES = {
    1: "ace",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "jack",
    12: "queen",
    13: "king",
}
DEALER_STAY = 17
FACES = ("ten", "jack", "queen", "king")
FACE_VALUE = 10
HIT_COMMAND = "d"
MESSAGE_SLEEP = {"slow": 0.75, "fast": 0.33, "lightning": 0.07}
NUMBER_OF_CARD_TYPES = 13
NUMBER_OF_SUIT_TYPES = 4
QUIT = "q"
STARTUP_SLEEP = 15
STAY_COMMAND = "s"
SUIT_TYPES = {
    1: "hearts",
    2: "clubs",
    3: "spades",
    4: "diamonds",
}
UNKNOWN_DEALER_VALUE = 0
VALID_INPUTS = {"turn": "ds", "ready": "r", "new": "n"}
VICTORY_THRESHHOLD = 5

NUMBER_OF_CARDS = NUMBER_OF_CARD_TYPES * NUMBER_OF_SUIT_TYPES

###############################################################################

#~~~~BASIC FUNCTIONALITY~~~~#

def program_print(message):
    print(f"~~~~~~| {message}")
    time.sleep(MESSAGE_SLEEP["lightning"])

def critical_print(message):
    print("-" * 127)
    print(f"{message:^127}")
    print("-" * 127)

def display_card(card_number, value, whose_card=""):
    what_card = CARD_TYPES[(card_number % NUMBER_OF_CARD_TYPES) + 1]
    what_suit = SUIT_TYPES[((card_number + NUMBER_OF_CARD_TYPES - 1)
        // NUMBER_OF_CARD_TYPES)]
    card_value = get_card_value(card_number, value)

    if whose_card == "dealer":
        if what_card in ACES:
            card_value = join_or(ACE_VALUES, "", "or")

        program_print("You can see the dealer has the:")
    elif whose_card == "player":
        program_print("You have the:")

    program_print(f"{what_card} of {what_suit}, which is worth {card_value}")

def display_cards(player_hand, dealer_hand):
    program_print("")

    revealed_dealer_card = dealer_hand["cards"][0]
    display_card(revealed_dealer_card, UNKNOWN_DEALER_VALUE, "dealer")

    first_player_card  = player_hand["cards"][0]
    player_value = player_hand["value"]
    display_card(first_player_card, player_value, "player")

    for card_number in player_hand["cards"][1:]:
        display_card(card_number, player_value)

    program_print("")

def display_dealer_cards(dealer_hand):
    program_print("The dealer has:")

    for card_number in dealer_hand["cards"]:
        display_card(card_number, dealer_hand["value"])

def join_or(_list, seperator=", ", terminal_seperator="and"):
    if len(_list) < 2:
        joined_items = ""

        for item in _list:
            joined_items += str(item)
    elif len(_list) == 2:
        joined_items = f"{str(_list[0])} {terminal_seperator} {str(_list[1])}"
    else:
        joined_items = seperator.join([ str(item) for item in _list[:-1] ])
        joined_items += f"{seperator}{terminal_seperator} {str(_list[-1])}"

    return joined_items

def receive_user_input(state):
    valid_state_inputs = VALID_INPUTS[state] + QUIT

    while True:
        program_print("Valid choices are: " +
            join_or([ repr(char) for char in valid_state_inputs ]))
        choice = input("===> ").strip().casefold()

        if (len(choice) == 1) and choice in valid_state_inputs:
            return choice

        program_print("That's not a valid input!")

#~~~~HAND MANAGEMENT~~~~#

def get_card_value(card_number, value):
    card_type = CARD_TYPES[(card_number % NUMBER_OF_CARD_TYPES) + 1]

    if card_type in FACES:
        return FACE_VALUE # returns 10
    if card_type not in ACES:
        return (card_number % NUMBER_OF_CARD_TYPES) + 1 # returns 2-9

    return (ACE_VALUES[0] if value + ACE_VALUES[1] > BUST
        else ACE_VALUES[1]) # returns 1 or 11

def update_value(hand):
    value = 0

    for card_number in hand["cards"]:
        value += get_card_value(card_number, value)

    hand["value"] = value

def draw(hand, deck):
    card = deck.pop(0)
    hand["cards"].append(card)

    update_value(hand)

def initialize_hands(deck):
    player_hand = {"value": 0, "cards": []}
    dealer_hand = {"value": 0, "cards": []}

    for _ in range(2):
        draw(player_hand, deck)
        draw(dealer_hand, deck)

    return player_hand, dealer_hand

#~~~~RUNNING A TURN IN PLAY~~~~#

def run_player_turn(hand, deck):
    program_print("It's your turn! Do you want to draw, or stay?")
    turn_choice = receive_user_input("turn")
    if turn_choice == HIT_COMMAND:
        draw(hand, deck)
        program_print("You drew:")
        display_card(hand["cards"][-1], hand["value"])
    return turn_choice

def run_dealer_turn(hand, deck):
    if hand["value"] >= DEALER_STAY:
        return hand["value"]

    draw(hand, deck)

    program_print("The dealer drew:")
    display_card(hand["cards"][-1], hand["value"])

    return hand["value"]

def control_turn(hand, whose_turn, deck):
    if whose_turn == "player":
        choice = run_player_turn(hand, deck)
        if hand["value"] > BUST:
            return "busted"
        return choice

    return run_dealer_turn(hand, deck)

#~~~~GAME MANAGEMENT~~~~#

def player_loop(player_hand, dealer_hand, deck):
    while True:
        display_cards(player_hand, dealer_hand)
        program_print(f"Your total value is {player_hand['value']}")

        status = control_turn(player_hand, "player", deck)
        if status == QUIT:
            return status
        if status == "busted":
            return "player busted"
        if status == "s":
            program_print("You've chosen to stay! Let's see if the dealer")
            program_print("gets a higher value than you without busting!")
            return player_hand["value"]

def dealer_loop(dealer_hand, deck):
    while True:
        status = control_turn(dealer_hand, "dealer", deck)
        if status > BUST:
            return "dealer busted"
        if status >= DEALER_STAY:
            return status

def turns_loop(player_hand, dealer_hand, deck):
    player_status = player_loop(player_hand, dealer_hand, deck)
    if player_status == QUIT:
        return player_status
    if player_status == "player busted":
        program_print("You busted out!")
        return "lost"

    program_print("Time to see how it goes for the dealer!")
    display_dealer_cards(dealer_hand)

    dealer_status = dealer_loop(dealer_hand, deck)
    if dealer_status == "dealer busted":
        program_print("The dealer busted out!")
        return "won"

    return "won" if player_status >= dealer_status else "lost"

def report_endgame(victory_status, victories):
    if victory_status == "won":
        program_print("Good job, you won that game!")

        victories["user"] += 1

        if VICTORY_THRESHHOLD in victories.values():
            program_print("You won the match! Way to go!")

    if victory_status == "lost":
        program_print("Sadly, you lost that game.")

        victories["dealer"] += 1

        if VICTORY_THRESHHOLD in victories.values():
            program_print("The dealer won that match!")
            program_print("You're really getting it handed to you!")

def game_loop(victories):
    while True:
        program_print("")
        program_print("Game begin!")

        deck = list(range(1, NUMBER_OF_CARDS + 1))
        random.shuffle(deck)
        player_hand, dealer_hand = initialize_hands(deck)

        game_over = turns_loop(player_hand, dealer_hand, deck)
        if game_over in ("lost", "won"):
            report_endgame(game_over, victories)
        if game_over in (QUIT, "lost", "won"):
            return game_over

#~~~~MAIN PROGRAM~~~~#

def main():
    victories = {"user": 0, "dealer": 0}

    while True:
        game_choice = game_loop(victories)
        if game_choice == QUIT:
            break

        program_print("Now that game is over.")
        program_print("Do you want to quit the program, or start a new game?")
        program_print("Victories will be tracked as long as you don't quit!")
        if receive_user_input("new") == QUIT:
            break

###############################################################################

critical_print("Welcome to TWENTY1!")

program_print("The rules of 21 are fairly simple: you and the dealer draw two")
program_print("cards to start off, then you'll draw more cards until your")
program_print("total value is greater than 21, or you choose to \"stay\".")
program_print("Then, the computer, standing in for the dealer, will do the")
program_print("same: the computer always stays once its total is at least 17.")
program_print("Cards 2-9 are worth their value, 10s and faces are worth 10,")
program_print("aces are worth 11 unless that would cause you to exceed 21,")
program_print("then any aces are worth 1. For rules questions, see Wikipedia.")

program_print("")
program_print("When you receive prompts, please only enter 1 input.")
program_print("You can enter \"q\" as any input to quit the program.")
program_print("When you're done reading the rules, you can enter an")
program_print("input to get the game rolling.")

if receive_user_input("ready") == QUIT:
    pass
else:
    while True:
        program_print("Initializing game...")
        time.sleep(1)

        if main() == QUIT:
            break

critical_print("Farewell!")
