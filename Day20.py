import numpy as np


# Get data from .txt file
def get_input() -> (np.ndarray, np.ndarray):
    # Split lines and write each line to list
    with open('Input/Day20.txt', 'r') as file:
        data = file.read().splitlines()

    # Initialize dictionary to convert from the string representation to a number representation
    conversion_dict = {'.': 0, '#': 1}
    # Initialize algo array and input image array
    image_enhancement_algo = np.zeros((len(data[0])), dtype=int)
    input_image = np.zeros((len(data[2]), len(data) - 2), dtype=int)
    # Go through the data lines
    for i, data_line in enumerate(data):
        # The first line is the algo
        if i == 0:
            for j, char in enumerate(data_line):
                image_enhancement_algo[j] = conversion_dict[char]
        # The second line is a space, so everything above is the input image
        elif i >= 2:
            for j, char in enumerate(data_line):
                input_image[i-2, j] = conversion_dict[char]

    return image_enhancement_algo, input_image


def calculate_pixel(input_pixels: np.ndarray, image_enhancement_algo: np.ndarray) -> int:
    # Convert the input_pixels to a bit string
    bit_string = ''.join(map(str, np.concatenate(input_pixels)))
    # Calculate the decimal number
    number = int(bit_string, 2)
    # Return the result of the algo at that number
    return int(image_enhancement_algo[number])


def part_one_two(data: tuple, num_cycles: int) -> int:
    # Get algo and image data
    image_enhancement_algo, input_image = data
    # Initialize output image with zeros
    output_image = np.zeros((input_image.shape[0], input_image.shape[1]), dtype=int)
    # The output image dimension is increased by 2 for each dimension, which corresponds to a padding of 1
    output_image = np.pad(output_image, 1)
    # The input image needs to also have padding and because of the 3x3 kernel, we need a padding of 2
    input_image = np.pad(input_image, 2)

    # Run for num_cycles
    for t in range(num_cycles):
        # Go through every pixel of the output image
        for i in range(output_image.shape[0]):
            for j in range(output_image.shape[1]):
                # Because of the padding, the 3x3 kernels now follow a simple rule to get the sub image
                sub_image = input_image[i:i+3, j:j+3]
                # Calculate the output pixel from that sub image
                output_image[i, j] = calculate_pixel(sub_image, image_enhancement_algo)
        # Set the new input image to the current output
        input_image = output_image
        # The next output adds another padding layer
        output_image = np.pad(output_image, 1)
        # Padding the new input images is a bit trickier because of the infinity consideration. We need to look at
        # our algo and check what it does if there are all zeros (infinity). If it sets them to zero again,
        # we are good and don't have to worry about it and just add a padding of 2 with zeros
        if image_enhancement_algo[0] == 0:
            input_image = np.pad(input_image, 2, mode='constant', constant_values=0)
        # However, if it changes it to 1, we now need to take a closer look
        elif image_enhancement_algo[0] == 1:
            # If the last algo element (all ones) also converts it to a 1, infinity will always be 1s
            if image_enhancement_algo[-1] == 1:
                input_image = np.pad(input_image, 2, mode='constant', constant_values=1)
            # If the last algo element (all ones) converts it to 0, infinity switches between 0s and 1s for every step
            elif image_enhancement_algo[-1] == 0:
                # For every odd round, we have 0s
                if t % 2 == 1:
                    input_image = np.pad(input_image, 2, mode='constant', constant_values=0)
                # For every even round, we have 1s
                elif t % 2 == 0:
                    input_image = np.pad(input_image, 2, mode='constant', constant_values=1)

    # Take the sum of lit pixels and return it
    return int(np.sum(output_image))


def main():
    print('Pixels that are lit in the resulting image:', part_one_two(get_input(), 2))
    print('Pixels that are lit in the resulting image:', part_one_two(get_input(), 50))


if __name__ == '__main__':
    main()
