#!/usr/bin/python

''' Program for generating a tree for Aispace's Search simulator.

Generates a .txt file with the description of a tree for the 3x3 slider game.

October 2013 - PCS2428 - Poli-USP
'''

import sys

# SETTINGS. Configure stuff here.
_MAX_DEPTH = 6

# If set to false, the movements will have the following edge costs:
# Up: 4
# Right: 1
# Down: 2
# Left: 3
_UNITARY_EDGE_COST = True

# /SETTINGS

# State representation
_EMPTY = "B"
_GOAL_STATE = ["1", "2", "3", "4", "5", "6", "7", "8", _EMPTY]
_START_STATE = ["4", "1", "2", "7", "5", "3", _EMPTY, "8", "6"]

# Output strings
_NODES_HEADER = "% Nodes\n% N: index, node_name, x_position, y_position, node_type, node_heuristics;"
_EDGES_HEADER = "% Edges\n% E: from_node_index, to_node_index, edge_cost;"
_MISC_HEADER = "% Miscellaneous\n% M: predicate, value;"
_NODE_TYPE_REGULAR = "REGULAR"
_NODE_TYPE_START = "START"
_NODE_TYPE_GOAL = "GOAL"

# Eye-candy to make the tree look good
_INITIAL_X = 0
_INITIAL_Y = 0
_MIN_DIST = 10

# Global Variables
_node_index = 0
_generated_nodes = {}


class Node(object):
    def __init__(self, node_name, edge_cost=1, x_position=0, y_position=0,
                 node_type=_NODE_TYPE_REGULAR, node_heuristics=0):
        global _node_index
        self.index = _node_index
        _node_index += 1

        self.node_name = node_name

        self.x_position = x_position
        self.y_position = y_position
        self.node_type = node_type
        self.node_heuristics = node_heuristics

        self.edge_cost = edge_cost
        self.children = []

    def __repr__(self):
        # This is equivalent to Java's toString() method. Allows us to print the node directly.
        return (
            "N: " + str(self.index) + ", " +
            self.node_name + ", " +
            str(self.x_position) + ", " +
            str(self.y_position) + ", " +
            self.node_type + ", " +
            str(self.node_heuristics) + ";"
        )

    def add_child(self, node):
        if node is not None:
            self.children.append(node)


def _subtree(state, heuristic, edge_cost=1, x=_INITIAL_X, y=_INITIAL_Y, depth=0, max_depth=10):
    if state is None or depth > max_depth:
        return None

    node_name = "".join(state)

    # If we've been here before, just returns the node so we can add a returning edge.
    if _generated_nodes.get(node_name):
        return _generated_nodes[node_name]

    node = Node(
        node_name=node_name,
        edge_cost=edge_cost,
        x_position=x,
        y_position=y,
        node_heuristics=heuristic(state)
    )
    _generated_nodes[node_name] = node

    if state == _GOAL_STATE:
        node.node_type = _NODE_TYPE_GOAL
        return node

    # Pretty hard to make the tree look good. This is acceptable for depth 6, dunno for others.
    x_offset = _MIN_DIST * 5 ** (max_depth - depth)
    y_offset = _MIN_DIST * 5 ** max_depth / max_depth

    node.add_child(_subtree(
        state=_move_up(state),
        heuristic=heuristic,
        edge_cost=1 if _UNITARY_EDGE_COST else 4,
        x=x - 1.5 * x_offset,
        y=y + y_offset,
        depth=depth + 1,
        max_depth=max_depth
    ))

    node.add_child(_subtree(
        state=_move_right(state),
        heuristic=heuristic,
        edge_cost=1 if _UNITARY_EDGE_COST else 1,
        x=x - 0.5 * x_offset,
        y=y + y_offset,
        depth=depth + 1,
        max_depth=max_depth
    ))

    node.add_child(_subtree(
        state=_move_down(state),
        heuristic=heuristic,
        edge_cost=1 if _UNITARY_EDGE_COST else 2,
        x=x + 0.5 * x_offset,
        y=y + y_offset,
        depth=depth + 1,
        max_depth=max_depth
    ))

    node.add_child(_subtree(
        state=_move_left(state),
        heuristic=heuristic,
        edge_cost=1 if _UNITARY_EDGE_COST else 3,
        x=x + 1.5 * x_offset,
        y=y + y_offset,
        depth=depth + 1,
        max_depth=max_depth
    ))

    return node


