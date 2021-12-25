import numpy as np


# Get data from .txt file
def get_input():
    # Split lines and write each line to list
    with open('Input/Day25.txt', 'r') as file:
        data = file.read().splitlines()
    # Initialize numpy array
    herds = np.zeros((len(data), len(data[0])), dtype=str)
    # Fill each data_line in a numpy row
    for i, data_line in enumerate(data):
        herds[i, :] = list(data_line)

    return herds


def part_one(herds: np.ndarray) -> int:
    # Get shape of the herd
    num_rows, num_cols = herds.shape
    # Initialize variable for while loop
    is_changing = True
    # Step counter
    steps = 0
    while is_changing:
        # East step
        # Find all east facing cucumbers
        east = np.where(herds == '>')
        # Add the potential next step, convert to proper tuple, and convert to set for comparison
        east_target = set(tuple(zip(east[0], (east[1] + 1) % num_cols)))
        # Find all blocked spots
        blocked = np.where(np.logical_or(herds == 'v', herds == '>'))
        # Convert to proper tuple, and convert to set for comparison
        blocked = set(tuple(zip(blocked[0], blocked[1])))
        # Find which moves are possible
        east_move = east_target.difference(blocked)
        # Convert these moves in np.array for easy manipulation of herds array
        east_move = np.asarray(list(east_move))
        # Check if we have any possible moves
        if len(east_move) > 0:
            # Create a copy of the move array to make sure we don't overwrite it
            east_original = east_move.copy()
            # Find the original positions of the cucumbers that can move
            east_original[:, 1] = (east_original[:, 1] + num_cols - 1) % num_cols
            # Delete old positions
            herds[east_original[:, 0], east_original[:, 1]] = '.'
            # Add new positions
            herds[east_move[:, 0], east_move[:, 1]] = '>'

        # South step
        # Find all south facing cucumbers
        south = np.where(herds == 'v')
        # Add the potential next step, convert to proper tuple, and convert to set for comparison
        south_target = set(tuple(zip((south[0] + 1) % num_rows, south[1])))
        # Find all blocked spots (note we need to do this, because the east ones have now new positions)
        blocked = np.where(np.logical_or(herds == 'v', herds == '>'))
        # Convert to proper tuple, and convert to set for comparison
        blocked = set(tuple(zip(blocked[0], blocked[1])))
        # Find which moves are possible
        south_move = south_target.difference(blocked)
        # Convert these moves in np.array for easy manipulation of herds array
        south_move = np.asarray(list(south_move))
        # Check if we have any possible moves
        if len(south_move) > 0:
            # Create a copy of the move array to make sure we don't overwrite it
            south_original = south_move.copy()
            # Find the original positions of the cucumbers that can move
            south_original[:, 0] = (south_original[:, 0] + num_rows - 1) % num_rows
            # Delete old positions
            herds[south_original[:, 0], south_original[:, 1]] = '.'
            # Add new positions
            herds[south_move[:, 0], south_move[:, 1]] = 'v'

        # Check if the cucumbers stopped moving
        if east_move.shape[0] + south_move.shape[0] == 0:
            is_changing = False
        # After the whole process, increase step size
        steps += 1

    # Return the number of steps
    return steps


def main():
    print('Part 1: The first step on which no sea cucumbers move is:', part_one(get_input()))
    print('Part 2: There is only one part, enjoy the holidays!')


if __name__ == '__main__':
    main()
