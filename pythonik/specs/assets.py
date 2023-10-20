from pythonik.models.assets.assets import Asset
from pythonik.models.base import Response
from pythonik.specs.base import Spec

GET_URL = "assets/{}/"


class AssetSpec(Spec):
    server = "API/assets/"

    def get(self, asset_id: str) -> Response:
        """
        Get an iconik asset by id
        Returns: Response(model=Asset)
        """

        resp = self._get(GET_URL.format(asset_id))

        return self.parse_response(resp, Asset)
