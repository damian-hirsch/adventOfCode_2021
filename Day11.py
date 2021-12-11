import numpy as np


# Get data from .txt file
def get_input():
    # Split lines and write each line to list
    with open('Input/Day11.txt', 'r') as file:
        data = file.read().splitlines()
    # Initialize np array
    octopuses = np.zeros(shape=(len(data[0]), len(data)), dtype=int)
    # Convert data to np array splitting each number in its own cell
    for i in range(len(data)):
        octopuses[i, :] = list(map(int, [number for number in data[i]]))
    return octopuses


# Function to add the flashes to neighbors
def flash(y: int, x: int, octopuses: np.ndarray) -> np.ndarray:
    # y: y position of the flash
    # x: x position of the flash
    # octopuses: grid of octopus values

    # Add a padding so we don't need to bother about edge effects
    octopuses = np.pad(octopuses, 1, 'constant', constant_values=0)
    # Add +1 to x and y to account for the padding
    x += 1
    y += 1
    # Add +1 to the value of all neighbors
    for j in range(y - 1, y + 1 + 1):
        for i in range(x - 1, x + 1 + 1):
            octopuses[j, i] += 1
    # Set the flashing octopus to 0
    octopuses[y, x] = 0
    # Return the updated grid without the padding
    return octopuses[1:-1, 1:-1]


def part_one(octopuses: np.ndarray, rounds: int) -> int:
    num_flashes = 0

    # Step through the rounds
    for t in range(rounds):
        # Add +1 to each octopus for every round
        octopuses += 1
        # Initialize variables for later
        is_flashing = True
        flashed = []
        # While we still have flashing octopuses repeat
        while is_flashing:
            # Find all octopuses with a value of 10 or higher (this is possible if one gets multiple flashes from
            # neighboring octopuses that where in the previous np.where
            y_array, x_array = np.where(octopuses >= 10)
            # If we couldn't find any with a value of 10 or more, we have no (more) and are done
            if len(x_array) == 0:
                is_flashing = False
            # Else we go through our findings and add the flashes with our function
            else:
                for i in range(len(x_array)):
                    # Add flashes to neighbors with our function
                    octopuses = flash(y_array[i], x_array[i], octopuses)
                    # Add to flashed array, which we need for later to truly reset all octopuses to 0
                    flashed.append([y_array[i], x_array[i]])
                    # Increase the flash count
                    num_flashes += 1

        # Set all octopuses that flashed to 0 (this avoids having some missing ones, that got a flash by a neighbor
        # that was triggered after we set them to 0 already)
        for j in range(len(flashed)):
            octopuses[flashed[j][0], flashed[j][1]] = 0
    # Return the number of flashes
    return num_flashes


def part_two(octopuses: np.ndarray) -> int:
    # Find the number of total octopuses we have
    num_octopuses = octopuses.shape[0] * octopuses.shape[1]
    # Initialize round counter
    t = 0
    while True:
        # Increase the counter per round
        t += 1
        # Add +1 to each octopus for every round
        octopuses += 1
        # Initialize variables for later
        is_flashing = True
        flashed = []
        # While we still have flashing octopuses repeat
        while is_flashing:
            # Find all octopuses with a value of 10 or higher (this is possible if one gets multiple flashes from
            # neighboring octopuses that where in the previous np.where
            y_array, x_array = np.where(octopuses >= 10)
            # If we couldn't find any with a value of 10 or more, we have no (more) and are done
            if len(x_array) == 0:
                is_flashing = False
            # Else we go through our findings and add the flashes with our function
            else:
                for i in range(len(x_array)):
                    # Add flashes to neighbors with our function
                    octopuses = flash(y_array[i], x_array[i], octopuses)
                    # Add to flashed array, which we need for later to truly reset all octopuses to 0
                    flashed.append([y_array[i], x_array[i]])

        # Set all octopuses that flashed to 0 (this avoids having some missing ones, that got a flash by a neighbor
        # that was triggered after we set them to 0 already)
        for j in range(len(flashed)):
            octopuses[flashed[j][0], flashed[j][1]] = 0
        # The the number of octopuses that flash is equal to the number of total octopuses, we are done
        if len(flashed) == num_octopuses:
            break
    # Return the round number
    return t


def main():
    print('Number of total flashes are there after 100 steps:', part_one(get_input(), 100))
    print('Number of total flashes are there after 100 steps:', part_two(get_input()))


if __name__ == '__main__':
    main()
