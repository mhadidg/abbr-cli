from docopt import docopt

from abbr import __main__
from abbr.core import main

_mocked_html = """
<html>
<table class="no-margin">
    <tbody>
        <tr>
            <dir>
                <span class="sf" />
                <span class="sf" />
            </dir>
            <p class="desc">term1</p>
            <td>
                <a>abbr1</a>
            </td>
            <p class="path">
                <a>category1</a>
            </p>
        </tr>
        <tr>
            <dir>
                <span class="sf" />
                <span class="sf" />
                <span class="sf" />
            </dir>
            <p class="desc">TERM2</p>
            <td>
                <a>ABBR2</a>
            </td>
            <p class="path">
                <a>category2</a>
            </p>
        </tr>
        <tr>
            <dir>
                <span class="sf" />
                <span class="sf" />
                <span class="sf" />
                <span class="sf" />
            </dir>
            <p class="desc">Term3</p>
            <td>
                <a>Abbr3</a>
            </td>
            <p class="path">
                <a>category3</a>
            </p>
        </tr>
    </tbody>
</table>
</html>
"""


def abbr_cli(args: str):
    args = docopt(__main__.__doc__, args.split())
    return main(args)
