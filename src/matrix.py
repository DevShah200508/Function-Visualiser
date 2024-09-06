import math
import numpy as np
from colorama import Fore, Style
from vector import Vector
from custom import custom_round

"""
Class Name: Matrix

Description:
    A matrix class useful for any complex matrix operations

Attributes:
    - d (tuple(int, int)): Represents the dimensions of the matrix as tuple 
    - values (list[list[float]]): Stores the contents of the matrix in the form of a nested list

Methods:
      (All methdos contain logging bool which allows for terminal output of result if set to True)
    - scale(k: float, logging: bool) -> Matrix: Scales a matrix and produces a new one as a result.
    - add(m: Matrix, logging: bool) -> Matrix: Adds current matrix with inputted one and produces a new matrix (dimensions of both matrices need to be the same).
    - multiply(m: Matrix, logging: bool) -> Matrix: Multiplies the current matrix with inputted one and produces new matrix (# of columns of first matrix = # rows of 2nd matrix)
    - determinant() -> float: Computes the determinant of a square matrix (n x n)
    - minorMatrix(p1: int, p2: int, logging: bool) -> Matrix: returns the minor matrix at zero-indexed [p1][p2] positions
    - transpose() -> Matrix: Returns the transposed matrix of the current matrix 
    - inverse() -> Matrix: Returns the inverse matrix of the current matrix 
    - toVector() -> Vector: converts a matrix, in the form (n x 1), into a vector 

Example:
    # Example code showing how to create an instance of the class and use its methods.
    m1 = Vector((2,2), [[2, 2], [1, 4]])
    det = m1.determinant(logging=True)
    inverse = m1.inverse()
    minorMatrix = m1.minorMatrix(0, 1, logging=True)
    transpose = m1.transpose()
"""

