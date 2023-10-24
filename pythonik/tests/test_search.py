import uuid
import requests_mock
from pythonik.client import PythonikClient

from pythonik.models.metadata.views import ViewMetadata
from pythonik.models.mutation.metadata.mutate import (
    UpdateMetadata,
    UpdateMetadataResponse,
)
from pythonik.models.search.search_body import Criteria, SearchBody
from pythonik.specs.metadata import (
    ASSET_METADATA_FROM_VIEW_PATH,
    UPDATE_ASSET_METADATA,
    MetadataSpec,
)
from pythonik.specs.search import SEARCH_PATH, SearchSpec


def test_search_assets():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())

        # needs model
        params = {"generate_signed_url": "true", "generate_signed_download_url": "true"}

        # search criteria
        search_chriteria = Criteria()
        search_chriteria.doc_types = ["assets"]
        search_chriteria.query = f"id:{asset_id}"
        search_chriteria.filter.operator = "AND"
        # get only active assets
        search_chriteria.filter.terms = [{"name": "status", "value": "ACTIVE"}]
        search_chriteria.sort = [{"name": "date_created", "order": "desc"}]

        body_model = SearchBody()
        body = body_model.model_dump()
        mock_address = SearchSpec.gen_url(SEARCH_PATH)
        m.post(mock_address, json=body)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.search().search(body_model, params=params)
