import unittest
import math
from matrix import Matrix
from vector import Vector

class VectorTest(unittest.TestCase):
    
    # Sets up the vectors being used in the tests
    def setUp(self):
        self.vector1 = Vector(3, [1.0, 2.0, 3.0])
        self.vector2 = Vector(3, [4.0, 5.0, 6.0])
        self.vector3 = Vector(2, [7.0, 8.0])
        self.vector4 = Vector(4, [3.0, 15.0, 12.0, 5.0])

    # Ensures that vectors are correctly being initialized 
    def test_initialization(self):
        v = Vector(3, [1.0, 2.0, 3.0])
        self.assertEqual(v.d, 3)
        self.assertEqual(v.values, [1.0, 2.0, 3.0])

    # Tests vector initialisation error (e.g mismatch of dimensions)
    def test_initialization_dimension_mismatch(self):
        with self.assertRaises(ValueError):
            Vector(3, [1.0, 2.0])  # Dimensions don't match the number of values

    # Tests vector scaling
    def test_scale(self):
        scaled_v1 = self.vector1.scale(2)
        scaled_v2 = self.vector2.scale(3)
        scaled_v3 = self.vector3.scale(4)
        scaled_v4 = self.vector4.scale(5)
        self.assertEqual(scaled_v1.values, [2.0, 4.0, 6.0])
        self.assertEqual(scaled_v2.values, [12.0, 15.0, 18.0])
        self.assertEqual(scaled_v3.values, [28.0, 32.0])
        self.assertEqual(scaled_v4.values, [15.0, 75.0, 60.0, 25.0])

    # Tests zero scaling    
    def test_scale_zero(self):
        scaled_v = self.vector1.scale(0)
        self.assertEqual(scaled_v.values, [0.0, 0.0, 0.0])

    # Tests negative scaling
    def test_scale_negative(self):
        scaled_v = self.vector1.scale(-1)
        self.assertEqual(scaled_v.values, [-1.0, -2.0, -3.0])

    # Tests vector addition
    def test_add(self):
        v = self.vector1.add(self.vector2)
        self.assertEqual(v.values, [5.0, 7.0, 9.0])

    # Tests mismatch dimensions between 2 vectors undergoing addition
    def test_add_dimension_mismatch(self):
        with self.assertRaises(ValueError):
            self.vector1.add(self.vector3)  # Vectors don't have the same dimensions
        
        with self.assertRaises(ValueError):
            self.vector1.add(self.vector4)  # Vectors don't have the same dimensions

    # Tests vector magnitude calculations 
    def test_magnitude(self):
        self.assertAlmostEqual(self.vector1.magnitude(), math.sqrt(14))
        self.assertAlmostEqual(self.vector2.magnitude(), math.sqrt(77))
        self.assertAlmostEqual(self.vector3.magnitude(), math.sqrt(113))
        self.assertAlmostEqual(self.vector4.magnitude(), math.sqrt(403))

    # Test for 0 magnitude vector
    def test_magnitude_zero_vector(self):
        zero_vector = Vector(3, [0.0, 0.0, 0.0])
        self.assertAlmostEqual(zero_vector.magnitude(), 0.0)

    # Test for normalization of a vector
    def test_normalize(self):
        normalized_v = self.vector1.normalize()
        self.assertAlmostEqual(normalized_v.magnitude(), 1.0)
        expected_values = [val / math.sqrt(14) for val in self.vector1.values]
        for i in range(len(self.vector1.values)):
            self.assertAlmostEqual(expected_values[i], normalized_v.values[i])

    # Test for normalizing a zero vector 
    def test_normalize_zero_vector(self):
        zero_vector = Vector(3, [0.0, 0.0, 0.0])
        with self.assertRaises(ZeroDivisionError):
            zero_vector.normalize()

    # Test for dot product vector operation
    def test_dot_product(self):
        self.assertAlmostEqual(self.vector1.dotProduct(self.vector2), 32.0)

    # Test for 0 dot product for orthogonal vectors
    def test_dot_product_orthogonal_vectors(self):
        v1 = Vector(2, [1.0, 0.0])
        v2 = Vector(2, [0.0, 1.0])
        self.assertAlmostEqual(v1.dotProduct(v2), 0.0)

    # Test for dot product with mismatch dimensions
    def test_dot_product_dimension_mismatch(self):
        with self.assertRaises(ValueError):
            self.vector1.dotProduct(self.vector3)  # Vectors don't have the same dimensions

    # Test for angle between 2 vectors
    def test_angle(self):
        self.assertAlmostEqual(self.vector1.angle(self.vector2), 12.9331545)

    # Test for angle between orthogonal vectors
    def test_angle_orthogonal(self):
        v1 = Vector(2, [1.0, 0.0])
        v2 = Vector(2, [0.0, 1.0])
        self.assertAlmostEqual(v1.angle(v2), 90.0)

    # Test for angle between parallel vectors
    def test_angle_parallel_vectors(self):
        v1 = Vector(2, [1.0, 0.0])
        v2 = Vector(2, [2.0, 0.0])
        self.assertAlmostEqual(v1.angle(v2), 0.0)

    # Test for conversion between a vector to a matrix
    def test_toMatrix(self):
        self.assertEqual(self.vector1.toMatrix(), Matrix((3,1), [[1.0], [2.0], [3.0]]))
        self.assertEqual(self.vector2.toMatrix(), Matrix((3,1), [[4.0], [5.0], [6.0]]))
        self.assertEqual(self.vector3.toMatrix(), Matrix((2,1), [[7.0], [8.0]]))
        self.assertEqual(self.vector4.toMatrix(), Matrix((4,1), [[3.0], [15.0], [12.0], [5.0]]))


if __name__ == '__main__':
    unittest.main()
    