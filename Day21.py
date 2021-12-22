import numpy as np
import re
from functools import lru_cache


# Get data from .txt file
def get_input() -> np.ndarray:
    # Split lines and write each line to list
    with open('Input/Day21.txt', 'r') as file:
        data = file.read().splitlines()
    # Initialize player position
    player_position = np.zeros(2, dtype=int)
    # Get initial player position
    for i, data_line in enumerate(data):
        player_position_re = re.search(r'(\d+)$', data_line)
        player_position[i] = player_position_re.group(1)
    return player_position


def roll_dice(position: int, points: int, dice_count: int, dice_size: int) -> (int, int):
    # Math expression for summing 3 rolls starting at dice count and then mod of 10
    move = ((3 * (dice_count % dice_size + 1)) + 3) % 10
    # Update board position
    position = ((position + move - 1) % 10) + 1
    # Update points
    points += position

    # Return position, points, and increased dice count
    return position, points, dice_count + 3


def game_normal(player_positions: np.ndarray, player_points: np.ndarray, dice_count: int, limit: int, dice_size: int):
    # While no player has reached the limit, play
    while max(player_points) < limit:
        # Player 1 turn
        player_positions[0], player_points[0], dice_count = roll_dice(player_positions[0], player_points[0],
                                                                      dice_count, dice_size)

        # Check if player 1 won
        if player_points[0] >= limit:
            break

        # Player 2 turn
        player_positions[1], player_points[1], dice_count = roll_dice(player_positions[1], player_points[1],
                                                                      dice_count, dice_size)
        # Check if player 2 won
        if player_points[1] >= limit:
            break

    # Return player points and dice count for calculation
    return player_points, dice_count


def roll_dirac(player_position: int, player_points: int, roll: int):
    # New position in board after roll
    player_position = ((player_position - 1 + roll) % 10) + 1
    # Update player points
    player_points += player_position

    return player_position, player_points


# Thanks to @thibaultj for the inspiration with the lru_cache decorator! Learned something new! The other possible way
# would be to use defaultdict for the function calls and then look them up in a similar way. However, this is much
# easier an cleaner.
# How it works: The lru_cache caches the function calls and "remembers" previously used ones. In an exercise like this,
# where a function is potentially called many, many times, this tremendously speeds up the code
# Note: To use this, all function inputs need to be hashable, this is not the case for numpy arrays!
@lru_cache(maxsize=None)
def count_wins(player, position_0, position_1, points_0, points_1):
    # Check if a player has won and return result
    if points_0 >= 21:
        return 1, 0
    elif points_1 >= 21:
        return 0, 1

    # Initialize wins
    player_wins = np.zeros(2, dtype=np.int64)
    # Get all options for 3 rolls (27 combinations)
    rolls = [(roll1, roll2, roll3) for roll1 in range(1, 4) for roll2 in range(1, 4) for roll3 in range(1, 4)]
    # Go through every option
    for roll in rolls:
        # Turn player 1
        if player == 0:
            # Get the new positions and points for that option
            new_position, new_points = roll_dirac(position_0, points_0, sum(roll))
            # Recursive function call
            player_wins_new = count_wins(1, new_position, position_1, new_points, points_1)
        # Turn player 2
        else:
            # Get the new positions and points for that option
            new_position, new_points = roll_dirac(position_1, points_1, sum(roll))
            # Recursive function call
            player_wins_new = count_wins(0, position_0, new_position, points_0, new_points)

        # Add up the wins from this roll combination
        player_wins += player_wins_new

    # Return the wins
    return player_wins


def part_one(player_positions: np.ndarray, limit: int, dice_size: int) -> int:
    # Initialize dice count and player points
    dice_count = 0
    player_points = np.zeros(2, dtype=int)

    # Play the game
    player_points, dice_count = game_normal(player_positions, player_points, dice_count, limit, dice_size)

    # Calculate the score number
    return min(player_points) * dice_count


def part_two(player_positions: np.ndarray) -> int:
    # Initialize player points
    player_points = np.zeros(2, dtype=int)

    # Play the game (recursive function)
    player_wins = count_wins(0, player_positions[0], player_positions[1], player_points[0], player_points[1])

    # Return the higher number of wins
    return max(player_wins)


def main():
    print('Multiplying the score of the losing player by the dice rolls gives:', part_one(get_input(), 1000, 100))
    print('The player that wins in more universes, wins in this many universes:', part_two(get_input()))


if __name__ == '__main__':
    main()
