import unittest
from tests.logger_test import TestMock

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMock)
    unittest.TextTestRunner(verbosity=3).run(suite)