import json
from pydantic import BaseModel
from urllib3.util import Retry
from typing import Type, Optional, Union, List
from urllib.parse import urljoin
from requests import Session, Request, Response, PreparedRequest
from requests.adapters import HTTPAdapter

from pythonik.specs.assets import AssetSpec
from pythonik.specs.files import FilesSpec


# Iconik APIs
JOBS_API = "API/jobs/v1/"
FILES_API = "API/files/v1/"
USERS_API = "API/users/v1/"
# COLLECTION_API = f"{ASSETS_API}collections/"


class PythonikClient:
    """
    Iconik Client
    """

    def __init__(self, app_id: str, auth_token: str, timeout: int):
        # self.assets_url = urljoin(self.base_url, ASSETS_API)
        # self.files_url = urljoin(self.base_url, FILES_API)
        # self.jobs_url = urljoin(self.base_url, JOBS_API)
        # self.users_url = urljoin(self.base_url, USERS_API)
        # self.collections_url = urljoin(self.base_url, COLLECTION_API)

        self.session = Session()
        retry_strategy = Retry(
            total=4,  # Maximum number of retries
            backoff_factor=3,
        )
        http_adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", http_adapter)
        self.session.mount("https://", http_adapter)
        self.session.headers = {
            "App-ID": app_id,
            "Auth-Token": auth_token,
            "Accept": "application/json",
        }
        self.timeout = timeout

    def assets(self):
        return AssetSpec(self.session, self.timeout)

    def files(self):
        return FilesSpec(self.session, self.timeout)
