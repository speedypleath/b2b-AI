import logging
import unittest
import time
import os
from b2b_AI.utils.logging import get_logger

class MockLogHandler(logging.Handler):
    records = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)

    def setFormatter(self, fmt: logging.Formatter | None) -> None:
        return super().setFormatter(fmt)
    
class TestMock(unittest.TestCase):
    logger = logging.getLogger("mock")
    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger("mock")
        logger.setLevel(logging.DEBUG)
        cls._mock_logger = MockLogHandler(level='DEBUG')
        cls._mock_logger.setFormatter(logging.Formatter('["%(levelname)s" - %(asctime)s]: %(message)s'))
        logger.addHandler(cls._mock_logger)

    def setUp(self):
        self._mock_logger.records = []

    def test_debug(self):
        self.logger.debug("This is a debug")
        self.assertEqual(len(self._mock_logger.records), 1)
        self.assertEqual("This is a debug", self._mock_logger.records[0].getMessage())
        self.assertEqual(self._mock_logger.records[0].levelno, logging.DEBUG)
        
    def test_info(self):
        self.logger.info("This is an info")
        self.assertEqual(len(self._mock_logger.records), 1)
        self.assertEqual("This is an info", self._mock_logger.records[0].getMessage())
        self.assertEqual(self._mock_logger.records[0].levelno, logging.INFO)

    def test_warning(self):
        self.logger.warning("This is a warning")
        self.assertEqual(len(self._mock_logger.records), 1)
        self.assertEqual("This is a warning", self._mock_logger.records[0].getMessage())
        self.assertEqual(self._mock_logger.records[0].levelno, logging.WARNING)

    def test_error(self):
        self.logger.error("This is an error")
        self.assertEqual(len(self._mock_logger.records), 1)
        self.assertEqual("This is an error", self._mock_logger.records[0].getMessage())
        self.assertEqual(self._mock_logger.records[0].levelno, logging.ERROR)
    
    def test_time(self):
        self.logger.info("This is an info")
        self.assertAlmostEqual(time.time(), self._mock_logger.records[0].created, delta=1)

class TestMainLog(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = os.path.join(os.path.dirname(__file__), "test.logs")
        cls._logger = get_logger(path)
        cls._file = open(path, "r")
            
    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(os.path.join(os.path.dirname(__file__), "test.logs"))
        
    def test_file_exists(self):
        self.assertTrue(os.path.join(os.path.dirname(__file__), "test.logs"))
        
    def test_message(self):
        self._logger.info("This is an info")
        self.assertEqual(self._file.read(), f'["INFO" - {time.strftime("%Y-%m-%d %H:%M:%S")}]: This is an info in {os.path.realpath(__file__)}:72\n')

def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMock))
    suite.addTest(unittest.makeSuite(TestMainLog))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=3).run(create_suite())