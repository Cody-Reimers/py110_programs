VOWELS = ("a", "e", "i", "o", "u")

def get_user_input():
    return input("===> ").strip()

def get_idiomatic_words():
    while True:
        line_of_text = get_user_input()

        for character in line_of_text:
            if not (character.isalpha() or character.isspace()):
                print("Not valid text input, please ",
                    "only input letters and spaces.")
                continue

        return line_of_text

def get_quit():
    while True:
        print("Enter \"y\" to proceed again, or \"n\" to quit.")
        choice = get_user_input().lower()

        if choice[0] in ("y", "n"):
            return choice[0]

        print("Invalid choice.")

def calculate_adjacent_consonant_runs(text):
    lengths = {}

    for line in text:
        length = 0
        length_record = 1
        letters = "".join(line.split()).lower()

        for letter in letters:
            if letter in VOWELS:
                length_record = max(length_record, length)
                length = 0
                continue

            length += 1

        lengths[line] = max(length_record, length)

    return lengths

def form_organized_text(lengths):
    organized = []
    lengths_items = list(lengths.items())
    longest_run = max(list(lengths.values()))

    for length in range(longest_run, 0, -1):
        for string, value in lengths_items:
            if value == length:
                organized.append(string)

    return organized

def main():
    text = []
    print("Let's start collecting your inputs to compare.")

    while True:
        text.append(get_idiomatic_words())

        print("Are you done entering different lines of text?")
        quit_choice = get_quit()

        if quit_choice == "y":
            print("Enter your next line of text.")
            continue

        break

    lengths = calculate_adjacent_consonant_runs(text)
    organized = form_organized_text(lengths)

    print(f"Here is your organized list of strings:\n{organized}")

main()