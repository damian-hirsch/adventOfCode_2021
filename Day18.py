import numpy as np
import re
import ast

# Note: The problem is set up as a binary problem, but it offers several pitfalls:
# - Need to remember if an explosions has already happened or not
# - During explosions, the left add can cause troubles when ones needs to go back to a previously visited left branch
# Due to that, here a string implementation is used, that seems to be way more straight-forward, without complicated
# recursive functions or similar, performance-wise it's not great, but by far sufficient


# Get data from .txt file
def get_input():
    # Split lines and write each line to list
    with open('Input/Day18.txt', 'r') as file:
        data = file.read().splitlines()
    # Convert the data strings to a list of data
    data_list = []
    for data_line in data:
        data_list.append(ast.literal_eval(data_line))
    return data_list


# Add two list pairs together using string representation
def add_pair(pair: str, add: str) -> str:
    return '[' + pair + ', ' + add + ']'


# Function to take care of explosions
def explode(list_string: str) -> str:
    # We have an explosion if we are 5 levels deep
    counter = 0
    for i, char in enumerate(list_string):
        if char == '[':
            counter += 1
        elif char == ']':
            counter -= 1
            counter_set = False

        if counter == 5:
            # Left string
            left_string = list_string[:i]
            # Right string
            right_string = list_string[i+1:]

            # Explode
            re_explode = re.search(r'(\d+),\s(\d+)', right_string)
            # Get left value that needs to be added to the left
            explode_left = int(re_explode.group(1))
            # Get right value that needs to be added to the right
            explode_right = int(re_explode.group(2))
            # Get the end position of the right value
            explode_right_pos = re_explode.end(2)
            # Remove explosion in string
            right_string = '0' + right_string[explode_right_pos+1:]

            # Update second number on the right if it exists (first number is the 0 after the explosion)
            re_update_right = re.search(r'\d+\D+(\d+)', right_string)
            if re_update_right is not None:
                right_update = int(re_update_right.group(1))
                r_pos_start = re_update_right.start(1)
                r_pos_end = re_update_right.end(1)
                # Update right string
                right_string = right_string[:r_pos_start] + f'{right_update + explode_right}' + right_string[r_pos_end:]

            # Search last digit on the left and add if it exists
            re_update_left = re.search(r'(\d+)\D+$', left_string)
            if re_update_left is not None:
                left_update = int(re_update_left.group(1))
                l_pos_start = re_update_left.start(1)
                l_pos_end = re_update_left.end(1)
                # Update left string
                left_string = left_string[:l_pos_start] + f'{left_update + explode_left}' + left_string[l_pos_end:]

            # Merge left and right string, break the loop, because we can only do one explosion per round
            list_string = left_string + right_string
            break

    return list_string


# Function to split string values greater or equal 10
def split(string_list: str) -> str:
    # Find first two digit number
    re_split = re.search(r'(\d\d)', string_list)
    # If it exists, split it
    if re_split is not None:
        digit = int(re_split.group(1))
        digit_start = re_split.start(1)
        digit_end = re_split.end(1)

        split_digit_left = int(np.floor(digit/2))
        split_digit_right = int(np.ceil(digit/2))

        string_list = string_list[:digit_start] + f'[{split_digit_left}, {split_digit_right}]' + string_list[digit_end:]

    return string_list


# Calculate the magnitude of a list
def calc_magnitude(pair: list) -> int:
    # Continue recursion as long as we are not at integer level
    pair_left = pair[0]
    pair_right = pair[1]

    if type(pair_left) == int:
        magnitude_left = 3 * pair_left
    else:
        magnitude_left = 3 * calc_magnitude(pair_left)

    if type(pair_right) == int:
        magnitude_right = 2 * pair_right
    else:
        magnitude_right = 2 * calc_magnitude(pair_right)

    magnitude = magnitude_left + magnitude_right

    return magnitude


def part_one(data_list: list) -> int:
    # Initialize first list
    sf_number = str(data_list[0])
    # Add up lists until we are done
    for i in range(len(data_list) - 1):
        # Add the current list with a new one from data
        sf_number = add_pair(sf_number, str(data_list[i+1]))
        sf_number_old = ''
        # Split as long as we can
        while sf_number != sf_number_old:
            # Explode as long as we can
            while sf_number != sf_number_old:
                sf_number_old = sf_number
                sf_number = explode(sf_number)
            sf_number = split(sf_number)
    # Cast the string list to a real list for calculation
    return calc_magnitude(ast.literal_eval(sf_number))


def part_two(data: list) -> int:
    # Initialize max value
    calc_max = 0
    # Check each possible combination except with itself
    for i, first_list in enumerate(data):
        for j, second_list in enumerate(data):
            if i != j:
                # Create candidate list
                candidate_list = [first_list, second_list]
                # We can reuse part 1
                candidate_calc = part_one(candidate_list)
                # If the candidate list has a higher value than the currently best combination, update the value
                if candidate_calc > calc_max:
                    calc_max = candidate_calc
    return calc_max


def main():
    print('The magnitude of the final sum is: ', part_one(get_input()))
    print('The largest magnitude of any sum of two different snail fish numbers is:', part_two(get_input()))


if __name__ == '__main__':
    main()
