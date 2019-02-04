#!/usr/bin/python3
import unittest
import linear_systems_unoptimised as linear

# Make a new class for each function we want to test. These need to be derived
# from the base TestCase class in unittest
class TestVecNorm(unittest.TestCase):
    
    # In this test suite, we want to try to find ways to "break" the vecnorm
    # function. A good rule of thumb is to test for zero, positive, and 
    # negative inputs, as well as extreme input values (e.g. largest possible 
    # integer, not implemented here) and invalid input (e.g. a list of 
    # strings).

    # Test function names *must* begin with "test_", otherwise they will not
    # be run by unittest
    def test_zero(self):
        zero_vec = [0 for _ in range(3)]
        self.assertEqual(linear.vecnorm(zero_vec), 0.0)
    
    def test_pos(self):
        x = [1, 2, 3]
        self.assertEqual(linear.vecnorm(x), 14)

    def test_neg(self):
        x = [-1, -2, -3]
        self.assertEqual(linear.vecnorm(x), 14)

    def test_float(self):
        x = [0.5, -0.5, 1/8]
        self.assertEqual(linear.vecnorm(x), 5.15625e-1)

    def test_string(self):
        x = ['a', 'b', 'c']
        # Note: self.assertWarns is also useful to test for e.g. divide by 
        # zero errors
        with self.assertRaises(TypeError):
            linear.vecnorm(x)

if __name__ == "__main__":
    unittest.main()
