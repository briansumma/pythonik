from pythonik.models.base import Response
from pythonik.models.files.format import Format
from pythonik.models.files.proxy import Proxy
from pythonik.specs.base import Spec

GET_ASSET_PROXY_PATH = "assets/{}/proxies/{}/"
GET_ASSETS_FORMATS_PATH = "assets/{}/formats/"
GET_ASSETS_FORMAT_PATH = "assets/{}/formats/{}"


class FilesSpec(Spec):
    server = "API/files/"

    def get_asset_proxy(self, asset_id: str, proxy_id: str) -> Response:
        """Get asset's proxy
        Returns: Response(model=Proxy)
        """

        resp = self._get(GET_ASSET_PROXY_PATH.format(asset_id, proxy_id))

        return self.parse_response(resp, Proxy)

    def get_asset_formats(self, asset_id: str, **kwargs) -> Response:
        """Get all asset's formats"""
        resp = self._get(GET_ASSETS_FORMATS_PATH.format(asset_id), **kwargs)

        return self.parse_response(resp, Format)

    def get_asset_format(self, asset_id: str, format_id: str, **kwargs) -> Response:
        """Get asset format"""
        resp = self._get(GET_ASSETS_FORMAT_PATH.format(asset_id, format_id), **kwargs)

        return self.parse_response(resp, Format)
