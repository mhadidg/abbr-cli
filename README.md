# abbr-cli

A command-line tool to look up abbreviations for terms (and the reverse). The abbreviations, or the terms in reverse
lookup, are extracted from [abbreviations.com](https://www.abbreviations.com).

```
$ abbr configuration
(5/5) cfg
(4/5) config
(-/5) conf
(-/5) cnf

$ abbr --reverse alloc
(3/5) Allocation
(-/5) Allocate
```

## Table of content

- [Installation](#installation)
- [Exploring the arguments](#exploring-the-arguments)
    - [The documentation](#the-documentation)
    - [...In action](#in-action)
- [A little better than abbreviations.com](#a-little-better-than-abbreviationscom)

## Installation

- Python version 3.6 or greater is required.
- Install via `pip` command:

```
$ pip install abbr-cli
```

## Exploring the arguments

### The documentation

```
$ abbr -h
Look up abbreviations for terms.

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
  -c --with-category  Include categories along with the word.
```

### ...In action

```
$ abbr configuration
(5/5) cfg
(4/5) config
(-/5) conf
(-/5) cnf

$ abbr configuration --with-category
(5/5) cfg ~ Miscellaneous, Computing
(4/5) config ~ Governmental
(-/5) conf ~ Computing
(-/5) cnf ~ Computing

$ abbr configuration --only-words
cfg
config
conf
cnf

$ abbr configuration --min-stars 4
(5/5) cfg
(4/5) config

$ abbr configuration --limit 1
(5/5) cfg
```

## A little better than abbreviations.com

- No duplicates.
- Single-character abbreviations are excluded.
- A single abbreviation (or term in case of `--reverse` flag) with multiple categories (and sometimes subcategories)
  are merged in a single line. Subcategories are removed to avoid clutter. The rating will be the average rating.

```
# instead of getting
$ abbr command --with-category
(5/5) cmd ~ Governmental/NASA
(4/5) cmd ~ Governmental/Military
(4/5) cmd ~ Computing/DOSCommands
(5/5) cmd ~ Computing
(-/5) cmd ~ Miscellaneous/Aircraft
...

# you will get
$ abbr command --with-category
(4/5) cmd ~ Governmental, Computing, Miscellaneous
...
```

- Abbreviations are normalized to lowercase, while terms are normalized to title case.
