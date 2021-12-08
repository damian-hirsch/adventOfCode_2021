import re


def get_input():
    with open('Input/Day08.txt', 'r') as file:
        data = file.read().splitlines()
    patterns_list = []
    digits_list = []
    # Split between the patterns and the output digits
    for i in range(len(data)):
        patterns_list.append(re.findall(r'(\D+)\s\|\D+', data[i])[0])
        digits_list.append(re.findall(r'\D+\s\|\s(\D+)', data[i])[0])
    return patterns_list, digits_list


def decode_output(digits: str) -> dict:
    # Initialize dictionary
    dec_dict = {key: None for key in range(10)}
    # Initialize two list for later
    list_235 = []
    list_069 = []

    # Find distinctive digits 1, 4, 7, and 8, else add them to the respective list based on count
    code_strings = digits.split(' ')
    for code in code_strings:
        # Check if 1
        if len(code) == 2:
            dec_dict[1] = set(code)
        # Check if 7
        elif len(code) == 3:
            dec_dict[7] = set(code)
        # Check if 4
        elif len(code) == 4:
            dec_dict[4] = set(code)
        # Check if 8
        elif len(code) == 7:
            dec_dict[8] = set(code)
        # Add 2, 3, 5 to list_235
        elif len(code) == 5:
            list_235.append(code)
        # Add 0, 6, 9 to list_069
        elif len(code) == 6:
            list_069.append(code)
        else:
            print("Error: String length doesn't match!")
            break

    # Find the top right line and middle line by looking at the difference between 4 and 1
    check_for_5 = dec_dict[4].symmetric_difference(dec_dict[1])

    # Compare this to the list of 2, 3, 5, check_for_5 can only be a subset of 5 (not 2 or 3)
    for i in range(len(list_235)):
        set_candidate = set(list_235[i])
        found_5 = check_for_5.issubset(set_candidate)
        if found_5:
            list_235.pop(i)
            dec_dict[5] = set_candidate
            break

    # Find the top right corner
    top_right = dec_dict[1].difference(dec_dict[5])

    # The 8 minus top right corner is the 6
    dec_dict[6] = dec_dict[8] - top_right

    # 6 minus 5 is the bottom right corner
    bottom_right = dec_dict[6] - dec_dict[5]

    # 8 minus the bottom right corner is the 9
    dec_dict[9] = dec_dict[8] - bottom_right

    # Compare bottom right to the list of 2, 3, 5 (containing 2, 3 now), only 2 has it, 3 is the other
    for i in range(len(list_235)):
        set_candidate = set(list_235[i])
        found_2 = bottom_right.issubset(set_candidate)
        if found_2:
            list_235.pop(i)
            dec_dict[2] = set_candidate
            dec_dict[3] = set(list_235[0])
            break

    # 0 is the last one left, one way to get it is from the 0, 6, 9 list
    for i in range(len(list_069)):
        set_candidate = set(list_069[i])
        if not (set_candidate == dec_dict[6] or set_candidate == dec_dict[9]):
            dec_dict[0] = set_candidate
            break

    # We are done and return the decoded dictionary
    return dec_dict


def decode_input(pattern: str, digit: str) -> int:
    # Get the decoded dictionary for the pattern
    decoder = decode_output(pattern)
    # Turn the digit into a set
    digit = set(digit)
    # Initialize number
    number = -1
    # Find the digit with the decoder
    for i in range(10):
        if decoder[i] == digit:
            number = i
            break

    # Return the digit
    return number


def part_one() -> int:
    # Get the digits, patterns are not needed
    _, digits_list = get_input()

    # Initialize digits list
    single_digits_list = []
    # Cycle through all digits and add them to a list
    for digits in digits_list:
        single_digits_list.extend(digits.split(' '))

    # Count the digits with the specific lengths as required
    counter = 0
    for single_digit in single_digits_list:
        if len(single_digit) in (2, 4, 3, 7):
            counter += 1
    return counter


def part_two() -> int:
    # Get the patterns and digits list
    pattern, digits_list = get_input()
    # Initialize translated numbers vector
    numbers = [-1] * len(digits_list)
    for i in range(len(pattern)):
        # Emtpy string
        number = ''
        # Decode each digit and add to string
        for digit in digits_list[i].split(' '):
            number = number + str(decode_input(pattern[i], digit))

        # Convert string to number and add to numbers list
        numbers[i] = int(number)

    # Return sum of all these numbers
    return sum(numbers)


def main():
    print('Digits 1, 4, 7, or 8 appear this many times:', part_one())
    print('Adding up all of the output values gives:', part_two())


if __name__ == '__main__':
    main()
