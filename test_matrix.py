import unittest
import math
from vector import Vector
from matrix import Matrix

class MatrixTest(unittest.TestCase):

    # Sets up the matrices being used in the tests
    def setUp(self):
        self.matrix1 = Matrix((3, 3), [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
        self.matrix2 = Matrix((3, 1), [[2.0], [7.0], [1.0]])
        self.matrix3 = Matrix((4, 1), [[7.0], [8.0], [0.0], [3.0]])
        self.matrix4 = Matrix((1, 4), [[3.0, 15.0, 12.0, 5.0]])
        self.matrix5 = Matrix((4, 4), [[1.0, 4.0, 3.0, 7.0], [12.0, 25.0, 4.0, 2.0], [13.0, 37.0, 6.0, 9.0], [21.0, 2.0, 2.0, 5.0]])
        self.matrix6 =  Matrix((3, 3), [[1.0, 1.0, 3.0], [4.0, 5.0, 6.0], [2.0, 3.0, 9.0]])

    # Ensures that matrices are correctly being initialized 
    def test_intialization(self):
        m = Matrix((2, 2), [[1.0, 2.0], [3.0, 4.0]])
        self.assertEqual(m.d, (2,2))
        self.assertEqual(m.values, [[1.0, 2.0], [3.0, 4.0]])

    # Tests matrix initialisation error (e.g mismatch of dimensions)
    def test_initialization_dimension_mismatch(self):
        with self.assertRaises(ValueError):
            Matrix((1, 3), [[1.0, 2.0], [3.0, 4.0]])  # Dimensions don't match the number of values    

    # Tests matrix scaling
    def test_scale(self):
        scaled_m1 = self.matrix1.scale(2)
        scaled_m2 = self.matrix2.scale(3)
        self.assertEqual(scaled_m1.values, [[2.0, 4.0, 6.0], [8.0, 10.0, 12.0], [14.0, 16.0, 18.0]])
        self.assertEqual(scaled_m2.values, [[6.0], [21.0], [3.0]])

    # Tests zero scaling    
    def test_scale_zero(self):
        scaled_v = self.matrix1.scale(0)
        self.assertEqual(scaled_v.values, [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

    # Tests negative scaling
    def test_scale_negative(self):
        scaled_v = self.matrix1.scale(-1)
        self.assertEqual(scaled_v.values, [[-1.0, -2.0, -3.0], [-4.0, -5.0, -6.0], [-7.0, -8.0, -9.0]])

    # Tests matrix addition
    def test_add(self):
        v = self.matrix1.add(self.matrix6)
        self.assertEqual(v.values, [[2.0, 3.0, 6.0], [8.0, 10.0, 12.0], [9.0, 11.0, 18.0]])

    # Tests mismatch dimensions between 2 matrices undergoing addition
    def test_add_dimension_mismatch(self):
        with self.assertRaises(ValueError):
            self.matrix1.add(self.matrix2)  # Vectors don't have the same dimensions
        
        with self.assertRaises(ValueError):
            self.matrix1.add(self.matrix4) 

        with self.assertRaises(ValueError):
            self.matrix4.add(self.matrix5)  
        
        with self.assertRaises(ValueError):
            self.matrix2.add(self.matrix5) 

    # Tests matrix multiplication
    def test_multiply(self):
        v = self.matrix1.multiply(self.matrix2)
        self.assertEqual(v, Matrix((3, 1), [[19.0], [49.0], [79.0]]))

    # Tests mismatch row-column between 2 matrices undergoing multiplication
    def test_multiply_dimension_mismatch(self):
        with self.assertRaises(ValueError):
            self.matrix1.multiply(self.matrix3)
        
        with self.assertRaises(ValueError):
            self.matrix2.multiply(self.matrix3)
        
        with self.assertRaises(ValueError):
            self.matrix3.multiply(self.matrix5)

        with self.assertRaises(ValueError):
            self.matrix2.multiply(self.matrix6)

        with self.assertRaises(ValueError):
            self.matrix3.multiply(self.matrix6)

    # Tests repeated matrix multiplication (matrix raised to power k)
    def test_power(self):
        self.assertEqual(self.matrix1.power(3), Matrix((3,3), [[468.0, 576.0, 684.0], [1062.0, 1305.0, 1548.0], [1656.0, 2034.0, 2412.0]]))
        self.assertEqual(self.matrix5.power(2), Matrix((4,4), [[235.0, 229.0, 51.0, 77.0], [406.0, 825.0, 164.0, 180.0], [724.0, 1217.0, 241.0, 264.0], [176.0, 218.0, 93.0, 194.0]]))
        self.assertEqual(self.matrix6.power(4), Matrix((3,3), [[1813.0, 2454.0, 5616.0], [5160.0, 6973.0, 15888.0], [5296.0, 7168.0, 16401.0]]))

    # Tests determiant of a matrix
    def test_determinant(self):
        self.assertEqual(self.matrix1.determinant(), 0)
        self.assertEqual(self.matrix5.determinant(), 7122)
        self.assertEqual(self.matrix6.determinant(), 9)

    # Tests minor matrix of a matrix
    def test_minorMatrix(self):
        self.assertEqual(self.matrix1.minorMatrix(0,0), Matrix((2,2), [[5.0, 6.0], [8.0, 9.0]]))
        self.assertEqual(self.matrix1.minorMatrix(1,1), Matrix((2,2), [[1.0, 3.0], [7.0, 9.0]]))
        self.assertEqual(self.matrix1.minorMatrix(1,2), Matrix((2,2), [[1.0, 2.0], [7.0, 8.0]]))

    # Tests transposition of a matrix
    def test_transpose(self):
        self.assertEqual(self.matrix1.transpose(), Matrix((3, 3), [[1.0, 4.0, 7.0], [2.0, 5.0, 8.0], [3.0, 6.0, 9.0]]))
        self.assertEqual(self.matrix3.transpose(), Matrix((1, 4), [[7.0, 8.0, 0.0, 3.0]]))
        self.assertEqual(self.matrix4.transpose(), Matrix((4, 1), [[3.0], [15.0], [12.0], [5.0]]))            

    # Tests for inverse matrix
    def test_inverse(self):
        inverse = self.matrix6.inverse()
        test = Matrix((3, 3), [[3.0, 0.0, -1.0], [-8/3, 1/3, 2/3], [2/9, -1/9, 1/9]])    
        for i in range(self.matrix6.d[0]):
            for j in range(self.matrix6.d[1]):
                self.assertAlmostEqual(test.values[i][j], inverse.values[i][j])

    # Tests for error when attempting to inverse a singular matrix
    def test_singular_inverse(self):
        with self.assertRaises(ValueError):
            self.matrix1.inverse()

        with self.assertRaises(ValueError):
            self.matrix2.inverse()

        with self.assertRaises(ValueError):
            self.matrix3.inverse()

        with self.assertRaises(ValueError):
            self.matrix4.inverse()

    # Tests for conversion of matrix to vector
    def test_toVector(self):
        self.assertEqual(self.matrix2.toVector(), Vector(3, [2.0, 7.0, 1.0]))
        self.assertEqual(self.matrix3.toVector(), Vector(4, [7.0, 8.0, 0.0, 3.0]))

    # Tests for invalid conversion of matrix to vector
    def test_toVector_invalid(self):
        with self.assertRaises(ValueError):
            self.matrix1.toVector()

        with self.assertRaises(ValueError):
            self.matrix4.toVector()

        with self.assertRaises(ValueError):
            self.matrix5.toVector()

        with self.assertRaises(ValueError):
            self.matrix6.toVector()


if __name__ == '__main__':
    unittest.main()