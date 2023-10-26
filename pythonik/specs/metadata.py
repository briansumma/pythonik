from loguru import logger
from pydantic import BaseModel
from pythonik.models.base import Response
from pythonik.models.metadata.views import MetadataValues, ViewMetadata
from pythonik.models.mutation.metadata.mutate import (
    UpdateMetadata,
    UpdateMetadataResponse,
)
from pythonik.specs.base import Spec

ASSET_METADATA_FROM_VIEW_PATH = "assets/{}/views/{}"
UPDATE_ASSET_METADATA = "assets/{}/views/{}/"


class MetadataSpec(Spec):
    server = "API/metadata/"

    def get_asset_metadata(
        self, asset_id: str, view_id: str, intercept_404: MetadataValues = False
    ) -> Response:
        """Given an asset id and the asset's view id, fetch metadata from the asset's view

        intercept_404:
            Iconik returns a 404 when a view has no metadata, intercept_404 will intercept that error
            and return a the MetadataValues model provided with the MetadataValues instance provided,

            you can no longer call response.raise_for_status, so be careful using this
            call raise_for_status_404 if you still want to raise status on this error
        """

        resp = self._get(ASSET_METADATA_FROM_VIEW_PATH.format(asset_id, view_id))

        if intercept_404 and resp.status_code == 404:
            parsed_response = self.parse_response(resp, ViewMetadata)
            parsed_response.data = intercept_404
            parsed_response.response.raise_for_status_404 = (
                parsed_response.response.raise_for_status
            )

            parsed_response.response.raise_for_status = lambda: logger.warning(
                "raise for status disabled due to intercept_404, please call raise_for"
                " status_anyway if you want really raise status"
            )
            return parsed_response

        return self.parse_response(resp, ViewMetadata)

    def update_asset_metadata(
        self, asset_id: str, view_id: str, metadata: UpdateMetadata
    ) -> Response:
        """Given an asset's view id, update metadata in asset's view"""
        resp = self._put(
            UPDATE_ASSET_METADATA.format(asset_id, view_id), json=metadata.model_dump()
        )

        return self.parse_response(resp, UpdateMetadataResponse)
