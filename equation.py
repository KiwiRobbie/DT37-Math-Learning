# Class for solving and storing equations using trees
import random

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

# Object for storing data of nodes in tree
class Node:
    def __init__(self):
        self.parent = None
        self.data   = None
        self.nodes  = list()

# Tree of nodes that represents mathematical equation
class Tree:
    # Create with a root node, nodes are indexed by depth then order added
    def __init__(self):
        self.nodes = [[Node()]]

    # Add a child containing data to a specific parent node
    def add_child(self, level, parent, data):
        # Extend the array if we are adding a new level
        if len(self.nodes)-1<=level: self.nodes.append(list())

        # Append the new node and set properties
        self.nodes[level+1].append(Node())
        self.nodes[level+1][-1].parent=parent
        self.nodes[level+1][-1].data=data

        # Update parent node to include location of child
        self.nodes[level][parent].nodes.append(len(self.nodes[level+1])-1)

    # Build a tree from json data
    def build(self):
        pass

    # Evaluate the entire tree and return a value
    def evaluate(self):
        # Starting from the deepest level move back through the tree
        for level in range(len(self.nodes)-2,-1,-1 ):
            # Loop over each node in the level
            for node in range(0,len(self.nodes[level])):
                # Evaluate the node if it has children
                if len(self.nodes[level][node].nodes):
                    active = self.nodes[level][node]
                    left   = self.nodes[level+1][active.nodes[0]]
                    right  = self.nodes[level+1][active.nodes[1]]

                    # If the children's data is a list convert it to a complex number
                    if type(left.data) == list:
                        left.data=Complex(left.data)

                    if type(right.data) == list:
                        right.data=Complex(right.data)

                    # If the child nodes are expression execute them
                    if type(left.data) == str:
                        left.data=Complex(exp=left.data)

                    if type(right.data) == str:
                        right.data=Complex(exp=right.data)

                    # If the current node is an operation perform it on the child nodes
                    if   active.data == "+": active.data = left.data + right.data
                    elif active.data == "*": active.data = left.data * right.data

                    # Update the node with the evaluated value
                    self.nodes[level][node] = active

        # Return the value of the root after evaluating the tree
        return self.nodes[0][0].data

# Test that the systems are working
if __name__ == "__main__":
    equation = Tree()
    equation.nodes[0][0].data="*"
    equation.add_child(0,0,"+")
    equation.add_child(0,0,"*")

    equation.add_child(1,0,Complex(3,2))
    equation.add_child(1,0,Complex(1,2))

    equation.add_child(1,1,Complex(3,5))
    equation.add_child(1,1,"randc{10}")

    print(equation.evaluate())