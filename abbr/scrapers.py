import sys

from lxml import etree


class BaseScraper(object):

    def __init__(self, html: str, limit: int, min_stars: int, reversed_flag: bool):
        super().__init__()
        self.html = html
        self.limit = limit if limit > 0 else sys.maxsize
        self.min_stars = min_stars
        self.reversed = reversed_flag
        self._words: list[str] = list()
        self._words_stars: dict[int] = dict()
        self._words_categories: dict[set] = dict()
        self.parse()

    def parse(self):
        pass

    # noinspection PyMethodMayBeStatic
    def is_valid_word(self, word: str) -> bool:
        return len(word) > 1

    def normalize(self, word):
        if self.reversed:
            normalized = word.title()
        else:
            normalized = word.lower()
        return normalized

    def add_word(self, word: str):
        word = self.normalize(word)
        if word not in self._words:
            self._words.append(word)

    def add_word_stars(self, word: str, star_count: int):
        word = self.normalize(word)
        current_value = self._words_stars.get(word, 0)
        if current_value == 0:
            self._words_stars[word] = star_count
        elif star_count == 0:
            self._words_stars[word] = current_value
        else:
            self._words_stars[word] = round((current_value + star_count) / 2)

    def add_word_category(self, word: str, category: str):
        word = self.normalize(word)
        self._words_categories[word] = self._words_categories.get(word, set()) | {category}

    def words(self) -> list[str]:
        return self._words

    def words_stars(self) -> dict[int]:
        return self._words_stars

    def words_categories(self) -> dict[set]:
        return self._words_categories


class XPathScraper(BaseScraper):

    def __init__(self, html: str, limit: int = 0, min_stars=0, reversed_flag: bool = False):
        super().__init__(html, limit, min_stars, reversed_flag)

    def parse(self):
        elements = \
            etree.HTML(self.html).xpath(
                "//table[contains(@class,'no-margin')]/tbody/tr")  # type: list[etree._Element]

        if not elements:
            return

        total = 0
        for e in elements:
            star_count = int(e.xpath("count(.//span[contains(@class,'sf')])"))
            if star_count < self.min_stars:
                continue

            if self.reversed:
                word = e.xpath(".//p[contains(@class,'desc')]")[0].text
            else:
                word = e.xpath("./td[1]/a[1]")[0].text

            if not self.is_valid_word(word):
                continue

            self.add_word(word)
            self.add_word_stars(word, star_count)

            category = e.xpath(".//p[contains(@class,'path')]/a[1]")[0].text
            self.add_word_category(word, category)

            total += 1
            if total >= self.limit:
                break
