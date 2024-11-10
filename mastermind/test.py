import unittest
import sys
import os

# Determine the directory of this script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the tests directory
tests_dir = os.path.join(current_dir, 'tests')

# Add the tests directory to the system path
sys.path.insert(0, tests_dir)

if __name__ == '__main__':
    # Discover and run all unittests in the tests directory
    loader = unittest.TestLoader()
    suite = loader.discover(tests_dir)
    
    runner = unittest.TextTestRunner()
    runner.run(suite)