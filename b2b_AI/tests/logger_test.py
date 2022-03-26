from logging import LogRecord, Formatter, Handler, getLogger, DEBUG, INFO, WARNING, ERROR
from unittest import TestCase
from io import StringIO
import time
import os
import sys
from b2b_ai.utils.logging import get_logger


class MockLogHandler(Handler):
    """
    Class for mocking an Handler
    """
    records = []

    def emit(self, record: LogRecord) -> None:
        self.records.append(record)


class TestMock(TestCase):
    """
    Class for testing a mocked Handler
    """
    logger = getLogger('mock')

    @classmethod
    def setUpClass(cls):
        logger = getLogger('mock')
        logger.setLevel(DEBUG)
        cls._mock_logger = MockLogHandler(level='DEBUG')
        cls._mock_logger.setFormatter(
            Formatter('["%(levelname)s" - %(asctime)s]: %(message)s'))
        logger.addHandler(cls._mock_logger)

    def setUp(self):
        self._mock_logger.records = []

    def test_debug(self):
        self.logger.debug('This is a debug')
        self.assertEqual(len(self._mock_logger.records), 1)
        self.assertEqual('This is a debug',
                         self._mock_logger.records[0].getMessage())
        self.assertEqual(self._mock_logger.records[0].levelno, DEBUG)

    def test_info(self):
        self.logger.info('This is an info')
        self.assertEqual(len(self._mock_logger.records), 1)
        self.assertEqual('This is an info',
                         self._mock_logger.records[0].getMessage())
        self.assertEqual(self._mock_logger.records[0].levelno, INFO)

    def test_warning(self):
        self.logger.warning('This is a warning')
        self.assertEqual(len(self._mock_logger.records), 1)
        self.assertEqual('This is a warning',
                         self._mock_logger.records[0].getMessage())
        self.assertEqual(self._mock_logger.records[0].levelno, WARNING)

    def test_error(self):
        self.logger.error('This is an error')
        self.assertEqual(len(self._mock_logger.records), 1)
        self.assertEqual('This is an error',
                         self._mock_logger.records[0].getMessage())
        self.assertEqual(self._mock_logger.records[0].levelno, ERROR)

    def test_time(self):
        self.logger.info('This is an info')
        self.assertAlmostEqual(
            time.time(), self._mock_logger.records[0].created, delta=1)


class TestMainLog(TestCase):
    """
    Class for testing the main log
    """
    @classmethod
    def setUpClass(cls) -> None:
        path = os.path.join(os.path.dirname(__file__), 'test.logs')
        sys.stdout = StringIO()
        cls._logger = get_logger(path, level=DEBUG, handle_console=True)
        # pylint: disable="consider-using-with"
        cls._file = open(path, 'r', encoding='UTF-8')
        cls._logger.info('This is an info')
        cls._output = sys.stdout.getvalue()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._file.close()
        os.remove(os.path.join(os.path.dirname(__file__), 'test.logs'))

    def test_file_exists(self):
        self.assertTrue(os.path.join(os.path.dirname(__file__), 'test.logs'))

    def test_message_file(self):
        self.assertEqual(
        self._file.read(),
        f'["INFO" - {time.strftime("%Y-%m-%d %H:%M:%S")}]: This is an info in ' +
        f'{os.path.realpath(__file__)}:83\n')

    def test_message_stdout(self):
        self.assertEqual(
        self._output,
        f'["INFO" - {time.strftime("%Y-%m-%d %H:%M:%S")}]: This is an info in ' +
        f'{os.path.realpath(__file__)}:83\n')
