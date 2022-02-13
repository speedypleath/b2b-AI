import unittest
from tests.logger_test import TestMock, TestMainLog

def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMock))
    suite.addTest(unittest.makeSuite(TestMainLog))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=3).run(create_suite())