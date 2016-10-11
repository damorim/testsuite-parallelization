# Wraps the Github Search API v3
# Ref.: https://developer.github.com/v3/search/
#
# Author: Jeanderson Candido
#
class Queryable:
    def query(self):
        pass


class RepositoryQuery(Queryable):
    def __init__(self):
        self._API_URL = "https://api.github.com/search/repositories"
        self._params = {"q": [],
                        "sort": None,
                        "order": None}

    def lang(self, criteria):
        self._params["q"].append("language:{0}".format(criteria))
        return self

    def stars(self, criteria):
        self._params["q"].append("stars:{0}".format(criteria))
        return self

    def query(self):
        qfield = "+".join(self._params["q"])
        url = "{base}?q={query_field}".format(base=self._API_URL,
                                              query_field=qfield)
        return url

