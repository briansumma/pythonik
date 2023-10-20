from pythonik.client import PythonikClient
import requests_mock
import uuid

from pythonik.models.assets.assets import Asset
from pythonik.specs.assets import GET_URL, AssetSpec
from pythonik.specs.base import Spec


def test_get_asset():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = Asset()
        data = model.model_dump()
        mock_address = AssetSpec.gen_url(GET_URL.format(asset_id))

        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)

        client.assets().get(asset_id=asset_id)
