from urllib.parse import urljoin
from pythonik.models.assets import Asset
from pythonik.models.base import Response
from pythonik.specs.base import Spec


class AssetSpec(Spec):
    server = "API/assets/"

    def get(self, asset_id: str) -> Response:
        """
        Get an iconik asset by id
        """

        resp = self._get("assets/{asset_id}/".format(asset_id=asset_id))

        return self.parse_response(resp, Asset)
