import numpy as np


# Get data from .txt file
def get_input() -> str:
    # Get the string
    with open('Input/Day16.txt', 'r') as file:
        data = file.read()
    return data


# Calculate the literal value
def get_literal_value(bin_string: str) -> (int, int):
    # Initialize the literal string
    literal_value_string = ''
    # Initialize the first bit, so it goes into the while loop
    first_bit = '1'
    # Initialize current location
    current_location = 0
    # Repeat while the first bit of the 5 is equal to 1
    while first_bit == '1':
        # Check the first bit
        first_bit = bin_string[current_location]
        # Increase location to the second bit
        current_location += 1
        # Add the 4 bits to the string
        literal_value_string += bin_string[current_location:current_location + 4]
        # Increase the location by 4
        current_location += 4

    # Calculate literal value
    literal_value = int(literal_value_string, 2)

    # Return the literal value, and the current location in the string
    return literal_value, current_location


def open_packets(bin_string: str, version_count: int) -> (int, int, int):
    # Initialize the current location
    current_location = 0
    # Initialize the literal value
    literal_value = 0

    # Get packet version
    packet_version = int(bin_string[current_location:current_location + 3], 2)
    current_location += 3
    version_count += packet_version

    # Get packet type
    packet_type = int(bin_string[current_location:current_location + 3], 2)
    current_location += 3

    # If we have a literal packet type
    if packet_type == 4:
        # Get literal value
        literal_value, chars_used = get_literal_value(bin_string[current_location:])
        # Increase the current location based on how many characters (how many locations) the literal calculation used
        current_location += chars_used

    # If it's not a literal, we have to unpack
    else:
        # Initialize literal_value_list to store all literal_values from the sub-packages
        literal_value_list = []

        # Get length type ID
        length_type_id = bin_string[current_location]
        current_location += 1

        # Length type '0': 15-bit number representing the number of bits in the sub-packets in bits
        if length_type_id == '0':
            # Calculate the sub-package character length
            length_sub_packet = int(bin_string[current_location:current_location+15], 2)
            current_location += 15
            # Check packages by counting the characters used
            chars_used_total = 0
            # While we haven't used all characters, there are still more packages
            while chars_used_total < length_sub_packet:
                # Open the sub-packages by recursively opening the sub packets
                version_count, chars_used, literal_value = open_packets(
                    bin_string[current_location:current_location+length_sub_packet], version_count)
                # Add the literal values found to the literal values list
                literal_value_list.append(literal_value)
                # Move the current location based on how many chars the sub-package used
                current_location += chars_used
                # Increase the count based on how many chars the sub-package used
                chars_used_total += chars_used

        # Length type '1': 11-bit number representing the number of sub-packets
        elif length_type_id == '1':
            # Calculate the number of sub-packages
            num_sub_packet = int(bin_string[current_location:current_location+11], 2)
            current_location += 11
            # Loop through the number of sub-packages
            for i in range(num_sub_packet):
                # Open the sub-packages by recursively opening the sub packets
                version_count, chars_used, literal_value = open_packets(bin_string[current_location:], version_count)
                # Add the literal values found to the literal values list
                literal_value_list.append(literal_value)
                # Move the current location based on how many chars the sub-package used
                current_location += chars_used
        # Error in case we find something weird
        else:
            print('Error: Could not find length type ID')

        # Packet type 0 calculates the sum of elements
        if packet_type == 0:
            literal_value = np.sum(literal_value_list)
        # Packet type 1 calculates the product of elements
        elif packet_type == 1:
            literal_value = np.product(literal_value_list)
        # Packet type 2 calculates the minimum of elements
        elif packet_type == 2:
            literal_value = np.min(literal_value_list)
        # Packet type 3 calculates the maximum of elements
        elif packet_type == 3:
            literal_value = np.max(literal_value_list)
        # Packet type 4 calculates the literal (skipped because it's above)
        # Packet type 5 calculates if the first value is larger than the second (1/0)
        elif packet_type == 5:
            literal_value = int(literal_value_list[0] > literal_value_list[1])
        # Packet type 6 calculates if the first value is smaller than the second (1/0)
        elif packet_type == 6:
            literal_value = int(literal_value_list[0] < literal_value_list[1])
        # Packet type 7 calculates if the first value is equal to the second (1/0)
        elif packet_type == 7:
            literal_value = int(literal_value_list[0] == literal_value_list[1])
        # Error in case we find something weird
        else:
            print('Error: Could not find package type')

    # Return the literal_value of the package and the current location we are in the string
    return version_count, current_location, literal_value


def part_one(data: str) -> int:
    # Calculate the binary size
    bin_size = len(data) * 4
    # Get the binary string, remove the first two characters and pad with 0 zeros to fill it up according to bin
    # size. 0 or 00 at the start is required in order to work properly.
    bin_string = bin(int(data, 16))[2:].zfill(bin_size)
    # Call the open packets function with the full bin_string and initialize the version count
    version_count, _, _ = open_packets(bin_string, 0)

    return version_count


def part_two(data: str) -> int:
    # Calculate the binary size
    bin_size = len(data) * 4
    # Get the binary string, remove the first two characters and pad with 0 zeros to fill it up according to bin
    # size. 0 or 00 at the start is required in order to work properly.
    bin_string = bin(int(data, 16))[2:].zfill(bin_size)
    # Call the open packets function with the full bin_string and initialize the version count
    _, _, literal_value = open_packets(bin_string, 0)

    return literal_value


def main():
    print('Adding up the version numbers in all packets gets:', part_one(get_input()))
    print('Value after evaluating the expression represented by hex-encoded BITS transmission: ', part_two(get_input()))


if __name__ == '__main__':
    main()
