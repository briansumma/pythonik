from pythonik.models.base import Response
from pythonik.models.files.proxy import Proxy
from pythonik.specs.base import Spec

GET_ASSET_PROXY_PATH = "assets/{}/proxies/{}/"


class FilesSpec(Spec):
    server = "API/files/"

    def get_asset_proxy(self, asset_id: str, proxy_id: str) -> Response:
        """Get asset's proxy
        Returns: Response(model=Proxy)
        """

        resp = self._get(GET_ASSET_PROXY_PATH.format(asset_id, proxy_id))

        return self.parse_response(resp, Proxy)
