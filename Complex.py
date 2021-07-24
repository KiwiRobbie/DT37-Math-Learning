import random
import math


# Complex Number class
class Complex:
    # Create number from expression or values
    def __init__(self, a=0, b=0, exp=''):
        self.real = a
        self.imag = b

        if exp != '':
            self.evaluate(exp)

    # Evaluate expression
    def evaluate(self, exp):
        if "$randc" in exp:
            rand_range = int(exp[exp.find("{") + 1:exp.find("}")])
            self.real = random.randint(-rand_range, rand_range)
            self.imag = random.randint(-rand_range, rand_range)

    # Add complex numbers
    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    # Subtract complex numbers
    def __sub__(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)

    # Multiply complex numbers
    def __mul__(self, other):
        return Complex(self.real * other.real - self.imag * other.imag, self.real*other.imag + self.imag*other.real)

    # Convert to string for printing
    def __str__(self):
        if self.real and self.imag:
            output = "%d%s%di" % (self.real, {-1: "-", 0: "+", 1: "+"}[math.copysign(1, self.imag)], abs(self.imag))
        elif self.real:
            output = "%d" % self.real
        elif self.imag:
            output = "%d" % self.imag
        else:
            output = "0"
        return output