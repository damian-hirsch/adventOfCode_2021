import numpy as np


def get_input() -> np.ndarray:
    # Split lines and write each line to list
    with open('Input/Day07.txt', 'r') as file:
        data = file.read().splitlines()
        # Split the numbers and map to a list as integers
        data = list(map(int, data[0].split(',')))
    # Convert the list to an np array
    return np.asarray(data)


# Gauss' summation function (gauss(n) = 1+2+...+n) to calculate fuel cost in part 2
def gauss(n):
    return (n+1)*n/2


def part_one(data: np.ndarray) -> int:
    # Initialize fuel array, it can max be as long as the furthest position, anything right of that makes no sense
    fuel = np.zeros(max(data))

    # Cycle through all positions to that max position and calculate the fuel cost
    for i in range(len(fuel)):
        fuel[i] = np.sum(np.abs(data - i))

    # Return the minimum fuel cost
    return int(np.min(fuel))


# Because of the mathematical beauty of this problem, we know that the perfect distance has to be at the mean
def part_two(data: np.ndarray) -> int:
    # Because the mean is not an integer number, let's check both the upper and lower limit, and take the smaller one
    # Lower
    distance1 = np.abs(data - np.floor(np.mean(data)))
    fuel1 = np.sum(gauss(distance1))
    # Upper
    distance2 = np.abs(data - np.ceil(np.mean(data)))
    fuel2 = np.sum(gauss(distance2))
    # Return smaller
    return int(min(fuel1, fuel2))


def main():
    print('They spend this much fuel for part 1:', part_one(get_input()))
    print('They spend this much fuel for part 2:', part_two(get_input()))


if __name__ == '__main__':
    main()
