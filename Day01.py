import numpy as np


# Get data from .txt file
def get_input():
    with open('Input/Day01.txt', 'r') as file:
        data = file.read().splitlines()
        # Map strings in list to integers
        data = list(map(int, data))
    return data


# Solves part 1
def part_one(data: list) -> int:
    # Shift the data list by one value and use a comparison operator to get a true/false list
    analysis_list = data > np.roll(data, 1)
    # Remove the first value (it's comparing the first and last value) and take the sum of True values
    return sum(analysis_list[1:])


# Solves part 2
def part_two(data: list) -> int:
    # Using numpy.convolve with a unit vector to get an easy way to calculate the sliding window
    window_array = np.convolve(data, np.ones(3, dtype=int), 'valid')
    # Shift the data list by one value and use a comparison operator to get a true/false list
    analysis_list = window_array > np.roll(window_array, 1)
    # Remove the first value (it's comparing the first and last value) and take the sum of True values
    return sum(analysis_list[1:])


def main():

    print('This many measurements are larger than the previous measurement: ', part_one(get_input()))
    print('This sums are larger than the previous sum: ', part_two(get_input()))


if __name__ == '__main__':
    main()
