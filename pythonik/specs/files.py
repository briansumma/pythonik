from pythonik.models.base import Response
from pythonik.models.files.file import Files, File, FileCreate, FileSetCreate, FileSet, FileSets
from pythonik.models.files.format import Formats, Format, FormatCreate
from pythonik.models.files.proxy import Proxies, Proxy
from pythonik.models.files.storage import Storage, Storages
from pythonik.specs.base import Spec

GET_ASSET_PROXY_PATH = "assets/{}/proxies/{}/"
GET_ASSET_PROXIES_PATH = "assets/{}/proxies/"
GET_ASSETS_FORMATS_PATH = "assets/{}/formats/"
GET_ASSETS_FORMAT_PATH = "assets/{}/formats/{}"
GET_ASSETS_FILES_PATH = "assets/{}/files/"
GET_ASSETS_FILE_SET_PATH = "assets/{}/file_sets/"
GET_STORAGE_PATH = "storages/{}"
GET_STORAGES_PATH = "storages/"


class FilesSpec(Spec):
    server = "API/files/"

    def get_asset_proxy(self, asset_id: str, proxy_id: str) -> Response:
        """Get asset's proxy
        Returns: Response(model=Proxy)
        """

        resp = self._get(GET_ASSET_PROXY_PATH.format(asset_id, proxy_id))

        return self.parse_response(resp, Proxy)

    def create_asset_proxy(self, asset_id: str, body: Proxy, exclude_defaults=True, **kwargs) -> Response:
        """
        Create proxy and associate to asset
        Returns: Response(model=Proxy)
        """
        response = self._post(
            GET_ASSET_PROXIES_PATH.format(asset_id),
            json=body.model_dump(exclude_defaults=exclude_defaults),
            **kwargs
        )
        return self.parse_response(response, Proxy)

    def get_asset_proxies(self, asset_id: str):
        resp = self._get(GET_ASSET_PROXIES_PATH.format(asset_id))

        return self.parse_response(resp, Proxies)

    def create_asset_format(self, asset_id: str, body: FormatCreate, exclude_defaults=True, **kwargs) -> Response:
        """
        Create format and associate it to asset
        Returns: Response(model=Format)
        """
        response = self._post(
            GET_ASSETS_FORMATS_PATH.format(asset_id),
            json=body.model_dump(exclude_defaults=exclude_defaults),
            **kwargs
        )
        return self.parse_response(response, Format)

    def create_asset_file(self, asset_id: str, body: FileCreate, exclude_defaults=True, **kwargs) -> Response:
        """
        Create file and associate to asset
        Returns: Response(model=File)
        """
        response = self._post(
            GET_ASSETS_FILES_PATH.format(asset_id),
            json=body.model_dump(exclude_defaults=exclude_defaults),
            **kwargs
        )
        return self.parse_response(response, File)

    def create_asset_filesets(self, asset_id: str, body: FileSetCreate, exclude_defaults=True, **kwargs) -> Response:
        """
        Create file sets and associate it to asset
        Returns: Response(model=FileSet)
        """
        response = self._post(
            GET_ASSETS_FILE_SET_PATH.format(asset_id),
            json=body.model_dump(exclude_defaults=exclude_defaults),
            **kwargs
        )
        return self.parse_response(response, FileSet)

    def get_asset_filesets(self, asset_id: str, **kwargs) -> Response:
        """Get all asset's file sets"""
        resp = self._get(GET_ASSETS_FILE_SET_PATH.format(asset_id), **kwargs)

        return self.parse_response(resp, FileSets)

    def get_asset_formats(self, asset_id: str, **kwargs) -> Response:
        """Get all asset's formats"""
        resp = self._get(GET_ASSETS_FORMATS_PATH.format(asset_id), **kwargs)

        return self.parse_response(resp, Formats)

    def get_asset_format(self, asset_id: str, format_id: str, **kwargs) -> Response:
        """Get asset format"""
        resp = self._get(GET_ASSETS_FORMAT_PATH.format(asset_id, format_id), **kwargs)

        return self.parse_response(resp, Format)

    def get_asset_files(self, asset_id: str, **kwargs) -> Response:
        """Get asset files"""
        resp = self._get(GET_ASSETS_FILES_PATH.format(asset_id), **kwargs)

        return self.parse_response(resp, Files)

    def get_storage(self, storage_id: str, **kwargs):
        """Get storage meta"""
        resp = self._get(GET_STORAGE_PATH.format(storage_id), **kwargs)

        return self.parse_response(resp, Storage)

    def get_storages(self, **kwargs):
        """Get storage meta"""
        resp = self._get(GET_STORAGES_PATH, **kwargs)

        return self.parse_response(resp, Storages)
