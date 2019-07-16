import unittest
from fractions import Fraction

from my_sum import sum

class TestSum(unittest.TestCase):
    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result, 6)

    def test_list_fraction(self):
        """
        Test that it can sum a list of fractions
        """
        data = [Fraction(1, 4), Fraction(1, 4), Fraction(2, 5)]
        result = sum(data)
        self.assertEqual(result, 1)

    def test_bad_type(self):
        data = "banana"
        with self.assertRaises(TypeError):
            result = sum(data)

if __name__ == '__main__':
    unittest.main()
# command line entry point
# if you execute the script alone by running this file at command line, it will call unittest.main()
# this executes the test runner by discovering all classes in this file that inherit from unittest.TestCase
# instead you can also use the unittest command line 'python -m unittest test' in terminal
# python -m unittest -v test can also be used
# the v means verbose, verbose mode lists the names of the tests it executed first, along with the result of each test
'''
Once you have multiple test files, as long as you follow the test*.py naming pattern,
you can provide the name of the directory instead by using the -s flag and the name of the directory

$ python -m unittest discover -s tests

if your source code is not in the directory root and contained in a subdirectory, for example in a folder called src/, 
you can tell unittest where to execute the tests so that it can import the modules correctly with the -t flag:

$ python -m unittest discover -s tests -t src
'''

'''
Web app development is different from normal testing
'''




