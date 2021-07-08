"""Look up abbreviations for terms (or the reverse).

Usage:
  abbr [options] <term>
  abbr [options] -r <abbreviation>
  abbr (-h | --help)
  abbr --version

Options:
  --version           Show version.
  -h --help           Show this screen.
  -r --reverse        Reverse the look up. Find terms for an abbreviation.
  -n --limit <n>      Limit the number of result [default: 25].
  -m --min-stars <m>  Include only items with number of stars equal or above <m>.
                      Allowed values are 0-5 (inclusive) [default: 0].
  -w --only-words     List only the words (terms or abbreviations) without category
                      and rating. Helpful when used in a bash script.

"""

import sys

from docopt import docopt

import abbr
from abbr import core
from abbr.exitstatus import ExitStatus


def main():
    try:
        exit_status = core.main(docopt(__doc__, version=f'abbr {abbr.__version__}'))
    except KeyboardInterrupt:
        exit_status = ExitStatus.ERROR_CTRL_C

    sys.exit(exit_status.value)


if __name__ == '__main__':
    main()
