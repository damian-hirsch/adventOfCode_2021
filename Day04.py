import numpy as np
import re


def get_input() -> (np.ndarray, np.ndarray):
    # Split lines and write each line to list
    with open('Input/Day04.txt', 'r') as file:
        data = file.read().splitlines()
    # The bingo numbers are the first line of the data, split them and put them into an array
    numbers = np.array(list(map(int, data[0].split(','))))
    # Initialize the boards array with shape (board, x, y) --> (100, 5, 5), dividing by 6 because there's a space
    # between each board
    boards = np.zeros(shape=(int(len(data)/6), 5, 5), dtype=int)

    # Fill the board array with data
    counter = 0
    # Skip the first line because that's the bingo numbers line
    for i in range(1, len(data[1:]) + 1):
        # Skip all space lines
        if data[i] != '':
            z = int((i-1)/6)
            # Using regex to find digits instead of split because there are single and dual spaces
            boards[z, counter, :] = list(map(int, re.findall(r'\d+', data[i])))
            counter += 1
        else:
            # Reset board line counter after each space line
            counter = 0

    return numbers, boards


def part_one() -> int:
    # Get numbers and boards
    numbers, boards = get_input()

    # Initialize variables
    found_bingo = False
    board_number = -1
    last_number = -1
    bingo_numbers = set()

    # There can be no bingo with less than 5 numbers
    for j in range(5, len(numbers)):

        # Create set of bingo numbers
        bingo_numbers = set(numbers[0:j])

        # Save last number for later
        last_number = numbers[j-1]
        for i in range(len(boards)*5):
            # Get board number
            board_number = int(i/5)

            # Check horizontals using sets
            board_check = set(boards[board_number, i % 5, :])
            # If we found a winner, we set the bingo flag to True (for outer loop), and we break the inner loop
            if board_check.issubset(bingo_numbers):
                found_bingo = True
                break

            # Check verticals using sets
            board_check = set(boards[board_number, :, i % 5])
            # If we found a winner, we set the bingo flag to True (for outer loop), and we break the inner loop
            if board_check.issubset(bingo_numbers):
                found_bingo = True
                break

        # If we found a winner, we break the outer loop using the bingo flag
        if found_bingo:
            break

    # To get the numbers not use, we create a set of the board array by flattening it first
    board_numbers = set(np.array(boards[board_number, :, :]).flatten())
    # We use set.difference to get the board numbers that were not used and the last number we saved earlier
    return last_number * sum(board_numbers.difference(bingo_numbers))


def part_two() -> int:
    # Get numbers and boards
    numbers, boards = get_input()

    # Initialize variables
    last_number = -1
    bingo_numbers = set()
    winner_boards = []

    # There can be no bingo with less than 5 numbers
    for j in range(5, len(numbers)):
        # Create set of bingo numbers
        bingo_numbers = set(numbers[0:j])

        # Save last number for later
        last_number = numbers[j - 1]

        for i in range(len(boards) * 5):
            # Get board number
            board_number = int(i/5)

            # Check horizontals using sets
            board_check = set(boards[board_number, i % 5, :])
            # If we have a winner, add it to the list of winner boards if it's not already there --> note,
            # this is not the most efficient way but it simplifies the problem and works
            if board_check.issubset(bingo_numbers) and board_number not in winner_boards:
                winner_boards.append(board_number)

            # Check verticals using sets
            board_check = set(boards[board_number, :, i % 5])
            # If we have a winner, add it to the list of winner boards if it's not already there --> note,
            # this is not the most efficient way but it simplifies the problem and works
            if board_check.issubset(bingo_numbers) and board_number not in winner_boards:
                winner_boards.append(board_number)

        # If the number of boards is equal to the number of winner boards, we found the last winner board
        if len(boards) == len(winner_boards):
            break

    # To get the numbers not use, we create a set of the board array by flattening it first
    board_numbers = set(np.array(boards[winner_boards[-1], :, :]).flatten())
    # We use set.difference to get the board numbers that were not used and the last number we saved earlier
    return last_number * sum(board_numbers.difference(bingo_numbers))


def main():
    print('The final score of the chosen that board is:', part_one())
    print('Once the squid wins, its final score is:', part_two())


if __name__ == '__main__':
    main()
