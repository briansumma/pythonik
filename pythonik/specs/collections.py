from pythonik.specs.base import Spec
from pythonik.models.base import Response
from pythonik.models.assets.collections import (
    Collection,
    CollectionContents,
    CollectionContentInfo,
)

BASE = "collections"
GET_URL = BASE + "/{}/"
GET_INFO = GET_URL + "content/info"
GET_CONTENTS = GET_URL + "contents"


class CollectionSpec(Spec):
    server = "API/assets/"

    def delete(self, collection_id: str) -> Response:
        resp = self._delete(GET_URL.format(collection_id))
        return self.parse_response(resp, None)

    def get(self, collection_id: str) -> Response:
        resp = self._get(GET_URL.format(collection_id))
        return self.parse_response(resp, Collection)

    def get_info(self, collection_id: str) -> Response:
        resp = self._get(GET_INFO.format(collection_id))
        return self.parse_response(resp, CollectionContentInfo)

    def get_contents(self, collection_id: str, **kwargs) -> Response:
        resp = self._get(GET_CONTENTS.format(collection_id), **kwargs)
        return self.parse_response(resp, CollectionContents)

    def create(self, body: Collection, exclude_defaults=True, **kwargs) -> Response:
        response = self._post(
            BASE, json=body.model_dump(exclude_defaults=exclude_defaults), **kwargs
        )
        return self.parse_response(response, Collection)
