import math
import numpy as np
from colorama import Fore, Style
from custom import custom_round

"""
Class Name: Vector

Description:
    A vector class useful for any complex vector operations

Attributes:
    - d (int): Represents the dimensions of the vector
    - values (list[float]): Stores the contents of the vector in the form of a list/array

Methods:
    (All methdos contain logging bool which allows for terminal output of result if set to True)
    - scale(k: float, logging: bool) -> Vector: Scales a vector and produces a new one as a result.
    - add(v: Vector, logging: bool) -> Vector: Adds current vector with inputted one and produces a new vector.
    - magnitude(logging: bool) -> float: Computes the eularian magnitude of a vector.
    - normalize(logging: bool) -> Vector: normalize's a vector (magnitude of vector = 1)
    - dotProduct(v: Vector, logging: bool) -> float: Computes the dot product between 2 vectors.
    - angle(v: Vector, logging: bool) -> float: Computes the angle between 2 vectors.
    - toMatrix() -> Matrix: converts a vector into a matrix

Example:
    # Example code showing how to create an instance of the class and use its methods.
    v1 = Vector(2, [1, 2])
    v1.normalize()
    v1.magnitude(logging=True)
"""

class Vector:
    
    # Constructor for vector object
    def __init__(self, d: int, values: list[float]) -> None:
        if not isinstance(d, int):
            raise TypeError(Fore.RED + "Ensure d is an integer!" + Style.RESET_ALL)

        if d != len(values):
            raise ValueError(Fore.RED + "Dimensions don't match number of inputted components" + Style.RESET_ALL)
        
        if d < 1:
            raise ValueError(Fore.RED + "Vector cannot have 0 dimensions" + Style.RESET_ALL)

        self.d = d
        self.values = values

    # Method for scaling a vector by some scalar k
    def scale(self, k: float, logging=False):
        result = Vector(self.d, list(map(lambda x: k*x, self.values)))
        if logging:
            print(Fore.LIGHTCYAN_EX + f"The vector scaled by scale factor {k} is:" + Style.RESET_ALL)
            result.toString(logging=False)
        return result

    # Method to add 2 vectors together
    def add(self, v, logging=False):
        self.__constraintCheck(v)
        values = [self.values[i] + v.values[i] for i in range(self.d)]
        result = Vector(self.d, values)
        if logging:
            print(Fore.LIGHTCYAN_EX + "The addition of the 2 vectors is:" + Style.RESET_ALL)
            result.toString(logging=False)
        return result
    
    # Method to find the size of a vector
    def magnitude(self, logging=False) -> float:
        squares = list(map(lambda x: x*x, self.values))
        result = math.sqrt(sum(squares))
        if logging:
            print(Fore.LIGHTCYAN_EX + f"The magnitude of the vector is:" + Style.RESET_ALL + f" {custom_round(result, 6)}")
        return result
    
    # Method to return a normalized vector
    def normalize(self, logging=False):
        result = self.scale(1/self.magnitude())
        if logging:
            print(Fore.LIGHTCYAN_EX + "The normalized vector is:" + Style.RESET_ALL)
            result.toString(logging=False)
        return result

    # Method to compute the dot product of 2 vectors
    def dotProduct(self, v, logging=False) -> float:
        self.__constraintCheck(v)
        result = 0
        for i in range(self.d):
            result += self.values[i] * v.values[i]
        if logging:
            print(Fore.LIGHTCYAN_EX + f"The dot product of the 2 vectors is:" + Style.RESET_ALL + + f" {custom_round(result, 6)}")
        return result
    
    # Method to compute the angle between 2 vectors in degrees
    def angle(self, v, logging=False) -> float:
        self.__constraintCheck(v)
        result = math.acos(self.dotProduct(v) / (self.magnitude() * v.magnitude())) * (180 / math.pi)
        if logging:
            print(Fore.LIGHTCYAN_EX + "The angle between the 2 vectors is:" + Style.RESET_ALL + f" {custom_round(result, 6)}{chr(176)}")
        return result
    
    # Method to represent a vector as a matrix 
    def toMatrix(self):
        from matrix import Matrix
        d = (self.d, 1)
        values = [[row] for row in self.values]
        return Matrix(d, values)
    
    # Constraint checks on 
    def __constraintCheck(self, v):
        if not isinstance(v, Vector): 
            raise TypeError(Fore.RED + "You must input a vector." + Style.RESET_ALL)

        if self.d != v.d:
            raise ValueError(Fore.RED + "Vectors don't have the same dimensions." + Style.RESET_ALL)
    
    # Method for visual representation of a vector
    def toString(self, logging=False) -> str:
        stringVal = list(map(lambda x:str(custom_round(x, 6)), self.values))
        maxLen = len(sorted(stringVal, key=len, reverse=False)[-1])
        if logging:
            print(Fore.LIGHTCYAN_EX + "The vector is:" + Style.RESET_ALL)
        for i in range(self.d):
            print(f"| {stringVal[i]}" + (" " * (maxLen - len(stringVal[i]))) + " |")
        print("")

         # Method to test equality between 2 vectors 
    def __eq__(self, v):
        try:
            self.__constraintCheck(v)
            if (self.d == v.d) and (np.allclose(self.values, v.values)):
                return True
            return False
        except ValueError or TypeError:
            return False
        
    # Detailed representation of the vector object for debugging
    def __repr__(self):
        return f"Vector(dimensions={self.d!r}, components={self.values!r})"



# Main function of the script
def main():
    vec1 = Vector(3, [1,2,3])
    vec1.toString(logging=True)
    vec2 = Vector(3, [4,5,6])
    vec2.toString(logging=True)
    vec3 = vec1.add(vec2, logging=True)
    vec3 = vec3.normalize(logging=True)
    vec1.angle(vec2, logging=True)
    vec1.toMatrix().toVector().toString(logging=True)
    print(repr(vec1))

# Running the main function
if __name__ == "__main__":
    main()