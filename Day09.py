import numpy as np
from scipy.ndimage.measurements import label


def get_input() -> np.ndarray:
    # Split lines and write each line to list
    with open('Input/Day09.txt', 'r') as file:
        data = file.read().splitlines()
    # Get row and column length
    rows = len(data)
    columns = len(data[0])
    # Initialize array
    height_map = np.zeros((rows, columns), dtype=int)

    # Fill the array with values from the data
    for i in range(rows):
        height_map[i, :] = list(map(int, list(data[i])))

    return height_map


def part_one(height_map: np.ndarray) -> int:
    # Get rows and columns shape
    num_rows, num_columns = height_map.shape
    # Pad the array with 9s so we don't need to worry about the edges
    height_map_padded = np.pad(height_map, 1, 'constant', constant_values=9)

    # Check every point and calculate risk
    sum_risk = 0
    for i in range(num_columns):
        for j in range(num_rows):
            # Define values to avoid packing them all in the condition and make it less readable
            point = height_map_padded[j+1, i+1]
            top = height_map_padded[j, i+1]
            right = height_map_padded[j+1, i+2]
            bottom = height_map_padded[j+2, i+1]
            left = height_map_padded[j+1, i]
            if point < top and point < right and point < bottom and point < left:
                # The risk is the point's height + 1
                sum_risk += point + 1

    return sum_risk


def part_two(height_map: np.ndarray) -> int:
    # We will use a function from the scipy library for this problem
    # First, we need to define how the points in the basin are allowed to touch each other = no diagonals!
    structure = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    # Second, we convert the map to 0s (all 9s) and 1s (everything else) to be able to use it with the scipy function
    # Multiplication by one to convert booleans back to integers
    height_map_binary = (height_map < 9) * 1
    # Use the label function to label all basins (each basins has its own digit) and return how many basins it found
    height_map_labeled, num_components = label(height_map_binary, structure)

    # To count the number of labels in each basin, we initialize an array to keep track of it
    counts = np.zeros(num_components, dtype=int)
    # Count the labels in each basin to get the basin size
    for i in range(num_components):
        counts[i] = np.count_nonzero(height_map_labeled == (i + 1))

    # Find the 3 biggest basins by sorting the array, and then multiply the last 3 numbers of that array together to
    # get the final result
    sorted_index_counts = np.argsort(counts)
    sorted_counts = counts[sorted_index_counts]
    return int(np.prod(sorted_counts[-3:]))


def main():
    print('The sum of the risk levels of all low points on the heightmap is:', part_one(get_input()))
    print('Multiplying the sizes of the three largest basins together equals:', part_two(get_input()))


if __name__ == '__main__':
    main()
