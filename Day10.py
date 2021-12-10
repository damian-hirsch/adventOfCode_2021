def get_input():
    # Split lines and write each line to list
    with open('Input/Day10.txt', 'r') as file:
        data = file.read().splitlines()
    return data


def part_one(data: list) -> int:
    # Initialize the error score dictionary and character pairs dictionary
    char_score = {')': 3, ']': 57, '}': 1197, '>': 25137}
    char_match = {'(': ')', '[': ']', '{': '}', '<': '>'}

    # Initialize the syntax error score
    syntax_error_score = 0
    # Go through every data line in our data
    for data_line in data:
        # Initialize the char stack for that line
        char_stack = []
        # Check every character of the data line (= string)
        for char in data_line:
            # If the character is an opening character, add to the stack
            if char in ['(', '[', '{', '<']:
                char_stack.append(char)
            # If the character is a closing character, pop one from the stack and compare it with the one we just got
            # By how the brackets should work, there should always be an opening and closing pair
            elif char in [')', ']', '}', '>']:
                check_char = char_stack.pop()
                # If they are not a pair, we have a corrupt line and add to the score
                if char != char_match[check_char]:
                    syntax_error_score += char_score[char]
                    break
            # Just a check in case we have unknown characters
            else:
                print('Unknown character')
                break

    return syntax_error_score


def part_two(data: list) -> int:
    # Initialize the error score dictionary and the matched pairs dictionary
    char_score = {'(': 1, '[': 2, '{': 3, '<': 4}
    char_match = {'(': ')', '[': ']', '{': '}', '<': '>'}
    # Initialize the completion score list for incomplete (not corrupt) lines
    completion_scores = []

    # Go through every data line in our data
    for data_line in data:
        # Initialize bool to check if a line is corrupt or not
        is_not_corrupt = True
        # Initialize the char stack for that line
        char_stack = []
        # Check every character of the data line (= string)
        for char in data_line:
            # If the character is an opening character, add to the stack
            if char in ['(', '[', '{', '<']:
                char_stack.append(char)
            # If the character is a closing character, pop one from the stack and compare it with the one we just got
            # By how the brackets should work, there should always be an opening and closing pair
            elif char in [')', ']', '}', '>']:
                check_char = char_stack.pop()
                # If they are not a pair, we have a corrupt line and change our flag
                if char != char_match[check_char]:
                    is_not_corrupt = False
                    break
            # Just a check in case we have unknown characters
            else:
                print('Unknown character')
                break

        # If the line is not corrupt and it is incomplete (= len of char stack larger 0)
        if is_not_corrupt and len(char_stack) > 0:
            # Initialize score
            score = 0
            # Invert the stack because the matching pairs would have the inverted order
            for char in char_stack[::-1]:
                # Calculate score
                score = score * 5 + char_score[char]
            # Add score to completion score list
            completion_scores.append(score)

    # Sort completion score list
    completion_scores.sort()
    # Return the middle score
    return completion_scores[int(len(completion_scores)/2)]


def main():
    print('Total syntax error score for the errors:', part_one(get_input()))
    print('The middle score is:', part_two(get_input()))


if __name__ == '__main__':
    main()
