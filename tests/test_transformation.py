# Tests for transformation module
import unittest
from src.transformations.vector import Vector
from src.transformations.transformation import translation, projection, shearing, scaling, reflection, rotation

# Tests for on standard linear transformations
class TestTransformations(unittest.TestCase):
    # Setup vectors for transformation tests
    def setUp(self):
        self.v1 = Vector([1, 2])
        self.v2 = Vector([3, 4])
        self.u = Vector([1, 0])
        self.origin = Vector([0, 0])
        self.v_zero = Vector([0, 0])
        self.angle = 90

    # Translation tests
    def test_translation(self):
        translated = translation(self.v1, self.v2)
        expected = Vector([4, 6])
        self.assertEqual(translated, expected)

        translated_zero = translation(self.v_zero, self.v2)
        expected_zero = self.v2
        self.assertEqual(translated_zero, expected_zero)

        translated_negative = translation(self.v1, Vector([-1, -1]))
        expected_negative = Vector([0, 1])
        self.assertEqual(translated_negative, expected_negative)

    # Projection tests
    def test_projection(self):
        projected = projection(self.v1, self.u)
        expected = Vector([1, 0])
        self.assertEqual(projected, expected)

        projected_zero = projection(self.v_zero, self.u)
        expected_zero = self.v_zero
        self.assertEqual(projected_zero, expected_zero)

        projected_negative = projection(Vector([-1, -2]), self.u)
        expected_negative = Vector([-1, 0])
        self.assertEqual(projected_negative, expected_negative)

    # Shearing tests
    def test_shearing(self):
        sheared = shearing(self.v1, 2, 3)
        expected = Vector([5, 5])
        self.assertEqual(sheared, expected)

        sheared_zero = shearing(self.v_zero, 2, 3)
        expected_zero = self.v_zero
        self.assertEqual(sheared_zero, expected_zero)

        sheared_negative = shearing(self.v1, -1, -1)
        expected_negative = Vector([-1, 1])
        self.assertEqual(sheared_negative, expected_negative)

        sheared_large = shearing(self.v1, 100, 200)
        expected_large = Vector([201, 202])
        self.assertEqual(sheared_large, expected_large)

    # Scaling tests
    def test_scaling(self):
        scaled = scaling(self.v1, 2, 3)
        expected = Vector([2, 6])
        self.assertEqual(scaled, expected)

        scaled_zero = scaling(self.v_zero, 2, 3)
        expected_zero = self.v_zero
        self.assertEqual(scaled_zero, expected_zero)

        scaled_negative = scaling(self.v1, -1, -1)
        expected_negative = Vector([-1, -2])
        self.assertEqual(scaled_negative, expected_negative)

        scaled_large = scaling(self.v1, 100, 100)
        expected_large = Vector([100, 200])
        self.assertEqual(scaled_large, expected_large)

    # Reflection tests
    def test_reflection(self):
        reflected = reflection(self.v1, self.u)
        expected = Vector([1, -2])
        self.assertEqual(reflected, expected)

        reflected_zero = reflection(self.v_zero, self.u)
        expected_zero = self.v_zero
        self.assertEqual(reflected_zero, expected_zero)

        reflected_negative = reflection(Vector([-1, -2]), self.u)
        expected_negative = Vector([-1, 2])
        self.assertEqual(reflected_negative, expected_negative)

        reflected_large = reflection(Vector([100, 200]), self.u)
        expected_large = Vector([100, -200])
        self.assertEqual(reflected_large, expected_large)

    # Rotation tests
    def test_rotation(self):
        rotated = rotation(self.v1, self.origin, self.angle)
        expected = Vector([2, -1])
        self.assertEqual(rotated, expected)

        rotated_zero = rotation(self.v_zero, self.origin, self.angle)
        expected_zero = self.v_zero
        self.assertEqual(rotated_zero, expected_zero)

        rotated_180 = rotation(self.v1, self.origin, 180)
        expected_180 = Vector([-1, -2])
        self.assertEqual(rotated_180, expected_180)

        rotated_large = rotation(Vector([10, 20]), self.origin, 45)
        expected_large = Vector([21.213203435596426, 7.071067811865475])
        self.assertEqual(rotated_large, expected_large)

    # Zero vector tests
    def test_zero_vector_translation(self):
        translated = translation(self.v_zero, self.v2)
        expected = self.v2
        self.assertEqual(translated, expected)

    def test_zero_vector_projection(self):
        projected = projection(self.v_zero, self.u)
        expected = self.v_zero
        self.assertEqual(projected, expected)

    def test_zero_vector_reflection(self):
        reflected = reflection(self.v_zero, self.u)
        expected = self.v_zero
        self.assertEqual(reflected, expected)

    def test_scaling_by_zero(self):
        scaled = scaling(self.v1, 0, 0)
        expected = self.v_zero
        self.assertEqual(scaled, expected)

    def test_negative_scaling(self):
        scaled = scaling(self.v1, -1, -1)
        expected = Vector([-1, -2])
        self.assertEqual(scaled, expected)

    # Edge case tests
    def test_rotation_edge_case(self):
        rotated = rotation(self.v1, self.origin, 0)
        expected = self.v1
        self.assertEqual(rotated, expected)

    def test_large_translation(self):
        large_translation = translation(self.v1, Vector([1000, 2000]))
        expected = Vector([1001, 2002])
        self.assertEqual(large_translation, expected)

    # Cache max limit test
    def test_cache_size_limit(self):
        self.assertEqual(translation.cache_info().maxsize, 1024)
        self.assertEqual(projection.cache_info().maxsize, 1024)
        self.assertEqual(shearing.cache_info().maxsize, 1024)
        self.assertEqual(scaling.cache_info().maxsize, 1024)
        self.assertEqual(reflection.cache_info().maxsize, 1024)
        self.assertEqual(rotation.cache_info().maxsize, 1024)


if __name__ == '__main__':
    unittest.main()