class Matrix:
    
    # Constructor for a matrix 
    def __init__(self, values: list[list[float]]) -> None:
        self.__dimensionCheck(values)
        d0, d1 = len(values), len(values[0])
        self.d = (d0, d1)
        self.values = values
    
    # Method to scale a matrix by some scalar k
    def scale(self, k: float):
        values = []
        for i in range(self.d[0]):
            values.append(list(map(lambda x:k*x, self.values[i])))
        
        return Matrix(values)
    
    # Method to add 2 matrices together
    def add(self, m):
        self.__typeCheckMatrix(m)
        if (self.d != m.d):
            raise ValueError(Fore.RED + "Both matrices should have the same dimensions" + Style.RESET_ALL)
        
        values = []
        for i in range(self.d[0]):
            values.append([self.values[i][j] + m.values[i][j] for j in range(self.d[1])])
        
        return Matrix(values)
    
    # Method to multiply 2 matrices together
    def multiply(self, m, logging=False):
        self.__typeCheckMatrix(m)
        if (self.d[1] != m.d[0]):
            raise ValueError(Fore.RED + "Column's of first matrix should be the same as row's of second matrix" + Style.RESET_ALL)
        
        values, temp = [], []
        vecArrA = [Vector(self.values[i]) for i in range(self.d[0])]
        vecArrB = [Vector([row[i] for row in m.values]) for i in range(m.d[1])]
            
        for i in range(self.d[0]):
            for j in range(m.d[1]):
                temp.append(vecArrA[i].dotProduct(vecArrB[j]))
            values.append(temp[:])
            temp.clear()

        result = Matrix(values)
        if logging:
            print(Fore.LIGHTCYAN_EX + "Result of multiplying both matrices is:" + Style.RESET_ALL)
            result.toString()
        
        return result
    
    # Computes a matrix to some power k
    def power(self, k: int, logging=False):
        result = self
        for i in range(k - 1):
            result = result.multiply(self)
        
        if logging:
            print(Fore.LIGHTCYAN_EX + f"Result of the matrix raised to power {k} is:" + Style.RESET_ALL)
            result.toString()

        return result


    # Method to compute the determinant of a square matrix
    def determinant(self, first_call=True, logging=False) -> float:
        if (self.d[0] != self.d[1]):
            raise ValueError(Fore.RED + "Invalid square matrix" + Style.RESET_ALL)
        
        if (self.d[0] == 2 and self.d[1] == 2):
            return (self.values[0][0] * self.values[1][1]) - (self.values[0][1] * self.values[1][0])
        
        determinant = 0
        for i in range(self.d[1]):
            determinant += math.pow(-1, i) * self.values[0][i] * (self.minorMatrix(0,i).determinant(first_call=False))
        
        if first_call and logging:
            print(Fore.LIGHTCYAN_EX + f"The determinant of the matrix is:" + Style.RESET_ALL + f" {custom_round(determinant, 6)}")

        return determinant
        
    # Method to determine the cofactor matrix when given the zero-based position of the first row
    def minorMatrix(self, p1: int, p2: int, logging=True):
        values, temp = [], []
    
        for i in range(self.d[0]):
            for j in range(self.d[1]):
                if (i != p1) and (j != p2):
                    temp.append(self.values[i][j])
            if (len(temp) > 0):
                values.append(temp[:])
                temp.clear()
            
        result = Matrix(values)
        return result
    
    # Method to transpose a matrix
    def transpose(self, logging=False):
        values = [[row[j] for row in self.values] for j in range(self.d[1])]
        result = Matrix(values)
        if logging:
            print(Fore.LIGHTCYAN_EX + "The transpose of the matrix is:" + Style.RESET_ALL)
            result.toString()
        return result
    
    # Method to compute the inverse of a square matrix using formula: A^-1 = 1/det(A) * Adj(A)
    def inverse(self, logging=False):
        if (self.d[0] != self.d[1]):
            raise ValueError(Fore.RED + "Invalid square matrix" + Style.RESET_ALL)
        
        determinant = self.determinant()
        if (determinant == 0):
            raise ValueError(Fore.RED + "Singular matrix cannot be inverted" + Style.RESET_ALL)
        
        cofactorArr = [[] for _ in range(self.d[0])]
        for i in range(self.d[0]):
            for j in range(self.d[1]):
                posValue = (math.pow(-1, i+j) * self.minorMatrix(i,j).determinant())
                cofactorArr[i].append(posValue)
        
        cofactorMatrix = Matrix(cofactorArr)
        transposedMatrix = cofactorMatrix.transpose()
        result = transposedMatrix.scale(1/determinant)
        if logging:
            print(Fore.LIGHTCYAN_EX + f"The inverse of the matrix is:" + Style.RESET_ALL)
            result.toString()

        return result
    
    # Method to turn a matrix into a vector if correct form is met
    def toVector(self):
        if self.d[1] != 1:
            raise ValueError(Fore.RED + "This matrix cannot be turned into a vector" + Style.RESET_ALL)
        
        values = [row[0] for row in self.values]
        return Vector(values)
    
    # Method containing all dimension checking for a matrix
    def __dimensionCheck(self, values: list[list[float]]) -> None:
        d0 = len(values)
        if (d0 == 0):
            raise ValueError(Fore.RED + "Make sure your matrix has atleast 1 row" + Style.RESET_ALL)
        
        d1 = len(values[0])
        if (d1 == 0):
            raise ValueError(Fore.RED + "Make sure your matrix has atleast 1 column" + Style.RESET_ALL)
        
        d = (d0, d1)

        if not (isinstance(values, list) and all(isinstance(row, list) for row in values)):
            raise TypeError(Fore.RED + "Matrix inputted in the incorrect format" + Style.RESET_ALL)
        
        if all(len(row) == d1 for row in values) != True:
            raise ValueError(Fore.RED + "Make sure all rows have the same number of columns" + Style.RESET_ALL)
        
    def __typeCheckMatrix(self, m) -> None:
        if not isinstance(m, Matrix):
            raise TypeError(Fore.RED + "Input a valid matrix" + Style.RESET_ALL)
            
    
    # Method for visual representation of a matrix
    def toString(self, logging=False) -> None:
        stringVal = [list(map(lambda x:str(custom_round(x, 6)), self.values[i])) for i in range(self.d[0])]
        joinedStringVal = [" ".join(row) for row in stringVal]
        maxLen = len(sorted(joinedStringVal, key=len, reverse=False)[-1])

        if logging:
            print(Fore.LIGHTCYAN_EX + "The matrix is:" + Style.RESET_ALL)
        
        for i in range(self.d[0]):
            print(f"| {joinedStringVal[i]}" + (" " * (maxLen - len(joinedStringVal[i]))) + " |")
        print("") 

         # Method to test equality between 2 matrices
    def __eq__(self, m):
        try:
            self.__typeCheckMatrix(m)
            if (self.d == m.d) and (np.allclose(self.values, m.values)):
                return True
            return False
        except TypeError:
            return False
     
    
    # Detailed representation of the matrix object for debugging
    def __repr__(self):
        return f"Matrix(dimensions={self.d!r}, values={self.values!r})"

def main():
    matA = Matrix([[2,1,3,0],[1,2,1,3],[3,1,2,2],[5,2,7,3]])
    matA.transpose(logging=True)
    matA.determinant(logging=True)
    matA.toString(logging=True)
    matB = matA.inverse(logging=True)
    matA.multiply(matB, logging=True)
    matC = Matrix([[1],[2],[3]])
    matC.toVector().normalize(logging=True)
    matD = Matrix([[2,0],[0,2]])
    matD.power(3, logging=True)
    print(repr(matA))
    print(matA == matB.inverse())

if __name__ == "__main__":
    main()
