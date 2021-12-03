# Get data from .txt file
def get_input():
    # Split lines and write each line to list
    with open('Input/Day03.txt', 'r') as file:
        data = file.read().splitlines()
    return data


def part_one(data: list) -> int:
    # Initialize strings
    s = ''
    gamma_rate = ''
    epsilon_rate = ''
    # Cycle through the data lines (j) and each bit position location (i)
    for i in range(len(data[0])):
        for j in range(len(data)):
            # Write a string with the character of every data line at position i
            s += data[j][i]
        # Check how many times 1 occurs in the string and assign correct definition to gamma_rate and epislon_rate
        if s.count('1') > len(s)/2:
            gamma_rate += '1'
            epsilon_rate += '0'
        else:
            gamma_rate += '0'
            epsilon_rate += '1'
        s = ''
    # Convert the values from base2 to base10 and multiply to get the result
    return int(gamma_rate, base=2) * int(epsilon_rate, base=2)


def part_two(data: list) -> int:
    # Initialize list
    list_oxy = []
    # Create a list of list with each bit having it's own location
    for i in range(len(data)):
        list_oxy.append(list(data[i]))
    # Copy the same initial list for CO2
    list_co2 = list_oxy.copy()

    # Find the oxygen bit
    counter_oxy = 0
    # Stop when we found the bit string with the result
    while len(list_oxy) > 1:
        # Initialize string
        s = ''
        # Write a string with the character of every data line at position i
        for j in range(len(list_oxy)):
            s += list_oxy[j][counter_oxy]
        # Figure out count and then drop the bit strings that are not part of it
        # To make sure pop doesn't mess up the iteration, start from the end and move to the beginning
        if s.count('1') >= len(s)/2:
            for k in range(len(list_oxy) - 1, -1, -1):
                if list_oxy[k][counter_oxy] == '0':
                    list_oxy.pop(k)
        else:
            for k in range(len(list_oxy) - 1, -1, -1):
                if list_oxy[k][counter_oxy] == '1':
                    list_oxy.pop(k)
        counter_oxy += 1

    # Do same as above for CO2
    counter_co2 = 0
    while len(list_co2) > 1:
        s = ''
        for j in range(len(list_co2)):
            s += list_co2[j][counter_co2]
        if s.count('0') <= len(s) / 2:
            for k in range(len(list_co2) - 1, -1, -1):
                if list_co2[k][counter_co2] == '1':
                    list_co2.pop(k)
        else:
            for k in range(len(list_co2) - 1, -1, -1):
                if list_co2[k][counter_co2] == '0':
                    list_co2.pop(k)
        counter_co2 += 1

    # Convert the character list of list to a string list of size 1
    oxy = [''.join(ele) for ele in list_oxy]
    co2 = [''.join(ele) for ele in list_co2]
    # Take the first element of the string list of size 1, convert from base2 to base10, and multiply to get the result
    return int(oxy[0], base=2) * int(co2[0], base=2)


def main():
    print('The power consumption of the submarine is:', part_one(get_input()))
    print('The life support rating of the submarine is:', part_two(get_input()))


if __name__ == '__main__':
    main()
