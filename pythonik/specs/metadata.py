from pythonik.models.base import Response
from pythonik.models.metadata.views import ViewMetadata
from pythonik.models.mutation.metadata.mutate import (
    UpdateMetadata,
    UpdateMetadataResponse,
)
from pythonik.specs.base import Spec

ASSET_METADATA_FROM_VIEW_PATH = "assets/{}/views/{}"
UPDATE_ASSET_METADATA = "assets/{}/views/{}/"


class MetadataSpec(Spec):
    server = "API/metadata/"

    def get_asset_metadata(self, asset_id: str, view_id: str) -> Response:
        """Given an asset id and the asset's view id, fetch metadata from the asset's view"""

        resp = self._get(ASSET_METADATA_FROM_VIEW_PATH.format(asset_id, view_id))

        return self.parse_response(resp, ViewMetadata)

    def update_asset_metadata(
        self, asset_id: str, view_id: str, metadata: UpdateMetadata
    ) -> Response:
        """Given an asset's view id, update metadata in asset's view"""
        resp = self._put(
            UPDATE_ASSET_METADATA.format(asset_id, view_id), json=metadata.model_dump()
        )

        return self.parse_response(resp, UpdateMetadataResponse)
