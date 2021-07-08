import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

import requests

from tests import abbr_cli


class TestErrors(unittest.TestCase):

    def setUp(self):
        self.stdout: StringIO = patch('sys.stdout', new_callable=StringIO).start()
        self.stderr: StringIO = patch('sys.stderr', new_callable=StringIO).start()
        self.mock: MagicMock = patch('requests.get').start()

    def test_connection_error(self):
        self.mock.side_effect = requests.exceptions.ConnectionError
        abbr_cli("example")
        self.assertIn("connection failed", self.stderr.getvalue().lower())

    def test_connection_timeout(self):
        self.mock.side_effect = requests.exceptions.ConnectTimeout
        abbr_cli("example")
        self.assertIn("connection timed out", self.stderr.getvalue().lower())

    def test_unexpected_error(self):
        self.mock.side_effect = RuntimeError
        abbr_cli("example")
        self.assertIn("unexpected error", self.stderr.getvalue().lower())


if __name__ == '__main__':
    unittest.main()
