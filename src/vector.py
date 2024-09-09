import math
import numpy as np
from colorama import Fore, Style
from custom import custom_round

"""Class containing all methods to perform vector operations"""
class Vector:
    
    # Constructor for vector object
    def __init__(self, values: list[float]) -> None:
        if len(values) < 1:
            raise ValueError(Fore.RED + "Vector cannot have 0 dimensions" + Style.RESET_ALL)

        self.d = len(values) # dimensions of the vector
        self.values = values # content of the vector

    # Method for scaling a vector by some scalar k
    def scale(self, k: float, logging=False):
        result = Vector(list(map(lambda x: k*x, self.values)))
        if logging:
            print(Fore.LIGHTCYAN_EX + f"The vector scaled by scale factor {k} is:" + Style.RESET_ALL)
            result.toString(logging=False)
        return result

    # Method to add 2 vectors together
    def add(self, v, logging=False):
        self.__constraintCheck(v)
        values = [self.values[i] + v.values[i] for i in range(self.d)]
        result = Vector(values)
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
        values = [[row] for row in self.values]
        return Matrix(values)
    
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
    vec1 = Vector([1,2,3])
    vec1.toString(logging=True)
    vec2 = Vector([4,5,6])
    vec2.toString(logging=True)
    vec3 = vec1.add(vec2, logging=True)
    vec3 = vec3.normalize(logging=True)
    vec1.angle(vec2, logging=True)
    vec1.toMatrix().toVector().toString(logging=True)
    print(repr(vec1))

# Running the main function
if __name__ == "__main__":
    main()