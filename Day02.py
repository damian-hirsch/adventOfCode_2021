# Get data from .txt file
def get_input():
    # Split lines and write each line to list
    with open('Input/Day02.txt', 'r') as file:
        data = file.read().splitlines()
    return data


def part_one(data: list) -> int:
    # Initialize variables at 0
    horizontal = 0
    depth = 0
    # For each data line
    for data_line in data:
        # Split the line at the space into a command and a distance
        (commands, distance) = data_line.split(" ")
        # Forward commands adds to horizontal
        if commands == 'forward':
            horizontal += int(distance)
        # Down command increased to depth
        elif commands == 'down':
            depth += int(distance)
        # Up command decreases depth
        elif commands == 'up':
            depth -= int(distance)
        # Simple error check
        else:
            print("Error: Couldn't find command")
    return horizontal*depth


def part_two(data: list) -> int:
    # Initialize variables at 0
    horizontal = 0
    depth = 0
    aim = 0
    # For each data line
    for data_line in data:
        # Split the line at the space into a command and a distance
        (commands, distance) = data_line.split(" ")
        # Forward commands adds to horizontal and increases depth by multiplying with aim
        if commands == 'forward':
            horizontal += int(distance)
            depth += int(distance) * aim
        # Down command increases aim
        elif commands == 'down':
            aim += int(distance)
        # Up command decreases aim
        elif commands == 'up':
            aim -= int(distance)
        # Simple error check
        else:
            print("Error: Couldn't find command")
    return horizontal*depth


def main():
    print('Final horizontal position multiplied by final depth: ', part_one(get_input()))
    print('Final horizontal position multiplied by final depth: ', part_two(get_input()))


if __name__ == '__main__':
    main()
