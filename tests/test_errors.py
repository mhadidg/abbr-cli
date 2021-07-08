import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

import requests

from tests import abbr_cli


class TestErrors(unittest.TestCase):

    def setUp(self):
        self.stdout_patch = patch('sys.stdout', new_callable=StringIO)
        self.stderr_patch = patch('sys.stderr', new_callable=StringIO)
        self.requests_patch = patch('requests.get')

        self.stdout: StringIO = self.stdout_patch.start()
        self.stderr: StringIO = self.stderr_patch.start()
        self.requests: MagicMock = self.requests_patch.start()

    def test_connection_error(self):
        self.requests.side_effect = requests.exceptions.ConnectionError
        abbr_cli("example")
        self.assertIn("connection failed", self.stderr.getvalue().lower())

    def test_connection_timeout(self):
        self.requests.side_effect = requests.exceptions.ConnectTimeout
        abbr_cli("example")
        self.assertIn("connection timed out", self.stderr.getvalue().lower())

    def test_unexpected_error(self):
        self.requests.side_effect = RuntimeError
        abbr_cli("example")
        self.assertIn("unexpected error", self.stderr.getvalue().lower())

    def tearDown(self) -> None:
        self.stdout_patch.stop()
        self.stderr_patch.stop()
        self.requests_patch.stop()


if __name__ == '__main__':
    unittest.main()
