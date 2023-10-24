from pythonik.models.base import Response
from pythonik.models.search.search_body import SearchBody
from pythonik.models.search.search_response import SearchResponse
from pythonik.specs.base import Spec


SEARCH_PATH = "search/"


class SearchSpec(Spec):
    server = "API/search"

    def search(self, search_body: SearchBody, **kwargs) -> Response:
        """search iconik"""
        resp = self._post(SEARCH_PATH, **kwargs)
        return self.parse_response(resp, SearchResponse)
