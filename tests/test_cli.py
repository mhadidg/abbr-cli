import unittest
from io import StringIO
from unittest.mock import patch

from abbr import __main__
from abbr.clients import AbbreviationsClient
from tests import abbr_cli, _mocked_html


class TestCommandLine(unittest.TestCase):

    def setUp(self):
        self.stdout: StringIO = patch('sys.stdout', new_callable=StringIO).start()
        self.stderr: StringIO = patch('sys.stderr', new_callable=StringIO).start()
        patch.object(AbbreviationsClient, 'execute', return_value=(200, _mocked_html)).start()

    def test_help(self):
        with self.assertRaises(SystemExit):
            abbr_cli("--help")
        self.assertEqual(self.stdout.getvalue().strip(), __main__.__doc__.strip())

    def test_term_to_abbr_is_default(self):
        abbr_cli("term --only-words")
        self.assertCountEqual(self.stdout.getvalue().split(), ['abbr1', 'abbr2', 'abbr3'])

    def test_reversed(self):
        abbr_cli("-r abbr --only-words")
        self.assertCountEqual(self.stdout.getvalue().split(), ['Term1', 'Term2', 'Term3'])

    def test_limit(self):
        abbr_cli("example --only-words --limit 1")
        self.assertEqual(len(self.stdout.getvalue().split()), 1)

    def test_zero_limit_means_unlimited(self):
        abbr_cli("example --only-words --limit 0")
        self.assertGreater(len(self.stdout.getvalue().split()), 0)

    def test_min_stars(self):
        abbr_cli("example --only-words --min-stars 4")
        self.assertCountEqual(self.stdout.getvalue().split(), ['abbr3'])

    def test_zero_min_stars_means_all(self):
        abbr_cli("example --only-words --min-stars 0")
        self.assertEqual(len(self.stdout.getvalue().split()), 3)

    def test_result_order_in_html_respected(self):
        abbr_cli("example --only-words")
        self.assertListEqual(self.stdout.getvalue().split(), ['abbr1', 'abbr2', 'abbr3'])

    def test_fancy_output(self):
        abbr_cli("example")
        for line in self.stdout.getvalue().strip().split(sep='\n'):
            with self.subTest(line=line):
                self.assertRegex(line, r'\(\d/\d\)')
                self.assertIn("abbr", line)
                self.assertIn("category", line)


if __name__ == '__main__':
    unittest.main()
