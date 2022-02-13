import unittest
from tests.logger_test import TestMock, TestMainLog

class Test(unittest.TestCase):
    def test_all(self):           
        testSuite = unittest.TestSuite()
        testResult = unittest.TestResult()
        testSuite.addTest(unittest.makeSuite(TestMock))
        testSuite.addTest(unittest.makeSuite(TestMainLog))
        test =  unittest.TextTestRunner(verbosity=3).run(testSuite)
        self.assertEqual(test.wasSuccessful(), True)