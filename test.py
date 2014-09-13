import unittest
import sys
import os

sys.path.append(os.getcwd())

if __name__ == '__main__':
    loader = unittest.TestLoader()
    tests = loader.discover('./tests')
    verbosity = 1
    if '-v' in sys.argv:
        verbosity = 2
    testRunner = unittest.TextTestRunner(verbosity=verbosity)
    testRunner.run(tests)
