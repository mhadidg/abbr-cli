import sys

import colorful as cf
from requests.exceptions import ConnectionError, ConnectTimeout

from abbr.clients import AbbreviationsClient
from abbr.exitstatus import ExitStatus
from abbr.scrapers import XPathScraper

_repo_url = 'https://github.com/mhadidg/abbr-cli'

_color_palette = {
    'red': '#EF5350',
    'abbr': '#FFFFFF',
    'rating': '#FFFFFF',
    'star': '#757575',
    'starBraket': '#757575',
    'category': '#757575',
    'categorySeparator': '#757575',
}


# noinspection PyBroadException
def main(args) -> ExitStatus:
    cf.use_palette(_color_palette)

    term = args['<term>']
    abbrv = args['<abbreviation>']
    reversed_flag = args['--reverse']
    min_stars = int(args['--min-stars'])
    fancy_output = not args['--only-words']
    limit = int(args['--limit'])

    query = abbrv if reversed_flag else term

    try:
        status_code, html = AbbreviationsClient(query, reversed_flag).execute()
    except ConnectTimeout:
        eprint(f"Connection timed out!")
        return ExitStatus.ERROR
    except ConnectionError:
        eprint(f"Connection failed! Make sure you're connected to the internet.")
        return ExitStatus.ERROR
    except Exception:
        eprint(f"Unexpected error! Please report the issue on {_repo_url}.")
        return ExitStatus.ERROR

    if status_code == 302:
        if reversed_flag and fancy_output:
            print("Zero terms. Is {} a term? Then don't use -r flag.".format(cf.bold_red(abbrv)))
        elif fancy_output:
            print("Zero abbreviations. Is {} an abbreviation? Then use with -r flag.".format(cf.bold_red(term)))
        return ExitStatus.SUCCESS

    try:
        scraper = XPathScraper(html, limit, min_stars, reversed_flag)
    except Exception:
        eprint(f"Unexpected Error! Please report the issue on {_repo_url}.")
        return ExitStatus.ERROR

    # The 'words' here could be either abbreivations or terms
    # depending on whether or not the --reverse flag is present.
    words = scraper.words()

    if not words:
        if reversed_flag and fancy_output:
            print("Zero terms.")
        elif fancy_output:
            print("Zero abbreviations.")
        return ExitStatus.SUCCESS

    if fancy_output:
        words_stars = scraper.words_stars()
        words_categories = scraper.words_categories()
        simplified_fancy_print(words, words_categories, words_stars)
    else:
        simple_print(words)

    return ExitStatus.SUCCESS


def fancy_print(words: list[str], category_dict: dict[set], star_dict: dict[int]):
    for abbr in words:
        star_count = star_dict[abbr]
        category = ', '.join(category_dict[abbr])
        filling_spaces = (' ' * (5 - star_count))
        print(
            cf.starBraket(" [{}] ".format(cf.star('×' * star_count) + filling_spaces))
            + cf.abbr(abbr)
            + cf.categorySeparator(' ~ ')
            + cf.category(category))


def simplified_fancy_print(words: list[str], category_dict: dict[set], star_dict: dict[int]):
    for abbr in words:
        star_count = star_dict[abbr]
        category = ', '.join(category_dict[abbr])
        print(
            "({}) ".format('{}/5'.format('-' if star_count == 0 else star_count))
            + abbr
            + cf.categorySeparator(' ~ ')
            + cf.category(category))


def simple_print(words: list[str]):
    for abbr in words:
        print(abbr)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
