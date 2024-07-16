import uuid

import requests_mock

from pythonik.client import PythonikClient
from pythonik.models.files.file import Files, FileSetCreate, FileSets, FileCreate
from pythonik.models.files.format import Formats, Format, FormatCreate
from pythonik.models.files.proxy import Proxies, Proxy
from pythonik.models.files.storage import Storage
from pythonik.specs.files import (
    GET_ASSET_PROXIES_PATH,
    GET_ASSET_PROXY_PATH,
    GET_ASSETS_FILES_PATH,
    GET_ASSETS_FORMAT_PATH,
    GET_ASSETS_FORMATS_PATH,
    GET_ASSETS_FILE_SET_PATH,
    GET_STORAGE_PATH,
    GET_STORAGES_PATH,
    FilesSpec,
)


def test_get_proxy_by_proxy_id():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        proxy_id = str(uuid.uuid4())

        model = Proxy()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(
            GET_ASSET_PROXY_PATH.format(asset_id, proxy_id)
        )

        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_asset_proxy(asset_id, proxy_id)


def test_get_proxies():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = Proxies()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_ASSET_PROXIES_PATH.format(asset_id))

        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_asset_proxies(asset_id)


def test_get_asset_format():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        format_id = str(uuid.uuid4())

        model = Format()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(
            GET_ASSETS_FORMAT_PATH.format(asset_id, format_id)
        )
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_asset_format(asset_id, format_id)


def test_get_asset_formats():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = Formats()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_ASSETS_FORMATS_PATH.format(asset_id))
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        params = {"per_page": 20}
        client.files().get_asset_formats(asset_id, params=params)


def test_create_asset_file():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        name = str(uuid.uuid4())

        model = FileCreate(
            file_set_id=str(uuid.uuid4()),
            format_id=str(uuid.uuid4()),
            storage_id=str(uuid.uuid4()),
            name=name,
            original_name=name,
            size=41
        )
        data = model.model_dump()

        mock_address = FilesSpec.gen_url(GET_ASSETS_FILES_PATH.format(asset_id))
        m.post(mock_address, json=data)

        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().create_asset_file(asset_id, body=model)


def test_create_asset_format():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = FormatCreate(name="ORIGINAL")
        data = model.model_dump()

        mock_address = FilesSpec.gen_url(GET_ASSETS_FORMATS_PATH.format(asset_id))
        m.post(mock_address, json=data)

        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().create_asset_format(asset_id, body=model)


def test_create_asset_fileset():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = FileSetCreate(
            name=str(uuid.uuid4()),
            format_id=str(uuid.uuid4()),
            storage_id=str(uuid.uuid4()),
        )
        data = model.model_dump()

        mock_address = FilesSpec.gen_url(GET_ASSETS_FILE_SET_PATH.format(asset_id))
        m.post(mock_address, json=data)

        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().create_asset_filesets(asset_id, body=model)


def test_get_asset_filesets():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = FileSets()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_ASSETS_FILE_SET_PATH.format(asset_id))
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        params = {"per_page": 20}
        client.files().get_asset_filesets(asset_id, params=params)


def test_get_asset_files():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = Files()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_ASSETS_FILES_PATH.format(asset_id))
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        params = {"per_page": 20}
        client.files().get_asset_files(asset_id, params=params)


def test_get_storage():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        storage_id = str(uuid.uuid4())

        model = Storage()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_STORAGE_PATH.format(storage_id))
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_storage(storage_id)


def test_get_storages():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())

        model = Storage()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_STORAGES_PATH)
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_storages()
