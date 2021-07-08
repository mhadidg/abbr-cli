import unittest
from io import StringIO
from unittest.mock import patch

from tests import abbr_cli


class TestBackend(unittest.TestCase):

    def setUp(self):
        self.stdout: StringIO = patch('sys.stdout', new_callable=StringIO).start()
        self.stderr: StringIO = patch('sys.stderr', new_callable=StringIO).start()

    def test_default(self):
        abbr_cli("example --only-words")
        self.assertTrue(len(self.stdout.getvalue().split()) > 0)

    def test_reversed(self):
        abbr_cli("-r ex --only-words")
        self.assertTrue(len(self.stdout.getvalue().split()) > 0)

    def test_wrong_flag(self):
        abbr_cli("-r example")
        self.assertIn("don't use -r flag", self.stdout.getvalue())
        abbr_cli("ex")
        self.assertIn("use with -r flag", self.stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
