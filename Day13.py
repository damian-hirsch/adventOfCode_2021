import numpy as np
import re


# Get data from .txt file
def get_input():
    # Split lines and write each line to list
    with open('Input/Day13.txt', 'r') as file:
        data = file.read().splitlines()
    # Initialize the two lists we need to get
    dots_coord = []
    folds = []
    # Initialize the space finder bool
    space_found = False
    for data_line in data:
        # If we found the space, set the bool to true
        if data_line is '':
            space_found = True
        # If we found the space, we add to the fold instructions
        if space_found:
            folds.append(data_line)
        # If there was no space yet, we are still appending dot coordinates
        else:
            dots_coord.append(data_line)
    # Folds will also get the space in the first position, we are removing it
    folds = folds[1:]
    # Build the dot map
    dots = np.zeros((len(dots_coord), 2), dtype=int)
    for i in range(len(dots_coord)):
        # Find the x and y position of the dot, and add them to a simple dot position list
        re_matches = re.search(r'(\d+),(\d+)', dots_coord[i])
        dots[i, 1] = re_matches.group(1)
        dots[i, 0] = re_matches.group(2)

    return dots, folds


def part_one() -> int:
    # Get dot instructions and fold instructions
    dots, folds = get_input()

    # Initialize the dot paper based on max dot data, + 1 needed because there is also a 0 position
    dot_paper = np.zeros((max(dots[:, 0]) + 1, max(dots[:, 1]) + 1), dtype=int)
    # Create the dot paper by adding each dot
    for dot in dots:
        dot_paper[dot[0], dot[1]] = 1

    # Get the first fold we have: along which axis, and at which position the fold occurs
    re_matches = re.search(r'\D+(\w)=(\d+)', folds[0])
    along = re_matches.group(1)
    fold = int(re_matches.group(2))

    # Check if the fold is along x or y
    if along == 'y':
        # Get top part
        part_1 = dot_paper[:fold, :]
        # Get bottom part and flip upside down to mimic the fold
        part_2 = np.flipud(dot_paper[fold+1:, :])
    elif along == 'x':
        # Get left part
        part_1 = dot_paper[:, :fold]
        # Get right part and flip left to right to mimic the fold
        part_2 = np.fliplr(dot_paper[:, fold+1:])
    else:
        print('Error: Could not find fold!')
        part_1 = -1
        part_2 = -1

    # Add the two parts
    dot_paper = np.clip(part_1 + part_2, 0, 1)

    # Return the sum of all dots after making sure that each dot only counts once in the same position
    return int(np.sum(dot_paper))


def part_two() -> np.ndarray:
    # Get dot instructions and fold instructions
    dots, folds = get_input()

    # Initialize the dot paper based on max dot data, + 1 needed because there is also a 0 position
    dot_paper = np.zeros((max(dots[:, 0]) + 1, max(dots[:, 1]) + 1), dtype=int)
    # Create the dot paper by adding each dot
    for dot in dots:
        dot_paper[dot[0], dot[1]] = 1

    # Go through all folds
    for i in range(len(folds)):
        # along which axis, and at which position the fold occurs
        re_matches = re.search(r'\D+(\w)=(\d+)', folds[i])
        along = re_matches.group(1)
        fold = int(re_matches.group(2))

        # Check if the fold is along x or y
        if along == 'y':
            # Get top part
            part_1 = dot_paper[:fold, :]
            # Get bottom part and flip upside down to mimic the fold
            part_2 = np.flipud(dot_paper[fold + 1:, :])
        elif along == 'x':
            # Get left part
            part_1 = dot_paper[:, :fold]
            # Get right part and flip left to right to mimic the fold
            part_2 = np.fliplr(dot_paper[:, fold + 1:])
        else:
            print('Error: Could not find fold!')
            part_1 = -1
            part_2 = -1

        # Make sure we clip to a max of 1 as instructed
        dot_paper = np.clip(part_1 + part_2, 0, 1)

    # Return the dot paper (it's recommended to look at it here with a debugger to get the letters)
    return dot_paper


def main():
    print('This many dots are visible after completing the first fold instruction:', part_one())
    print('The code to activate the infrared thermal imaging camera system is:\n', part_two())


if __name__ == '__main__':
    main()
