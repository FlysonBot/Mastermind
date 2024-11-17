import unittest

if __name__ == "__main__":
    # Discover and run all tests in the tests package
    loader = unittest.TestLoader()
    suite = loader.discover('tests')  # Looks in tests/ for all test files

    runner = unittest.TextTestRunner()
    runner.run(suite)
