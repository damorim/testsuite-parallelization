# Wraps the Github Search API v3
# Ref.: https://developer.github.com/v3/search/
#
# Author: Jeanderson Candido


class Paging:
    def at(self, page):
        pass

    def size(self, page_size):
        pass


class Queryable:
    def query(self):
        pass


class RepositoryQuery(Queryable, Paging):
    def __init__(self, criteria):
        self._API_URL = "https://api.github.com/search/repositories"
        self._criteria = criteria

        self._page_size = None
        self._page = None

    def at(self, page):
        self._page = page
        return self

    def size(self, page_size):
        self._page_size = page_size
        return self

    def query(self):
        query_args = []
        for k, v in self._criteria.items():
            query_args.append("{}:{}".format(k, v))

        qfield = "+".join(query_args)

        url = "{base}?q={query_field}".format(base=self._API_URL,
                                              query_field=qfield)

        if self._page:
            url = "{prefix}&page={page}".format(prefix=url, page=self._page)
        if self._page_size:
            url = "{prefix}&per_page={sz}".format(prefix=url, sz=self._page_size)

        return url
