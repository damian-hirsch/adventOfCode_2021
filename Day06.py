import numpy as np


def get_input() -> np.ndarray:
    # Split lines and write each line to list
    with open('Input/Day06.txt', 'r') as file:
        data = file.read().splitlines()
        # Split the numbers and map to a list as integers
        data = list(map(int, data[0].split(',')))
    # Convert the list to an np array
    return np.asarray(data)


# The problem is computationally critical, that's why we don't keep track of every fish, but only how many we have in
# each group
def part_one_and_two(data: np.ndarray, days: int) -> np.ndarray:
    # Array to track the fish count in each group
    fish_count = np.zeros(9, dtype='int64')
    # Fill this array with the initial count
    for i in range(len(fish_count)):
        fish_count[i] = np.count_nonzero(data == i)

    # Start growing the fish
    for d in range(days):
        # Keep track of how many parent fish = how many fish go back to 6 days = how many new fish
        parent_fish = fish_count[0]
        # Shift the fish count array one day forward (this is a very inexpensive operation compared to tracking the
        # fish, appending to a list every time, etc.)
        fish_count = np.roll(fish_count, -1)
        # Add the parent fish back to the fish that are now also at day 7 (former baby fish coming from day 8)
        fish_count[6] += parent_fish
        # Add the new fish to the end of the array --> not needed because the roll takes care of it parent_fish =
        # new_fish
        # fish_count[8] = new_fish

    return np.sum(fish_count)


def main():
    print('Lantern fish after 80 days:', part_one_and_two(get_input(), 80))
    print('Lantern fish after 256 days:', part_one_and_two(get_input(), 256))


if __name__ == '__main__':
    main()
