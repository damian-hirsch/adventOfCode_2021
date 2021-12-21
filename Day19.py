import numpy as np
import re
from collections import defaultdict

"""
Note: This problem was challenging, I tried a few approaches until I found the right one:
1. Correlation of 3D volumes --> computationally too expensive (memory and processing)
2. Checking only in 1D in a first step --> will not find the correct solution, because there are too many overlaps
3. Checking in 2D in a first step --> computationally expensive and tracking of indices makes things complicated

Approach used: With the assumption that the distances between beacons are unique, I used the Euclidean distance to get a
computationally cheap check if we have a match or not. The approach can probably be optimized even more, but it does the
job well enough.

Also note that getting the rotations correctly is a challenge in itself. One needs to think about what combinations are
possible to get the 24 (instead of 48 for a brute force approach)
"""

# The rotations need to be thought through and properly defined. Used the right-hand rule to get to these:
ROTATIONS = [([0, 1, 2], [1, 1, 1]), ([0, 1, 2], [1, -1, -1]), ([0, 1, 2], [-1, 1, -1]), ([0, 1, 2], [-1, -1, 1]),
             ([0, 2, 1], [-1, -1, -1]), ([0, 2, 1], [1, 1, -1]), ([0, 2, 1], [1, -1, 1]), ([0, 2, 1], [-1, 1, 1]),
             ([1, 2, 0], [1, 1, 1]), ([1, 2, 0], [1, -1, -1]), ([1, 2, 0], [-1, 1, -1]), ([1, 2, 0], [-1, -1, 1]),
             ([1, 0, 2], [-1, -1, -1]), ([1, 0, 2], [1, 1, -1]), ([1, 0, 2], [1, -1, 1]), ([1, 0, 2], [-1, 1, 1]),
             ([2, 0, 1], [1, 1, 1]), ([2, 0, 1], [1, -1, -1]), ([2, 0, 1], [-1, 1, -1]), ([2, 0, 1], [-1, -1, 1]),
             ([2, 1, 0], [-1, -1, -1]), ([2, 1, 0], [1, 1, -1]), ([2, 1, 0], [1, -1, 1]), ([2, 1, 0], [-1, 1, 1])]


def get_input() -> list:
    with open('Input/Day19.txt', 'r') as file:
        data = file.read().splitlines()
    # Initialize list of scanner data and list of coordinates
    scanners = []
    coordinates = []
    # For each data_line in data
    for data_line in data:
        # If we have a separator line, empty coordinates to prepare for next scanner data
        if data_line[0:3] == '---':
            coordinates = []
        # If we don't have a space line, keep appending coordinates
        elif data_line != '':
            coordinates.append(list(map(int, re.findall(r'-?\d+', data_line))))
        # If we have a space line, we are at the end of this scanner's data and can append all coordinates
        else:
            scanners.append(coordinates)
    # Add the last scanner, because there is no space line
    scanners.append(coordinates)
    return scanners


# Find the distance between all points in a list, there will be n * (n-1) / 2 values
def distance(list1: list) -> set:
    # Initialize the set of distances (we want to avoid double counts for distances of the same beacons)
    dist = set()
    # Loop through all beacons
    for i in range(len(list1)):
        for j in range(len(list1)):
            if i != j:
                # Calculate the Euclidean distance between two points
                dist.add(np.linalg.norm(np.asarray(list1[i]) - np.asarray(list1[j])))
    # Return the set of distances
    return dist


# Rotation of the beacons of a scanner
def rotate(beacon_array: np.ndarray, rotation_num: int) -> np.ndarray:
    # Get rotation
    axis, signs = ROTATIONS[rotation_num]
    # Initialize rotated array
    beacon_array_rotated = np.zeros(beacon_array.shape, dtype=int)
    # Rotate every coordinate according to the rotations and signs
    for i in range(len(axis)):
        beacon_array_rotated[:, i] = beacon_array[:, axis[i]] * signs[i]
    # Return the rotated array
    return beacon_array_rotated


