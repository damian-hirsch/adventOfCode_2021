import numpy as np
from collections import defaultdict
import heapq as heap


def get_input():
    with open('Input/Day15.txt', 'r') as file:
        data = file.read().splitlines()

    risk_level_map = np.zeros((len(data), len(data[0])), dtype=int)
    for i in range(len(data)):
        risk_level_map[i, :] = list(data[i])

    return risk_level_map


# The problem can be solved using the Dijkstra algorithm
def dijkstra(cost_map, starting_node):
    # Create a set “visited” to keep track of visited nodes
    visited = set()
    # Create a dictionary for parents map to reconstruct the path after the execution of the algorithm (not needed)
    parents_map = {}
    # Create a dictionary for keeping track of minimum costs for reaching different nodes from the source node,
    # and initialize the cost for the source node as 0
    # We are using defaultdict here to not having to deal with non-existing entries ourselves
    node_costs = defaultdict(lambda: float('inf'))
    # Create a priority queue data structure and push a tuple (0, source node) in the Priority Queue (heap),
    # representing the cost to the node from the source node, the node itself
    priority_queue = []
    node_costs[starting_node] = 0
    heap.heappush(priority_queue, (0, starting_node))

    # Loop inside a while loop until there is nothing in the priority queue. While looping, pop the node with minimum
    # cost. We could also add a break statement here once we found the bottom right location, but for completeness we
    # won't. The code still runs fast enough.
    while priority_queue:
        # Go greedily by always extending the shorter cost nodes first
        _, node = heap.heappop(priority_queue)
        visited.add(node)

        # Get adj_nodes and their weights
        adj_nodes = []
        weights = []
        y = int(node.split(', ')[0])
        x = int(node.split(', ')[1])
        # Check if there is a top node
        if y > 0:
            adj_nodes.append(str(y-1) + ', ' + str(x))
            weights.append(cost_map[y-1, x])
        # Check if there is a right node
        if x < cost_map.shape[1] - 1:
            adj_nodes.append(str(y) + ', ' + str(x+1))
            weights.append(cost_map[y, x+1])
        # Check if there is a bottom node
        if y < cost_map.shape[0] - 1:
            adj_nodes.append(str(y+1) + ', ' + str(x))
            weights.append(cost_map[y+1, x])
        # Check if there is a left node
        if x > 0:
            adj_nodes.append(str(y) + ', ' + str(x-1))
            weights.append(cost_map[y, x-1])

        # Check adj_nodes
        for i in range(len(adj_nodes)):
            # If we visited the note already, we can skip
            if adj_nodes[i] in visited:
                continue

            # Calculate new cost
            new_cost = node_costs[node] + weights[i]
            # If the current node cost is bigger than the new total costs, add them too to the priority queue and
            # update the parents_map
            if node_costs[adj_nodes[i]] > new_cost:
                parents_map[adj_nodes[i]] = node
                node_costs[adj_nodes[i]] = new_cost
                heap.heappush(priority_queue, (new_cost, adj_nodes[i]))

    # Return the parents_map and node_costs. The parents_map could be used to reconstruct the optimal path,
    # but we won't need this here
    return parents_map, node_costs


def part_one(risk_level_map: np.ndarray) -> int:
    # Get all node costs starting from [0, 0]
    _, node_costs = dijkstra(risk_level_map, '0, 0')

    # Get bottom right
    y = risk_level_map.shape[0] - 1
    x = risk_level_map.shape[1] - 1

    # Return node cost for the bottom right
    return int(node_costs[str(y) + ', ' + str(x)])


def part_two(risk_level_map: np.ndarray) -> np.int64:
    # Create extended risk level map
    y_len = risk_level_map.shape[0]
    x_len = risk_level_map.shape[1]
    risk_level_map_extended = np.zeros((y_len * 5, x_len * 5), dtype=int)
    # Add the new section add increase each section to the right/bottom by 1 of the previous one
    for i in range(5):
        for j in range(5):
            risk_level_map_extended[i*y_len:(i+1)*y_len, j*x_len:(j+1)*x_len] = risk_level_map + i + j

    # Risk levels above 9 wrap back around to 1
    risk_level_map_extended = ((risk_level_map_extended - 1) % 9) + 1

    # Get all node costs starting from [0, 0]
    _, node_costs = dijkstra(risk_level_map_extended, '0, 0')

    # Get bottom right
    y = risk_level_map_extended.shape[0] - 1
    x = risk_level_map_extended.shape[1] - 1

    # Return node cost for the bottom right
    return int(node_costs[str(y) + ', ' + str(x)])


def main():
    print('Part 1: Lowest total risk of any path from the top left to the bottom right: ', part_one(get_input()))
    print('Part 2: Lowest total risk of any path from the top left to the bottom right: ', part_two(get_input()))


if __name__ == '__main__':
    main()
