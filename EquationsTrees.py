# Class for solving and storing equations using trees
import operator as op

from Complex import Complex


# Node object for tree class
class Node:
    def __init__(self):
        self.parent = None
        self.data = None
        self.nodes = list()


# Tree of nodes that represents mathematical equation
class EquationsTree:
    # Stores nodes in a 2D list indexed by depth then order added
    def __init__(self):
        self.nodes = list()

    # Add a node containing a piece of data ( Optionally attached to a parent node )
    def add_child(self, level, parent, data):
        # Extend the array if we are adding a new level
        if len(self.nodes) <= level: self.nodes.append(list())

        # Append the new node and set properties
        self.nodes[level].append(Node())
        self.nodes[level][-1].data = data

        # Update properties if the node has a parent
        if level != 0:
            self.nodes[level][-1].parent = parent
            self.nodes[level - 1][parent].nodes.append(len(self.nodes[level]) - 1)

    # Recursively build a tree from imported json data
    def build(self, data, level=0, parent=0):
        # If the function was called on non list data add a leaf node with the value of the data
        if type(data) != list:
            self.add_child(level, parent, data)

        # Otherwise if data is an operation node we should add it and try building the child nodes of that node
        else:
            # Add the operation to the tree and remove the operation from the list
            self.add_child(level, parent, data[1])

            # Build the child nodes recursively
            self.build(data[0], level + 1, len(self.nodes[level]) - 1)
            self.build(data[2], level + 1, len(self.nodes[level]) - 1)

    # Use symbol dict to insert known values into variables
    def insert_symbols(self, symbols):
        for y, level in enumerate(self.nodes):
            for x, node in enumerate(level):
                for key, value in symbols.items():
                    if "[%s]" % key == node.data:
                        self.nodes[y][x].data = value[1]

    # Evaluate the entire tree and return a value
    def evaluate(self):
        # Starting from the second deepest level move back through the tree ( Deepest layer containing operations )
        for level in range(len(self.nodes) - 2, -1, -1):
            # Loop over each node in the level
            for node in range(0, len(self.nodes[level])):
                # Evaluate the node if it has children
                if len(self.nodes[level][node].nodes):
                    # Load the current node into a temp variable
                    active = self.nodes[level][node]

                    # Load both children into temp variables
                    left = self.nodes[level + 1][active.nodes[0]]
                    right = self.nodes[level + 1][active.nodes[1]]

                    # If the children's data is a tuple convert it to a complex number
                    if type(left.data) == tuple:
                        left.data = Complex(*left.data)

                    if type(right.data) == tuple:
                        right.data = Complex(*right.data)

                    # If the child nodes are expression execute them to generate a complex number
                    if type(left.data) == str:
                        left.data = Complex(exp=left.data)

                    if type(right.data) == str:
                        right.data = Complex(exp=right.data)

                    if active.data == "+": active.data = op.add
                    if active.data == "-": active.data = op.sub
                    if active.data == "*": active.data = op.mul
                    if active.data == "/": active.data = op.div

                    # If the current node is an operation perform it on the child nodes
                    active.data = active.data(left.data, right.data)

                    # Update the node with the evaluated value
                    self.nodes[level][node] = active

        # Return the value of the root after evaluating the tree
        return self.nodes[0][0].data
