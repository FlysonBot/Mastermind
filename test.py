import unittest

if __name__ == '__main__':
    # Discover and run all unittests in the 'tests' directory
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    
    runner = unittest.TextTestRunner()
    runner.run(suite)