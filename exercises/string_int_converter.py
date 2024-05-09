STR_INT_CONVERTS = {
    0: "0",
    "0": 0,
    1: "1",
    "1": 1,
    2: "2",
    "2": 2,
    3: "3",
    "3": 3,
    4: "4",
    "4": 4,
    5: "5",
    "5": 5,
    6: "6",
    "6": 6,
    7: "7",
    "7": 7,
    8: "8",
    "8": 8,
    9: "9",
    "9": 9,
}

def integer_to_string(integer):
    integer = abs(integer)
    digits = []

    while True:
        integer, current_digit = divmod(integer, 10)
        digits.append(STR_INT_CONVERTS[current_digit])

        if integer == 0:
            break

    return "".join(reversed(digits))

def signed_integer_to_string(integer):
    number_string = integer_to_string(integer)

    if integer > 0:
        number_string = "+" + number_string
    elif integer < 0:
        number_string = "-" + number_string

    return number_string

def string_to_integer(number_string):
    digits = []

    for character in number_string:
        if character in STR_INT_CONVERTS:
            digits.append(STR_INT_CONVERTS[character])

    return sum([ digit * 10 ** index for index,
        digit in enumerate(reversed(digits)) ])

def string_to_signed_integer(number_string):
    number = string_to_integer(number_string)

    return (-1 * number if number_string[0] == "-" else number)

print(string_to_integer("4321") == 4321)  # True
print(string_to_integer("570") == 570)    # True

print(string_to_signed_integer("4321") == 4321)  # True
print(string_to_signed_integer("-570") == -570)  # True
print(string_to_signed_integer("+100") == 100)   # True

print(integer_to_string(4321) == "4321")              # True
print(integer_to_string(0) == "0")                    # True
print(integer_to_string(5000) == "5000")              # True
print(integer_to_string(1234567890) == "1234567890")  # True

print(signed_integer_to_string(4321) == "+4321")  # True
print(signed_integer_to_string(-123) == "-123")   # True
print(signed_integer_to_string(0) == "0")         # True
