import requests


class BackendClient(object):

    def __init__(self, query: str, _reversed: bool = False, order=0):
        self.query = query
        self.reversed = _reversed
        self.order = order

    def execute(self) -> tuple[int, str]:
        pass


class AbbreviationsClient(BackendClient):
    base_url = "https://www.abbreviations.com"

    def __init__(self, query: str, _reversed: bool = False, order=0):
        super().__init__(query, _reversed, order)

    def execute(self):
        query_type = 1 if self.reversed else 2  # allowed valuae are 1 (abbr->term) or 2 (term->abbr)
        order = self.order  # allowed values are 0 (popularity), 1 (alphabetically), and 2 (category)
        page = 99999  # page number; special number 99999 means retrive all pages
        params = {'st': self.query, 'o': order, 'qtype': query_type, 'p': page}
        response = requests.get(f"{self.base_url}/serp.php", params=params, allow_redirects=False)
        return response.status_code, response.text
