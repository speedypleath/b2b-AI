"""
    Testing module, creates a test suite containing all tests
"""
import unittest
from .logger_test import TestMock, TestMainLog
from .midi_test import TestMidiUtils

class Test(unittest.TestCase):
    """
    Test class which runs every test in module
    Args:
        unittest (_type_): _description_
    """
    def test_all(self) -> None:
        test_suite = unittest.TestSuite()
        test_suite.addTest(unittest.makeSuite(TestMock))
        test_suite.addTest(unittest.makeSuite(TestMainLog))
        test_suite.addTest(unittest.makeSuite(TestMidiUtils))
        test =  unittest.TextTestRunner(verbosity=3).run(test_suite)
        self.assertEqual(test.wasSuccessful(), True)
