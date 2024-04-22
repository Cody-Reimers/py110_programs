def print_system(message, empty_above=True, empty_below=True):
    if empty_above:
        print("")

    print(f"~~~~~~~~| {message}")

    if empty_below:
        print("")

def get_user_input():
    return input("===> ").strip()

def get_quit():
    while True:
        print_system("Enter \"y\" to proceed again, or \"n\" to quit.",
            False, True)
        choice = get_user_input().lower()

        if choice[0] in ("y", "n"):
            return choice[0]

        print_system("Invalid choice.", True, False)

def check_palindrome(text):
    if not text:
        return False

    temp = ""

    for character in text:
        if character.isalnum():
            temp += character.casefold()

    return (True if temp == temp[::-1] else False)

def main():
    print_system("Enter the string you would like to check.", False, True)

    while True:
        text = get_user_input()
        is_palindrome = check_palindrome(text)

        if is_palindrome:
            print_system("The text you provided is a palindrome.",
                True, False)
        else:
            print_system("The text you provided is not a palindrome.",
                True, False)

        print_system("Would you like to check another string?", False, False)
        choice = get_quit()

        if choice == "y":
            print_system("Enter the next string you would like to check.")
            continue

        break

###############################################################################

print_system(("This program can help you check if " +
    "a given string of text is a palindrome."), True, False)
main()

print_system("Farewell!")
