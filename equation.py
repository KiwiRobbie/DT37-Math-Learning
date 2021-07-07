# Class for solving and storing equations using trees
import random
import operator as op

# Complex Number class
class Complex:
    # Create number from expression or values
    def __init__(self, a=0, b=0, exp=''):
        self.real = a
        self.imag = b

        if exp != '':
            self.evaluate(exp)

    # Evaluate expression
    def evaluate(self,exp):
        if "randc" in exp:
            rand_range = int(exp[exp.find("{")+1:exp.find("}")])
            self.real = random.randint(-rand_range,rand_range)
            self.imag = random.randint(-rand_range,rand_range)

    # Add complex numbers
    def __add__(self, other):
        return Complex(self.real+other.real,self.imag+other.imag)

    # Subtract complex numbers
    def __sub__(self, other):
        return Complex(self.real-other.real,self.imag-other.imag)

    # Multiply complex numbers
    def __mul__(self, other):
        return Complex(self.real*other.real - self.imag*other.imag,self.real+other.imag+self.imag+other.real)

    # Convert to string for printing
    def __str__(self):
        return "%d+%di"%(self.real,self.imag)


# Node object for tree class
class Node:
    def __init__(self):
        self.parent = None
        self.data   = None
        self.nodes  = list()

# Tree of nodes that represents mathematical equation
class Tree:
    # Stores nodes in a 2D list indexed by depth then order added
    def __init__(self):
        self.nodes = list()

    # Add a node containing a piece of data ( Optionally attached to a parent node )
    def add_child(self, level, parent, data):
        # Extend the array if we are adding a new level
        if len(self.nodes)<=level: self.nodes.append(list())

        # Append the new node and set properties
        self.nodes[level].append(Node())
        self.nodes[level][-1].data=data

        # Update properties if the node has a parent
        if level != 0:
            self.nodes[level][-1].parent=parent
            self.nodes[level-1][parent].nodes.append(len(self.nodes[level])-1)

    # Recursively build a tree from imported json data
    def build(self, data, level=0, parent=0):
        # If the function was called on non list data add a leaf node with the value of the data
        if type(data) != list:
            self.add_child(level, parent, data)

        # Otherwise if data is an operation node we should add it and try building the child nodes of that node
        else:
            # Add the operation to the tree and remove the operation from the list
            self.add_child(level, parent, data.pop(1))

            # Build the child nodes recursively
            self.build(data[0], level+1, len(self.nodes[level])-1)
            self.build(data[1], level+1, len(self.nodes[level])-1)

    # Evaluate the entire tree and return a value
    def evaluate(self):
        # Starting from the second deepest level move back through the tree ( Deepest layer containing operations )
        for level in range(len(self.nodes)-2,-1,-1 ):
            # Loop over each node in the level
            for node in range(0,len(self.nodes[level])):
                # Evaluate the node if it has children
                if len(self.nodes[level][node].nodes):
                    # Load the current node into a temp variable
                    active = self.nodes[level][node]

                    # Load both children into temp variables
                    left   = self.nodes[level+1][active.nodes[0]]
                    right  = self.nodes[level+1][active.nodes[1]]

                    # If the children's data is a tuple convert it to a complex number
                    if type(left.data) == tuple:
                        left.data=Complex(*left.data)

                    if type(right.data) == tuple:
                        right.data=Complex(*right.data)

                    # If the child nodes are expression execute them to generate a complex number
                    if type(left.data) == str:
                        left.data=Complex(exp=left.data)

                    if type(right.data) == str:
                        right.data=Complex(exp=right.data)

                    # If the current node is an operation perform it on the child nodes
                    active.data = active.data(left.data, right.data)

                    # Update the node with the evaluated value
                    self.nodes[level][node] = active

        # Return the value of the root after evaluating the tree
        return self.nodes[0][0].data

    def __str__(self):
        msg=''
        for level in range(len(self.nodes)-1,-1,-1 ):
            for node in range(len(self.nodes[level])):
                msg += str(self.nodes[level][node].data)
            msg+='\n'
        return msg

# Test that the systems are working
if __name__ == "__main__":
    json_data=[[Complex(2,0), op.mul, Complex(2,0)], op.add, Complex(2,0)]

    eq = Tree()
    eq.build(json_data)
    print(eq)
    print(eq.evaluate())
