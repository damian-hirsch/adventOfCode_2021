import re


"""
The key for this exercise is to actually understand what our input is doing: It basically boils down to 14 blocks of
code (from input line up to the next input line)
    1. Multiply the previous result by 26 and add the input variable (w) + a constant, there is no way to influence 
    these blocks in any way by choosing the input variable differently (this block always happens if we add to the
    constant in the first part of the block)
    2. The other block type could do the exact same, but here we have the option to choose the input variable w in a
    way, so it executes basically the opposite: dividing by 26 and removing the previous constant. 
Looking through the exercise, we have 7 blocks of code that execute 1. and 7 blocks of code that can execute 2. If we
want z to be 0 at the end, we need to make sure that with 2. we always choose the variable w in the correct way, so that
we end up at z = 0 again in the end. This tremendously limits the variable space and makes this exercise computationally
solvable.
"""


# Get data from .txt file
def get_input():
    # Split lines and write each line to list
    with open('Input/Day24.txt', 'r') as file:
        data = file.read().splitlines()
    # Initialize list for operation (type), variable, and the operand (second variable)
    operations = []
    variables = []
    operands = []
    # Get them for each instruction line
    for data_line in data:
        # Using a regex to split them
        re_data_line = re.search(r'(\w{3})\s(\w)\s?(\S*)', data_line)
        operations.append(re_data_line.group(1))
        variables.append(re_data_line.group(2))
        # inp commands do not have an operand, we need to check for that before adding to the list
        if re_data_line.group(3):
            operands.append(re_data_line.group(3))
        # Just add None if it doesn't exist
        else:
            operands.append(None)
    return operations, variables, operands


# ALU function that takes MONAD as input
def alu(input_number: str, operations: list, variables: list, operands: list) -> bool:
    # Initialize dictionary to use variables names dynamically
    dict_var = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    # Initialize at which position of the input number we are
    str_pos = 0
    # Loop through all operations, increase the string position after every operation
    for i in range(len(operations)):
        # Get input
        if operations[i] == 'inp':
            dict_var[variables[i]] = int(input_number[str_pos])
            str_pos += 1
        # Add
        elif operations[i] == 'add':
            if operands[i][-1].isdigit():
                dict_var[variables[i]] += int(operands[i])
            else:
                dict_var[variables[i]] += dict_var[operands[i]]
        # Multiply
        elif operations[i] == 'mul':
            if operands[i][-1].isdigit():
                dict_var[variables[i]] = dict_var[variables[i]] * int(operands[i])
            else:
                dict_var[variables[i]] = dict_var[variables[i]] * dict_var[operands[i]]
        # Division (division by 0 should not exist in ALU, no need to check that as well)
        elif operations[i] == 'div':
            # Check if we have a digit or variable, check from the back to avoid having to deal with the minus sign
            if operands[i][-1].isdigit():
                dict_var[variables[i]] = int(dict_var[variables[i]] / int(operands[i]))
            else:
                dict_var[variables[i]] = int(dict_var[variables[i]] / dict_var[operands[i]])
        # Modulo (mod with a<0 or b<=0 should not exist in ALU, no need to check that as well)
        elif operations[i] == 'mod':
            # Check if we have a digit or variable, check from the back to avoid having to deal with the minus sign
            if operands[i][-1].isdigit():
                dict_var[variables[i]] = dict_var[variables[i]] % int(operands[i])
            else:
                dict_var[variables[i]] = dict_var[variables[i]] % dict_var[operands[i]]
        # Equality
        elif operations[i] == 'eql':
            # Check if we have a digit or variable, check from the back to avoid having to deal with the minus sign
            if operands[i][-1].isdigit():
                dict_var[variables[i]] = int(dict_var[variables[i]] == int(operands[i]))
            else:
                dict_var[variables[i]] = int(dict_var[variables[i]] == dict_var[operands[i]])

    # Check if z is 0 in the end and return a bool
    return dict_var['z'] == 0


def part_one_two() -> (int, int):
    operations, variables, operands = get_input()
    # Find restrictions
    # Blocks are organized in groups of 18, the block type is hinted by line 7 within such a block. From this we can
    # create block pairs that build the restrictions with each other, we are using stacking to find the pairs
    positive_blocks = []
    block_pairs = []
    for i in range(int(len(operations)/18)):
        if int(operands[i*18+5]) > 0:
            positive_blocks.append(i)
        else:
            block_pairs.append([i, positive_blocks.pop(-1)])

    # Find the restriction for each block pair:
    restrictions = []
    for block_pair in block_pairs:
        restriction = int(operands[block_pair[0]*18+5]) + int(operands[block_pair[1]*18+15])
        restrictions.append(restriction)

    # Create possible number list for each variable w (model number position) based on these restrictions
    # Note the range is purposely from high to low, to find the number as fast as possible for part 1
    w_list = [[None]] * len(block_pairs) * 2
    for i in range(len(block_pairs)):
        if restrictions[i] >= 0:
            w_list[block_pairs[i][0]] = list(range(9, restrictions[i], -1))
            w_list[block_pairs[i][1]] = list(range(9 - restrictions[i], 0, -1))
        else:
            w_list[block_pairs[i][0]] = list(range(9 + restrictions[i], 0, -1))
            w_list[block_pairs[i][1]] = list(range(9, -restrictions[i], -1))

    # From these restrictions build our now much smaller combination list, ordered from high to low for speed up (not
    # tested if a set, which will lose the order benefit, may be faster, but it's fast enough as is)
    combinations = [(w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14) for w1 in w_list[0]
                    for w2 in w_list[1] for w3 in w_list[2] for w4 in w_list[3] for w5 in w_list[4] for w6 in w_list[5]
                    for w7 in w_list[6] for w8 in w_list[7] for w9 in w_list[8] for w10 in w_list[9]
                    for w11 in w_list[10] for w12 in w_list[11] for w13 in w_list[12] for w14 in w_list[13]]

    # Part 1: Now check all combinations for validity
    model_high = -1
    for combination in combinations:
        # Convert number to string
        number = ''.join(map(str, combination))
        # Check ALU
        check = alu(number, operations, variables, operands)
        # If we have a positive results, we found our number based on the ordering
        if check:
            model_high = int(number)
            break

    # Part 2: Same as above, but we start from the lowest number
    model_low = -1
    for combination in combinations[::-1]:
        # Convert number to string
        number = ''.join(map(str, combination))
        # Check ALU
        check = alu(number, operations, variables, operands)
        # If we have a positive results, we found our number based on the ordering
        if check == 1:
            model_low = int(number)
            break

    return model_high, model_low


def main():
    model_high, model_low = part_one_two()
    print('The largest model number accepted by MONAD is:', model_high)
    print('The lowest model number accepted by MONAD is:', model_low)


if __name__ == '__main__':
    main()
