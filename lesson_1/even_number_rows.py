def get_user_input():
    return input("===> ").strip()

def get_user_integer():
    while True:
        try:
            number = int(get_user_input())
            if number < 0:
                raise ValueError

            return number
        except ValueError:
            print("Bad input, please provide an integer.")

def get_quit():
    while True:
        print("Enter \"y\" to proceed again, or \"n\" to quit.")
        choice = get_user_input().lower()

        if choice[0] in ("y", "n"):
            return choice[0]

        print("Invalid choice.")

def calculate_row_total(target_row):
    start = find_first_row_number(target_row)
    row = construct_row(start, target_row)

    return sum(row)

def find_first_row_number(target_row):
    first_number = 0

    for number in range(target_row):
        first_number += 2 * (number + 1)

    return first_number

def construct_row(start, row_number):
    row = []

    for number in range(row_number):
        row.append(start + 2 * number)

    return row

def main():
    while True:
        print("What number row would you like the sum for?")
        target_row = get_user_integer()
        print(calculate_row_total(target_row))

        print("Would you like another row sum?")
        quit_choice = get_quit()

        if quit_choice == "y":
            continue

        break

main()

print("Thank you for running the even_number_rows calculator!")
