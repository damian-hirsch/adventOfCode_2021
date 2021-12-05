import numpy as np
import re


def get_input():
    # Split lines and write each line to list
    with open('Input/Day05.txt', 'r') as file:
        data = file.read().splitlines()
    return data


def part_one(data: list) -> int:
    # Initialize pipe grid, use 1000 because it should be big enough
    pipe_grid = np.zeros((1000, 1000), dtype=int)

    # For each data line, get x1, y1, x2, y2
    for data_line in data:
        re_matches = re.search(r'(\d+)\D+(\d+)\D+(\d+)\D+(\d+)', data_line)
        x1, y1 = int(re_matches.group(1)), int(re_matches.group(2))
        x2, y2 = int(re_matches.group(3)), int(re_matches.group(4))
        # If either x1 == x2 (horizontal) or y1 == y2 (vertical)
        if x1 == x2 or y1 == y2:
            # Get min, max of the entries first to avoid problems with +1 or -1 when slicing
            pipe_grid[min(y1, y2):max(y1, y2) + 1, min(x1, x2):max(x1, x2) + 1] += 1

    # Count all pipe grid values larger than 1
    return np.count_nonzero(pipe_grid > 1)


def part_two(data: list) -> int:
    # Initialize pipe grid, use 1000 because it should be big enough
    pipe_grid = np.zeros((1000, 1000), dtype=int)

    # For each data line, get x1, y1, x2, y2
    for data_line in data:
        re_matches = re.search(r'(\d+)\D+(\d+)\D+(\d+)\D+(\d+)', data_line)
        x1, y1 = int(re_matches.group(1)), int(re_matches.group(2))
        x2, y2 = int(re_matches.group(3)), int(re_matches.group(4))

        if x1 == x2 or y1 == y2:
            # Get min, max of the entries first to avoid problems with +1 or -1 when slicing (order here can be swapped)
            pipe_grid[min(y1, y2):max(y1, y2) + 1, min(x1, x2):max(x1, x2) + 1] += 1
        # If we have a diagonal (no need to check if len(x) = len(y), because if that were untrue, puzzle wouldn't work)
        else:
            # Setup the entries to cycle through, here the direction matters as order cannot be swapped
            if x1 < x2:
                x_entries = list(range(x1, x2 + 1))
            else:
                x_entries = list(range(x1, x2 - 1, -1))
            if y1 < y2:
                y_entries = list(range(y1, y2 + 1))
            else:
                y_entries = list(range(y1, y2 - 1, -1))

            # Cycle through the two entry lists
            for i in range(len(x_entries)):
                pipe_grid[y_entries[i], x_entries[i]] += 1

    # Count all pipe grid values larger than 1
    return np.count_nonzero(pipe_grid > 1)


def main():
    print('This many points have at least two lines overlapping:', part_one(get_input()))
    print('This many points have at least two lines overlapping when including diagonals:', part_two(get_input()))


if __name__ == '__main__':
    main()
