import numpy as np
import re


# Get data from .txt file
def get_input():
    # Split lines and write each line to list
    with open('Input/Day12.txt', 'r') as file:
        data = file.read().splitlines()
    return data


# Function to build the initial connection matrix
def build_connections(data: list) -> (np.ndarray, dict):
    # data: list of connections
    # cave_connections: connection matrix
    # dict_cave2idx: dictionary to track indices

    # First, find all caves usings sets
    cave_list = set()
    for data_line in data:
        re_matches = re.search(r'(\w+)-(\w+)', data_line)
        match1 = re_matches.group(1)
        match2 = re_matches.group(2)
        cave_list.add(match1)
        cave_list.add(match2)

    # Converting to a list and sorting makes it easier later for debugging
    cave_list = list(cave_list)
    cave_list.sort()

    # Initialize cave_connection matrix
    cave_connections = np.zeros((len(cave_list), len(cave_list)), dtype=int)
    # Create cave to index dictionary
    dict_cave2idx = dict(zip(cave_list, np.arange(len(cave_list))))
    # Build connections
    for data_line in data:
        re_matches = re.search(r'(\w+)-(\w+)', data_line)
        match1 = re_matches.group(1)
        match2 = re_matches.group(2)
        cave_connections[dict_cave2idx[match1], dict_cave2idx[match2]] = 1
        # Cave paths are symmetric = you can move in both directions
        cave_connections[dict_cave2idx[match2], dict_cave2idx[match1]] = 1
    # 'start' cannot be revisited
    cave_connections[:, dict_cave2idx['start']] = 0
    # Once you reach 'end', you cannot go back
    cave_connections[dict_cave2idx['end'], :] = 0

    return cave_connections, dict_cave2idx


def cave_crawler(current_cave: str, cave_connections: np.ndarray, dict_cave2idx: dict, count: int) -> int:
    # current_cave: the cave we are at now
    # cave_connections: latest connection matrix
    # dict_cave2idx: dictionary for cave to index
    # count: number of paths currently found
    # count: new number of paths found

    # If the current cave is 'end', we are done and increase count by 1
    if current_cave == 'end':
        count += 1
    else:
        # Check if there are any other caves to visit from the current position
        num_connections = np.sum(cave_connections[dict_cave2idx[current_cave], :])

        # If there are, do the following
        if num_connections >= 1:
            # Invert dictionary
            dict_idx2cave = {v: k for k, v in dict_cave2idx.items()}
            # Find next caves
            next_caves_idx = np.where(cave_connections[dict_cave2idx[current_cave], :] == 1)
            next_caves = []
            # Collect all caves to go to next (using names for easier debugging)
            for cave in next_caves_idx[0]:
                next_caves.append(dict_idx2cave[cave])

            # Loop through each of these caves
            for next_cave in next_caves:
                # Copy the connection matrix for a potential recursive call
                next_cave_connections = cave_connections.copy()
                # If the current and next cave are lower
                if current_cave.islower() and next_cave.islower():
                    # The current cave shouldn't be able to visit any further caves
                    next_cave_connections[dict_cave2idx[current_cave], :] = 0
                    # The next cave shouldn't be able to visit the current cave (not, necessary, but speeds up)
                    next_cave_connections[dict_cave2idx[next_cave], dict_cave2idx[current_cave]] = 0
                # If the current cave is upper and next cave is lower
                elif current_cave.isupper() and next_cave.islower():
                    # The upper cave shouldn't be able to visit the lower cave anymore in a further iteration
                    next_cave_connections[dict_cave2idx[current_cave], dict_cave2idx[next_cave]] = 0
                # If the current cave is lower and next cave is lower
                elif current_cave.islower() and next_cave.isupper():
                    # The current cave shouldn't be able to visit any further caves
                    next_cave_connections[dict_cave2idx[current_cave], :] = 0
                    # The upper cave shouldn't be able to visit the lower cave anymore in a further iteration
                    next_cave_connections[dict_cave2idx[next_cave], dict_cave2idx[current_cave]] = 0
                # If the current and next cave are upper
                elif current_cave.isupper() and next_cave.isupper():
                    # Nothing happens (shouldn't exist, because this way you can end up circling as long as you want)
                    pass
                else:
                    print('Error: Case does not exist!')
                # If there is a potential next cave, call the function recursively
                count = cave_crawler(next_cave, next_cave_connections, dict_cave2idx, count)

    return count


