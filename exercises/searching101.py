TIMES = ("1st", "2nd", "3rd", "4th", "5th", "last")

def print_system(message, empty_above=True, empty_below=True):
    if empty_above:
        print("")

    print(f"~~~~| {message}")

    if empty_below:
        print("")

def print_outcome(numbers, is_in):
    numbers = [str(number) for number in numbers]

    if is_in:
        is_in = "is in"
    else:
        is_in = "isn\'t in"

    print_system(" ".join((numbers[-1], is_in, str(numbers[:-1]))))

def get_user_input():
    return input("===> ").strip()

def get_user_integer():
    while True:
        try:
            return int(get_user_input())
        except ValueError:
            print_system("Bad input, please enter an integer.")

def get_numbers():
    numbers = []

    for time in TIMES:
        print_system(f"Enter the {time} number.")
        numbers.append(get_user_integer())

    return numbers

def main():
    print_system("Let's start collecting your input.", False, False)
    numbers = get_numbers()
    is_in = False

    for number in numbers[:-1]:
        if numbers[-1] == number:
            is_in = True
            break

    print_outcome(numbers, is_in)

###############################################################################

print_system(("This program will collect 6 numbers from you, " +
    "and tell you if the final number is repeated anywhere " +
    "in the first 5 numbers you provided."), True, False)
main()
