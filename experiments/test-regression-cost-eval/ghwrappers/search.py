# Wraps the Github Search API v3
# Ref.: https://developer.github.com/v3/search/
#
# Author: Jeanderson Candido
#
class Paginatable:
    def at(self, page):
        pass
    def size(self, page_size):
        pass

class Queryable:
    def query(self):
        pass

class RepositoryQuery(Queryable, Paginatable):
    def __init__(self):
        self._API_URL = "https://api.github.com/search/repositories"
        self._page_size = 10
        self._page = 1
        self._params = {"q": [],
                        "sort": None,
                        "order": None}

    def lang(self, criteria):
        self._params["q"].append("language:{0}".format(criteria))
        return self

    def stars(self, criteria):
        self._params["q"].append("stars:{0}".format(criteria))
        return self

    def stars(self, criteria):
        self._params["q"].append("stars:{0}".format(criteria))
        return self

    def at(self, page):
        self._page = page
        return self

    def size(self, page_size):
        self._page_size = page_size
        return self

    def query(self):
        qfield = "+".join(self._params["q"])
        url = "{base}?q={query_field}".format(base=self._API_URL,
                                              query_field=qfield)

        url = "{prefix}&page={page}&per_page={sz}".format(prefix=url,
                                                          page=self._page,
                                                          sz=self._page_size)

        return url