def _swap(state, i, j):
    aux = state[i]
    state[i] = state[j]
    state[j] = aux
    return state


def _move_up(state):
    empty_index = state.index(_EMPTY)
    return _swap(state[:], empty_index, empty_index - 3) if empty_index >= 3 else None


def _move_down(state):
    empty_index = state.index(_EMPTY)
    return _swap(state[:], empty_index, empty_index + 3) if empty_index <= 5 else None


def _move_left(state):
    empty_index = state.index(_EMPTY)
    return _swap(state[:], empty_index, empty_index - 1) if empty_index % 3 != 0 else None


def _move_right(state):
    empty_index = state.index(_EMPTY)
    return _swap(state[:], empty_index, empty_index + 1) if empty_index % 3 != 2 else None


def _print_subtree(node, visited_nodes):
    if node in visited_nodes:
        return
    print node
    visited_nodes.append(node)
    for n in node.children:
        _print_subtree(n, visited_nodes)


def _print_edges(node, visited_nodes):
    def print_edge(parent, child):
        print "E: " + str(parent.index) + ", " + str(child.index) + ", " + str(child.edge_cost) + ";"

    if node in visited_nodes:
        return
    visited_nodes.append(node)
    for n in node.children:
        print_edge(node, n)
        _print_edges(n, visited_nodes)


def main(heuristic_index):

    # No heuristic.
    def h0(state):
        return 0

    # Heuristic function 1: the number of pieces in wrong places.
    def h1(state):
        return [
            state[i] != _GOAL_STATE[i] and state[i] != _EMPTY
            for i in range(len(state))
        ].count(True)
        # List comprehension FTW! The line above is equivalent to:
        # count = 0
        # for i in range(len(state)):
        #     if state[i] != _GOAL_STATE[i] and state[i] != _EMPTY:
        #         count += 1
        # return count


    # Heuristic function 2: sum of Manhattan distances between pieces' positions and goal positions.
    def h2(state):
        return sum([
            abs(i % 3 - _GOAL_STATE.index(state[i]) % 3) +
            abs(i / 3 - _GOAL_STATE.index(state[i]) / 3)
            if state[i] != _EMPTY else 0 for i in range(len(state))
        ])
        # total = 0
        # for i in range(len(state)):
        #     if state[i] != _EMPTY:
        #         index = _GOAL_STATE.index(state[i])
        #         total += abs(i % 3 - index % 3) + abs(i / 3 - index / 3)
        # return total

    heuristics = [h0, h1, h2]

    node = _subtree(
        state=_START_STATE,
        heuristic=heuristics[heuristic_index],
        edge_cost=1,
        max_depth=_MAX_DEPTH
    )
    node.node_type = _NODE_TYPE_START

    print "\n" + _NODES_HEADER
    _print_subtree(node, [])

    print "\n" + _EDGES_HEADER
    _print_edges(node, [])

    print "\n" + _MISC_HEADER
    print "M: HEURISTICS, AUTOMATIC;\nM: COSTS, MANUAL;"


def help():
    print """usage: python tree_generator HEURISTIC_FUNCTION

    0 - no heuristic
    1 - number of pieces in wrong places
    2 - sum of Manhattan distances between pieces' positions and goal positions
    """


if __name__ == "__main__":
    if (len(sys.argv) != 2 or sys.argv[1] not in ["0", "1", "2"]
            or "-h" in sys.argv or "--help" in sys.argv):
        help()
    else:
        main(int(sys.argv[1]))
