import re


# Get data from .txt file
def get_input() -> tuple:
    # Get the string
    with open('Input/Day17.txt', 'r') as file:
        data = file.read()
    # Regex to get all the digits out of the string
    re_matches = re.search(r'\D+=(.?\d+)\.{2}(.?\d+)\D+=(.?\d+)\.{2}(.?\d+)', data)
    x_min = int(re_matches.group(1))
    x_max = int(re_matches.group(2))
    y_min = int(re_matches.group(3))
    y_max = int(re_matches.group(4))
    # Return x_min, x_max, y_min, y_max as a tuple
    return x_min, x_max, y_min, y_max


# Function for Gauss' formula
def gauss(n: int) -> int:
    return int(n*(n+1)/2)


def calc_next_step(x_start: int, y_start: int, x_velocity: int, y_velocity: int) -> (int, int, int, int):
    # Calculate the new positions after the step
    x_end = x_start + x_velocity
    y_end = y_start + y_velocity
    # Only reduce the x_velocity if it hasn't reached 0 yet
    if x_velocity > 0:
        x_velocity -= 1
    # The y velocity continues to decrease
    y_velocity -= 1

    return x_end, y_end, x_velocity, y_velocity


def part_one(data: tuple) -> int:
    # Get data
    x_min, x_max, y_min, y_max = data

    # It doesn't matter how high we shoot up, we will get back to the 0 line. At that point it's only important.
    # what's the next step size. The height is maximized, when the last step is as big as possible. The last step is
    # as big as possible if we go all the way to y_min. Note that the last step will be one higher than the initial
    # velocity.
    y_velocity = abs(y_min) - 1

    # Max height can be calculated using Gauss' formula
    return gauss(y_velocity)


def part_two(data: tuple) -> int:
    # Get data
    x_min, x_max, y_min, y_max = data
    # Initialize counter
    counter = 0
    # x cannot be negative with the input (positive x), the max velocity is when x_max is reached in one step
    for x_velocity_loop in range(0, x_max + 1):
        # y can not be lower than the minimum y, and as seen before, its max is the positive minimum minus 1 (part 1)
        for y_velocity_loop in range(y_min, -y_min):
            # Initialize velocities from loop
            x_velocity = x_velocity_loop
            y_velocity = y_velocity_loop
            # Calculate first step
            x, y, x_velocity, y_velocity = calc_next_step(0, 0, x_velocity, y_velocity)
            # Wait for the first variable to hit the target
            while x < x_min and y > y_max:
                x, y, x_velocity, y_velocity = calc_next_step(x, y, x_velocity, y_velocity)
            # If x is in target, and y is still < y_min, wait for y
            while x_min <= x <= x_max and y > y_max:
                x, y, x_velocity, y_velocity = calc_next_step(x, y, x_velocity, y_velocity)
            # If y is in target, and x is still < x_min, wait for x
            while x < x_min and y_min <= y <= y_max:
                x, y, x_velocity, y_velocity = calc_next_step(x, y, x_velocity, y_velocity)
            # If both are in target after all these steps, increase count
            if x_min <= x <= x_max and y_min <= y <= y_max:
                counter += 1

    return counter


def main():
    print('The highest y position the probe can reach on any trajectory is:', part_one(get_input()))
    print('Number of distinct initial velocities to be within the target area after any step:', part_two(get_input()))


if __name__ == '__main__':
    main()