# Shift and rotate the scanner data until it's in our (0, 0) coordinate system
def shift_and_rotate(beacons: list, scanner: list) -> (np.ndarray, tuple, tuple):
    # Convert to np.array for easier math
    beacons = np.array(beacons)
    scanner = np.array(scanner)
    # Initialize shifted and rotated array, the translations, and the rotation
    scanner_shifted_and_rotated = scanner.copy()
    translation = ()
    rotation = ()

    # Apply rotation to scanner and then try to find the shifts, keep rotating until found
    # We know there has to be a solution at this point, based on our distance check before calling this function
    for i in range(len(ROTATIONS)):
        # Initialize shift dictionary
        shifts = defaultdict(int)
        # Get next rotation
        rotation = ROTATIONS[i]
        # Rotate the scanner according to the latest rotation
        scanner_rotated = rotate(scanner, i)
        # Compare all known beacons with the data from the (rotated) scanner
        for beacon in beacons:
            for scanner_beacon in scanner_rotated:
                # Calculate the distances between all points
                dx, dy, dz = beacon - scanner_beacon
                # Add the results to the dictionary (note that if we have the correct orientation of the scanner,
                # we will obviously get multiple shifts with the same outcome. This is exactly what we are trying to
                # find
                shifts[dx, dy, dz] += 1
        # Check if we have a shift that occurred for at least 12 beacons (see comment above)
        most_common_shift = max(shifts.values())
        # If we don't have one, we need to keep rotating
        if most_common_shift < 12:
            continue
        # If we do, get the translations and add them to the rotated scanner data to get into the (0, 0) coordinate
        # system
        else:
            translation = max(shifts, key=shifts.get)
            scanner_shifted_and_rotated = scanner_rotated + translation
            # No need to check further
            break
    # Return the shifted and rotated scanner data, the translations, and rotations
    return scanner_shifted_and_rotated, translation, rotation


# Calculates the Manhattan distance between to points
def manhattan_distance(pos1: tuple, pos2: tuple) -> int:
    # Unpack tuples because that's our translation input data (= scanner positions)
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    # Calculate the distance and return it
    return int(abs(x1-x2) + abs(y1-y2) + abs(z1-z2))


def part_one(scanners: list) -> (int, list):
    # Assume we are in the reference of scanner 0 and calculate the distances of all points to each other
    # The scanner positions of scanner 0 are automatically our first detected beacons, we initialize it as a set
    beacons = set(tuple(i) for i in scanners[0])
    # Calculate all the distances between those beacons
    dist = distance(list(beacons))
    # Initialize array of translations
    translations = np.zeros((len(scanners)), dtype=tuple)
    # Translation of scanner 0 is (0, 0, 0)
    translations[0] = (0, 0, 0)
    # Initialize array of rotations
    rotations = np.zeros((len(scanners)), dtype=tuple)
    # The rotation for scanner 0 is x, y, z, all in the positive direction
    rotations[0] = ([0, 1, 2], [1, 1, 1])
    # Scanner 0 is hence found
    found = [0]

    # While we haven't found all scanners, we keep going
    while len(found) < len(scanners):
        # Cycle through the scanners
        for i in range(len(scanners)):
            # If it was already found, skip it
            if i in found:
                continue
            else:
                # Calculate the distance for the scanner and get a quick and computationally inexpensive way to check
                # if we have an overlap
                dist_candidate = distance(scanners[i])
                num_overlap = len(dist.intersection(dist_candidate))
                # If we need at least 12 scanner that overlap, that means we need at least n*(n-1)/2 overlaps,
                # where n = 12, so that means we need at least 66 matches
                if num_overlap >= 66:
                    # If we found an overlap, we need to remap the new beacons to the scanner 0 coordinate system
                    new_beacons, translations[i], rotations[i] = shift_and_rotate(list(beacons), scanners[i])
                    # Add the new beacons to our beacons list
                    new_beacons = set(tuple(i) for i in new_beacons)
                    beacons = beacons.union(set(new_beacons))
                    # Recalculate all the distances
                    dist = distance(list(beacons))
                    # Append the scanner to the found list
                    found.append(i)
                    # Printing statement for tracking because it takes a bit longer
                    print('Found:', round(len(found)/len(scanners) * 100, 2), '%')

    return len(beacons), translations


def part_two(scanner_coordinates: np.ndarray) -> int:
    # Initialize maximum distance as 0
    max_distance = 0
    # Compare every combinations of scanners
    for scanner_coord1 in scanner_coordinates:
        for scanner_coord2 in scanner_coordinates:
            # Calculate the Manhattan distance between the selected two scanners
            current_distance = manhattan_distance(scanner_coord1, scanner_coord2)
            # If this distance is larger than our current max, update the maximum distance
            if current_distance > max_distance:
                max_distance = current_distance

    return max_distance


def main():
    num_beacons, scanner_coordinates = part_one(get_input())
    print('Number of beacons:', num_beacons)
    print('The largest Manhattan distance between any two scanners is:', part_two(scanner_coordinates))


if __name__ == '__main__':
    main()
