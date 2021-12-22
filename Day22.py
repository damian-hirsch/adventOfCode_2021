import numpy as np
import re


"""
Note: 
Part 1: Straight-forward using a numpy array to track on/off cuboids 
Part 2: Too memory intensive to use the approach from Part 1. Instead, we need to keep track of the cuboid regions (not
        the single cuboid). First, I tried to manage everything with a functional approach, but tracking the indices and
        order of the overlapping cuboid regions got challenging, so I decided to use an object-oriented approach to keep
        it simpler.
"""


class CuboidRegion:
    # Initialize cuboid region
    def __init__(self):
        self.z1 = None
        self.z2 = None
        self.y1 = None
        self.y2 = None
        self.x1 = None
        self.x2 = None

        self.on_off = ''

    # Method to calculate the overlapping cuboid region
    def overlap(self, cr2: 'CuboidRegion'):
        # Check if we even have an overlap, if not return no cuboid region
        # in z
        if cr2.z2 < self.z1 or self.z2 < cr2.z1:
            return None
        # y
        if cr2.y2 < self.y1 or self.y2 < cr2.y1:
            return None
        # z
        if cr2.x2 < self.x1 or self.x2 < cr2.x1:
            return None

        # If we do have an overlap, calculate the coordinates of the cuboid region
        z_1 = max(cr2.z1, self.z1)
        z_2 = min(cr2.z2, self.z2)
        y_1 = max(cr2.y1, self.y1)
        y_2 = min(cr2.y2, self.y2)
        x_1 = max(cr2.x1, self.x1)
        x_2 = min(cr2.x2, self.x2)

        # From the coordinates, create overlap cuboid region and return it
        overlap_cuboid = CuboidRegion()
        overlap_cuboid.z1 = z_1
        overlap_cuboid.z2 = z_2
        overlap_cuboid.y1 = y_1
        overlap_cuboid.y2 = y_2
        overlap_cuboid.x1 = x_1
        overlap_cuboid.x2 = x_2

        return overlap_cuboid

    # Method to count the cuboids inside the cuboid region, making sure a large value can be stored using np.int64
    def count_cuboids(self) -> np.int64:
        z = np.int64(self.z2 - self.z1 + 1)
        y = np.int64(self.y2 - self.y1 + 1)
        x = np.int64(self.x2 - self.x1 + 1)

        return z * y * x


# Get data from .txt file
def get_input():
    # Split lines and write each line to list
    with open('Input/Day22.txt', 'r') as file:
        data = file.read().splitlines()
    # Convert lines to data arrays
    # Initialize arrays
    on_off = np.zeros((len(data)), dtype=int)
    cuboid_regions = np.zeros((len(data), 6), dtype=int)
    for i, data_line in enumerate(data):
        # Find relevant data using regex
        re_data_line = re.search(r'(\w+)\D+=(-?\d+)..(-?\d+)\D+=(-?\d+)..(-?\d+)\D+=(-?\d+)..(-?\d+)', data_line)
        if re_data_line.group(1) == 'on':
            on_off[i] = 1
        elif re_data_line.group(1) == 'off':
            on_off[i] = 0
        # Cuboid regions with coordinates ordered z1, z2, y1, y2, x1, x2
        cuboid_regions[i, :] = [re_data_line.group(6), re_data_line.group(7), re_data_line.group(4),
                                re_data_line.group(5), re_data_line.group(2), re_data_line.group(3)]

    return on_off, cuboid_regions


def part_one(data: tuple) -> int:
    # Unpack data tuple
    on_off, cuboid_regions = data
    # Initialize cuboid (101 comes from the range -50 to 50 in each dimension)
    cuboid = np.zeros((101, 101, 101), dtype=int)
    # Add + 1 to x2, y2, z2 to avoid a +1 later and interfering with clipping
    cuboid_regions[:, 1::2] += 1
    # Limit cuboid regions to the area we have (mind the + 1 for the second coordinate)
    cuboid_regions = np.clip(cuboid_regions, -50, 50 + 1)
    # Shift all instructions to the cuboid coordinate system (-50, -50, -50) -> (0, 0, 0)
    cuboid_regions += 50
    for i, ins in enumerate(cuboid_regions):
        cuboid[ins[0]:ins[1], ins[2]:ins[3], ins[4]:ins[5]] = on_off[i]

    return int(np.sum(cuboid))


def part_two(data: tuple) -> np.int64:
    # Unpack data tuple
    on_off, cuboid_regions_data = data
    # Initialize list of cuboid regions
    cuboid_regions = []
    # Convert data to cuboid regions
    for i, cuboid_region_data in enumerate(cuboid_regions_data):
        cuboid = CuboidRegion()
        cuboid.z1, cuboid.z2, cuboid.y1, cuboid.y2, cuboid.x1, cuboid.x2 = cuboid_region_data
        cuboid.on_off = on_off[i]
        cuboid_regions.append(cuboid)

    # Initialize seen cuboid regions
    seen_crs = []
    # Loop through every cuboid region from the data
    for cuboid_region in cuboid_regions:
        # Initialize overlapping regions list
        overlapping_crs = []
        # Loop through all regions that have already been seen
        for seen_cr in seen_crs:
            # Check if there is an overlap between these regions and the latest cuboid region from the data
            overlapping_cr = seen_cr.overlap(cuboid_region)
            # If we have an overlapping cuboid region
            if overlapping_cr:
                # The overlap is always the opposite type of the one we compared it to, which is nothing else than
                # activating or deactivating the cuboids inside, whenever we visit them with the corresponding on/off
                # cuboid region. In the end, we just pile activations and deactivations regions (on regions that were
                # once activated, see below) on top of each other. A single cuboid might go through various states
                # through all of the cuboid regions.
                # Example:
                # On-CR1 + partially overlapping On-CR2 --> will create a Off-CR-21 in the overlap between 1 and 2 to
                # account for the double count
                # Add a partially overlapping Off-CR3:
                #   1. creates Off-CR-31 to reduce cuboids in the overlap region 3-1
                #   2. creates Off-CR-32 to reduce cuboids in the overlap region 3-2
                #   3. creates On-CR-3-21 to add back the cuboids that where subtracted twice in the region where all
                #   three CRs where overlapping
                if seen_cr.on_off == 1:
                    overlapping_cr.on_off = 0
                elif seen_cr.on_off == 0:
                    overlapping_cr.on_off = 1
                else:
                    print('Error: On/off not correctly defined')
                # Append this overlapping cuboid region to the overlapping regions list
                overlapping_crs.append(overlapping_cr)

        # If the current cuboid region was of type on, we append it to the seen cuboid regions, if the type was off,
        # it doesn't matter, because we don't need to track the 0s (see also large comment above)
        if cuboid_region.on_off == 1:
            seen_crs.append(cuboid_region)
        # However, we need to add all the overlapping regions, because they define new sub-regions we need to track
        seen_crs += overlapping_crs

    # Initialize cuboid count with long integer for the larger numbers
    cuboid_count = np.int64(0)
    # Loop through every cuboid regions we have seen
    for seen_cr in seen_crs:
        # If it was an on region, we add to the count
        if seen_cr.on_off == 1:
            cuboid_count += seen_cr.count_cuboids()
        # If it was on off region, we subtract from the count
        elif seen_cr.on_off == 0:
            cuboid_count -= seen_cr.count_cuboids()
        else:
            print('Error: On/off not correctly defined')

    # Return the total cuboid count
    return cuboid_count


def main():
    print('Number of cuboids that are on:', part_one(get_input()))
    print('Number of cuboids that are on:', part_two(get_input()))


if __name__ == '__main__':
    main()
