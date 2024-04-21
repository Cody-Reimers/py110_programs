TESTS = ((0, 0), (1, 0), (2, 1), (4, 3), (5, 0), (6, 1), (14, 0))

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
            print("Bad input, please provide a positive integer.")

def calculate_leftover(levels, allowed_blocks):
    def add_level(levels):
        new_layer_number = len(levels) + 1
        levels.append(new_layer_number ** 2)

    while allowed_blocks > sum(levels):
        add_level(levels)

    if sum(levels) > allowed_blocks:
        del levels[-1]

    return allowed_blocks - sum(levels)

def main():
    levels = []
    allowed_blocks = get_user_integer()
    leftover = calculate_leftover(levels, allowed_blocks)

    print(f"The number of leftover blocks is: {leftover}")

###############################################################################

print("How many blocks do you want to provide for the tower construction?")

main()
