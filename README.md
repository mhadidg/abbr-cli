A command-line tool to look up abbreviations for terms (and the reverse). The abbreviations (or the terms in reverse
lookup) are extracted from [abbreviations.com](https://www.abbreviations.com).

```shell
$ abbr configuration
(5/5) cfg ~ Miscellaneous, Computing
(4/5) config ~ Governmental
(-/5) conf ~ Computing
(-/5) cnf ~ Computing

$ abbr --reverse alloc
(3/5) Allocation ~ Governmental
(-/5) Allocate ~ Business
```

## Table of content

- [Installation](#installation)
- [Exploring the arguments](#exploring-the-arguments)
- [A little better than abbreviations.com](#a-little-better-than-abbreviationscom)

## Installation

- Python version 3.6 or greater is required.
- Install via `pip` command:

```shell
pip install abbr-cli
```

## Exploring the arguments

```shell
$ abbr configuration
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
(5/5) cfg ~ Miscellaneous, Computing
(4/5) config ~ Governmental

$ abbr configuration --limit 1
(5/5) cfg ~ Miscellaneous, Computing
```

## A little better than abbreviations.com

- No duplicates.
- Abbreviations with a single charater are removed.
- A single abbreviation (or term in case of `--reverise` flag) with multiple cateogries (and sometimes subcategories)
  are merged in a single line. Subcategories are removed to avoid clutter. The rating will be the average rating.

```shell
# instead of getting
$ abbr command
(5/5) cmd ~ Governmental/NASA
(4/5) cmd ~ Governmental/Military
(4/5) cmd ~ Computing/DOSCommands
(5/5) cmd ~ Computing
(-/5) cmd ~ Miscellaneous/Aircraft
...

# you will get
$ abbr command
(4/5) cmd ~ Governmental, Computing, Miscellaneous
...
```

- Abbreviations are normalized to lowercase, while terms are normatlized to title case.

```shell
# instead of getting
$ abbr address
(4/5) ADD ~ Computing
(3/5) addr ~ Computing, Miscellaneous
...

# you will get
$ abbr address
(4/5) add ~ Computing
(3/5) addr ~ Computing, Miscellaneous
...
```