def cave_crawler_part2(current_cave: str, cave_connections: np.ndarray, dict_cave2idx: dict, count: int, seen: list,
                       visited: list) -> int:
    # current_cave: the cave we are at now
    # cave_connections: latest connection matrix
    # dict_cave2idx: dictionary for cave to index
    # count: number of paths currently found
    # seen: lower caves we have already visited
    # visited: list of previously visited caves (for debugging)
    # count: new number of paths found

    # Copy the visited list for potential further recursion
    new_visited = visited.copy()
    # Append the current cave
    new_visited.append(current_cave)
    # If the current cave is 'end', we are done and increase count by 1, uncomment for printing the found paths
    if current_cave == 'end':
        count += 1
        # print(str(count) + ': ' + ','.join(new_visited))
    else:
        # Check if there are any other caves to visit from the current position
        num_connections = np.sum(cave_connections[dict_cave2idx[current_cave], :])

        # If there are, do the following
        if num_connections >= 1:
            # Invert dictionary
            dict_idx2cave = {v: k for k, v in dict_cave2idx.items()}
            # Find next caves
            next_caves_idx = np.where(cave_connections[dict_cave2idx[current_cave], :] == 1)
            next_caves = []
            # Collect all caves to go to next (using names for easier debugging)
            for cave in next_caves_idx[0]:
                next_caves.append(dict_idx2cave[cave])

            # Loop through each of these caves
            for next_cave in next_caves:
                # Copy the connection matrix and seen list for a potential recursive call
                next_cave_connections = cave_connections.copy()
                next_seen = seen.copy()
                # If current cave is upper
                if current_cave.isupper():
                    # Check if next cave in seen OR if we already used our double visit
                    if next_cave in next_seen or len(next_seen) > len(set(next_seen)):
                        # Block the paths from the current cave to the next caves
                        next_cave_connections[dict_cave2idx[current_cave], dict_cave2idx[next_cave]] = 0
                        # Block all other paths from the current caves to all caves that already have been visited
                        for cave in next_seen:
                            next_cave_connections[dict_cave2idx[current_cave], dict_cave2idx[cave]] = 0
                    # Next cave not in seen and we have no double visits yet
                    else:
                        # Nothing happens (same as two upper caves would exist)
                        pass
                # Elif current cave is lower
                elif current_cave.islower():
                    # Check if current cave in seen OR if we already used our double visit
                    if current_cave in next_seen or len(next_seen) > len(set(next_seen)):
                        # Block all paths of each cave that was in seen and block the path from the next cave to them
                        for cave in next_seen:
                            next_cave_connections[dict_cave2idx[cave], :] = 0
                            next_cave_connections[dict_cave2idx[next_cave], dict_cave2idx[cave]] = 0
                        # Check if next cave in seen OR if we already used our double visit
                        if next_cave in next_seen or len(next_seen) > len(set(next_seen)):
                            # Block all paths of each cave that was in seen and block the path from the next cave to
                            # the current cave
                            next_cave_connections[dict_cave2idx[current_cave], :] = 0
                            next_cave_connections[dict_cave2idx[next_cave], dict_cave2idx[current_cave]] = 0
                        # If the next cave was not seen and we haven't used our double visit
                        else:
                            # Block all paths of each cave that was in seen and block the path from the next cave to
                            # the current cave
                            next_cave_connections[dict_cave2idx[current_cave], :] = 0
                            next_cave_connections[dict_cave2idx[next_cave], dict_cave2idx[current_cave]] = 0
                    # If the current cave was not seen and if we haven't used the double visit
                    else:
                        # Check if next cave in seen OR if we already used our double visit
                        if next_cave in next_seen or len(next_seen) > len(set(next_seen)):
                            # If next cave was seen, block the path from current to it
                            next_cave_connections[dict_cave2idx[current_cave], dict_cave2idx[next_cave]] = 0
                            # Block the paths from current to all other caves in seen
                            for cave in next_seen:
                                next_cave_connections[dict_cave2idx[current_cave], dict_cave2idx[cave]] = 0
                        # If next cave was not seen, then nothing happens (same as two upper caves would exist)
                        else:
                            pass
                    # Append current cave to seen cave
                    next_seen.append(current_cave)
                else:
                    print('Error: Case does not exist!')
                # If there is a potential next cave, call the function recursively
                count = cave_crawler_part2(next_cave, next_cave_connections, dict_cave2idx, count, next_seen,
                                           new_visited)

    return count


def part_one(data: list) -> int:
    cave_connections, dict_indices = build_connections(data)
    count = cave_crawler('start', cave_connections, dict_indices, 0)

    return count


def part_two(data: list) -> int:
    cave_connections, dict_indices = build_connections(data)
    count = cave_crawler_part2('start', cave_connections, dict_indices, 0, [], [])

    return count


def main():
    print('This many paths through the cave system exist that visit small caves at most once:', part_one(get_input()))
    print('This many paths through the cave system exist that visit one small cave twice:', part_two(get_input()))


if __name__ == '__main__':
    main()
