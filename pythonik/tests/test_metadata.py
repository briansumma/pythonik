import uuid
import requests_mock
from pythonik.client import PythonikClient

from pythonik.models.metadata.views import ViewMetadata
from pythonik.models.mutation.metadata.mutate import (
    UpdateMetadata,
    UpdateMetadataResponse,
)
from pythonik.specs.metadata import (
    ASSET_METADATA_FROM_VIEW_PATH,
    UPDATE_ASSET_METADATA,
    MetadataSpec,
)


def test_get_asset_metadata():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())

        model = ViewMetadata()
        data = model.model_dump()
        mock_address = MetadataSpec.gen_url(
            ASSET_METADATA_FROM_VIEW_PATH.format(asset_id, view_id)
        )
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.metadata().get_asset_metadata(asset_id, view_id)


def test_update_asset_metadata():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())
        payload = {"metadata_values": {"field1": {"field_values": [{"value": "123"}]}}}

        mutate_model = UpdateMetadata.model_validate(payload)
        response_model = UpdateMetadataResponse(
            metadata_values=mutate_model.metadata_values.model_dump()
        )

        data = mutate_model.model_dump()
        mock_address = MetadataSpec.gen_url(
            UPDATE_ASSET_METADATA.format(asset_id, view_id)
        )
        m.put(mock_address, json=response_model.model_dump())
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.metadata().update_asset_metadata(asset_id, view_id, mutate_model)
