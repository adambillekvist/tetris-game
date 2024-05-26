import unittest

def load_tests(loader, standard_tests, pattern):
    """ Load all tests in the tests directory """
    package_tests = loader.discover(start_dir='.', pattern='test_*.py')
    standard_tests.addTests(package_tests)
    return standard_tests

if __name__ == '__main__':
    unittest.main()