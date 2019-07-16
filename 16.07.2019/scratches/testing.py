'''
Testing
1. integration test - checks components
2. unit test - checks a small component
'''
'''
'Integration test'

assert sum([1,2,3]) == 3, "Should be 6"
# an error message displays - result incorrect
'''


'Using a test runner'
# unittest is one library built into python for testing
'''
Unittest
- contains both a testing framework and a test runner
- requires
    put tests into classes as methods
    use a series of special assertion methods in the unittest - TestCase class instead of assert statement
'''
'''
import unittest


class TestSum(unittest.TestCase):
# Create a class called TestSum that inherits from the TestCase class

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
# Convert the test functions into methods by adding self as the first argument
# Change the assertions to use the self.assertEqual() method on the TestCase class

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()
# Change the command-line entry point to call unittest.main()
# in python 2.7 and below, unittest is called unittest 2
'''

'''
Nose
- compatible with any tests written using the unittest framework
- run nose2 in shell/terminal
- it checks all the files in the project folder
'''

'''
Pytest
- supports execution of unittest test cases
- pytest test cases are a series of functions in a python file starting with the name test_
- pros
    support for the built-in assert statement instead of using special self.assert*() methods
    support for filtering for test cases
    ability of rerun from the last failing test
    an ecosystem of plugins to extend the functionality
'''
def test_sum():
    assert sum([1, 2, 3]) == 6, "Should be 6"

def test_sum_tuple():
    assert sum((1, 2, 2)) == 6, "Should be 6"
# just like nose, run in terminal

'''
Structure a simple test
1. write test code and test with sample data
2. write assertions
    make sure tests are repeatable and run test for multiple times
    try and assert results that relate to input data
    .assertEqual(a, b)
        a == b
    .assertTrue(x)
        bool(x) is True
    .assertFalse(x)
        bool(x) is False
    .assertIs(a, b)
        a is b
    .assertIsNone(x)
        x is None
    .assertIn(a, b)
        a in b
    .assertIsInstance(a, b)
        isinstance(a, b)
'''

'''
Side effects
- executing a piece of code will alter other things in the environment
- E.g. the attribute of a class, a file on the filesystem, a value in a database
- decide if the side effect is being tested before including it in the list of assertions
'''