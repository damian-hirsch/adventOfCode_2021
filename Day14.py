import numpy as np
import re


# Get data from .txt file
def get_input():
    # Split lines and write each line to list
    with open('Input/Day14.txt', 'r') as file:
        data = file.read().splitlines()

    # The polymer template is the first line of the data
    template = data[0]

    # Initialize dictionary for insertion
    dict_insertion = {}
    # Build insertion dictionary
    for data_line in data[2:]:
        # Find input component and output component
        re_matches = re.search(r'(\w+) -> (\w)', data_line)
        # Assign to key and value in the dictionary
        dict_insertion[re_matches.group(1)] = re_matches.group(2)

    # Return both the template and dictionary
    return template, dict_insertion


def part_one(steps: int) -> int:
    # Get the template and dictionary
    template, dict_insertion = get_input()

    # Go through the steps
    for t in range(steps):
        # Initialize new template, the first letter is always the same
        template_new = template[0]
        # Go through the template
        for i in range(len(template) - 1):
            # Get components, translate them with the dictionary, and add new component to template
            template_new += dict_insertion[template[i:i+2]]
            # Add the second letter of the initial component after, like requested
            template_new += template[i+1]
        # Reset the template
        template = template_new

    # Get all characters in the template
    characters = list(set(template))
    # Initialize character count
    characters_count = np.zeros((len(characters)), dtype=int)
    # Count all characters
    for j in range(len(characters)):
        characters_count[j] = template.count(characters[j])

    # Return difference between max and min of the counts
    return int(max(characters_count) - min(characters_count))


def part_two(steps: int) -> int:
    # Part 2 is a bit more challenging, because the previous approach won't work. It's computationally too expensive
    # because of the string concatenation. Thus, we are using a different approach here.

    # Get the template and dictionary
    template, dict_insertion = get_input()

    # Create a component dictionary to track indices and find all elements
    component_to_idx = {}
    elements = set()
    for i, component in enumerate(dict_insertion.keys()):
        component_to_idx[component] = i
        elements.update(set(component))

    # Create an element dictionary
    element_to_idx = {}
    for i, element in enumerate(elements):
        element_to_idx[element] = i

    # Create build plan (each reaction will consume one component and create two new ones, example CH --> B yields to
    # string CBH which actually are components CB and BH, so CH --> CB, BH).
    components_build = np.zeros((len(dict_insertion), len(dict_insertion)), dtype=int)
    components_to_element = np.zeros((len(dict_insertion), (len(elements))), dtype=int)
    for component, compound in dict_insertion.items():
        # Create new components
        new_component1 = component[0] + compound
        new_component2 = compound + component[1]
        # The original component is used up
        components_build[component_to_idx[component], component_to_idx[component]] += -1
        # Two new components are created
        components_build[component_to_idx[component], component_to_idx[new_component1]] += 1
        components_build[component_to_idx[component], component_to_idx[new_component2]] += 1

        # Build component to element map at the same time (example: CH consists of element C and H)
        components_to_element[component_to_idx[component], element_to_idx[component[0]]] += 1
        components_to_element[component_to_idx[component], element_to_idx[component[1]]] += 1

    # Build initial components count from template
    component_count = np.zeros((len(dict_insertion)), dtype=np.int64)
    for i in range(len(template) - 1):
        component = template[i:i+2]
        component_count[component_to_idx[component]] += 1

    # Go through steps
    for t in range(steps):
        # Copy the component_count to not let it overwrite itself while processing
        component_count_copy = component_count.copy()
        for j in range(len(component_count)):
            # Update the count by adding the build components multiplied by the number of the components to it
            component_count_copy += component_count[j] * components_build[j, :]
        # Update the component_count
        component_count = component_count_copy

    # Calculate the amounts of elements we have, we can use a matrix multiplication with our setup to make this
    # efficient. Note that this way, every element is counted twice for each component (divide by 2), e.g.,
    # example CH, HB --> CHB. The first and last element are only counted once (ceil is an easy way to fix this)
    count_elements = np.ceil(np.matmul(np.transpose(component_count), components_to_element) / 2)

    # Return the difference between the max and min element count
    return int(max(count_elements) - min(count_elements))


def main():
    print('Part 1: Quantity of the most common element subtracted the least common element:', part_one(10))
    print('Part 2: Quantity of the most common element subtracted the least common element:', part_two(40))


if __name__ == '__main__':
    main()
