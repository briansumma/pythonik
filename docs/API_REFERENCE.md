# Pythonik API Reference

This document provides detailed documentation for the classes and methods
available Pythonik.

## Pythonik Response

Every request returns a `PythonikResponse`, which is a Pydantic model with 2 fields:

- `response` - underlying requests response object
- `data` - if the request was `OK` and has an associated model, the response
JSON is converted to that Pydantic model.

```python
from pythonik.client import PythonikClient

client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=5)
request = client.assets().get(asset_id)

# access response data via underlying requests response
response_json = request.response.json()
print(response_json["id"])

# access response data via Pydantic model
asset = request.data
print(asset.id)
```

## Table of Contents

1. [Assets](#assets)
   - [get](#get)
   - [create](#create)
   - [create_segment](#create_segment)
   - [update_segment](#update_segment)
   - [partial_update_segment](#partial_update_segment)
2. [Jobs](#jobs)
   - [create](#create-2)
   - [update](#update-1)
3. [Files](#files)
   - [get_asset_proxy](#get_asset_proxy)
   - [update_asset_proxy](#update_asset_proxy)
   - [create_asset_proxy](#create_asset_proxy)
   - [get_upload_id_for_proxy](#get_upload_id_for_proxy)
   - [get_s3_presigned_url](#get_s3_presigned_url)
   - [get_s3_complete_url](#get_s3_complete_url)
   - [get_asset_proxies](#get_asset_proxies)
   - [create_asset_format](#create_asset_format)
   - [create_asset_file](#create_asset_file)
   - [create_asset_filesets](#create_asset_filesets)
   - [get_asset_filesets](#get_asset_filesets)
   - [get_asset_formats](#get_asset_formats)
   - [get_asset_format](#get_asset_format)
   - [get_asset_files](#get_asset_files)
   - [get_storage](#get_storage)
   - [get_storages](#get_storages)
4. [Search](#search)
   - [search](#search)
5. [Metadata](#metadata)
   - [get_asset_metadata](#get_asset_metadata)
   - [update_asset_metadata](#update_asset_metadata)
6. [Version Management](#version-management)
   - [Update a Version](#update-a-version)
   - [Promote a Version](#promote-a-version)
   - [Delete Versions](#delete-versions)

## Assets

`AssetSpec` provides methods for interacting with Iconik assets.

### get

Retrieves an Iconik asset by its ID.

```python
asset = client.assets().get(asset_id="1234567890abcdef")
```

### create

Creates a new Iconik asset.

```python
from pythonik.models.assets.assets import AssetCreate

asset_data = {
    "name": "My New Asset",
    "metadata": {
        "custom_field": "Custom value"
    }
}
body = AssetCreate(**asset_data)
asset = client.assets().create(body=body)
```

### create_segment

Creates a new segment for an Iconik asset.

```python
from pythonik.models.assets.segments import SegmentBody

segment_data = {
    "segment_text": "Segment 1",
    "metadata": {
        "segment_type": "interview"
    }
}
body = SegmentBody(**segment_data)
segment = client.assets().create_segment(asset_id="1234567890abcdef", body=body)
```

### update_segment

Update a segment on an asset, such as a comment, using `PUT`.

```python
from pythonik.models.assets.segments import SegmentBody

body = SegmentBody(segment_text="Update Segment 1")
updated_segment = client.assets().update_segment(asset_id="1234567890abcdef", segment_id="seg123456", body=body)
```

### partial_update_segment

Partially update a segment on an asset, such as a comment, using `PATCH`.

```python
from pythonik.models.assets.segments import SegmentBody

partial_update_data = {
    "metadata": {
        "segment_type": "b-roll"
    }
}
body = SegmentBody(**partial_update_data)
partially_updated_segment = client.assets().partial_update_segment(asset_id="1234567890abcdef", segment_id="seg123456", body=body)
```

## Jobs

`JobSpec` provides methods for interacting with jobs in Iconik.

### create

Creates a new Iconik job.

```python
from pythonik.models.jobs.job_body import JobBody, JobTypes, JobStatus

job_body = JobBody(title="Transfer Job", type=JobTypes.TRANSFER, metadata={"client": "Pythonik"}, status=JobStatus.STARTED)

job = client.jobs().create(job_body)
```

### update

Updates an existing Iconik job.

```python
from pythonik.models.jobs.job_body import JobBody, JobStatus

job_update = JobBody(status=JobStatus.FINISHED, progress=100)
updated_job = client.jobs().update(job_id="job123456", body=job_update)
```

## Files

`FilesSpec` provides methods for interacting with files, proxies, formats, and storages in Iconik.

### get_asset_proxy

Retrieves a proxy for a specific asset.

```python
proxy = client.files().get_asset_proxy(asset_id="1234567890abcdef", proxy_id="proxy123")
```

### update_asset_proxy

Updates an existing proxy for an asset.

```python
from pythonik.models.files.proxy import Proxy

proxy_update = Proxy(status="CLOSED")
updated_proxy = client.files().update_asset_proxy(asset_id="1234567890abcdef", proxy_id="proxy123", body=proxy_update)
```

### create_asset_proxy

Creates a new proxy for an asset.

```python
from pythonik.models.files.proxy import Proxy

proxy_data = Proxy(
    resolution={"height": 1920, "width": 1080},
    size=1024000,
    status="OPEN",
    name="3235603-uhd_3840_2160.mp4",
    storage_id="eef9280a-0057-4198-8f4b-06705a54d142",
    storage_method="S3",
    codec="av01",
    filename="3235603-uhd_3840_2160.mp4"
)
new_proxy = client.files().create_asset_proxy(asset_id="1234567890abcdef", body=proxy_data)
```

### get_upload_id_for_proxy

Retrieves an upload ID for a proxy, which is required for uploading proxy files.

```python
response = client.files().get_upload_id_for_proxy(asset_id="1234567890abcdef", proxy_id="proxy123")
upload_id = response.data
```

### get_s3_presigned_url

Retrieves a signed part URL for uploading a proxy to S3.
Iconik (and thus Pythonik) uses multipart uploads when uploading to S3.
If uploading a split file, you’ll need a pre-signed URL and upload for each part.

```python
presigned_url = client.files().get_s3_presigned_url(asset_id="1234567890abcdef", proxy_id="proxy123", upload_id="upload456", part_number=1)
```

### get_s3_complete_url

Retrieves the URL to complete an S3 multipart upload.

```python
complete_url = client.files().get_s3_complete_url(asset_id="1234567890abcdef", proxy_id="proxy123", upload_id="upload456")
```

### get_asset_proxies

Retrieves all proxies for a specific asset.

```python
proxies = client.files().get_asset_proxies(asset_id="1234567890abcdef")
```

### create_asset_format

Creates a new format for an asset.

```python
from pythonik.models.files.format import FormatCreate

format_data = FormatCreate(
    name="High Resolution",
    is_online=True,
    storage_methods=["FILE"]
)
new_format =client.files().create_asset_format(asset_id="1234567890abcdef", body=format_data)
```

### create_asset_file

Creates a new file for an asset.

```python
from pythonik.models.files.file import FileCreate

file_data = FileCreate(
    size=102004,
    name="odor amet",
    original_name="odor amet",
    format_id="c41b5c9a-05f9-4ca5-ac50-74a125f5aeac",
    storage_id="2c5ac73d-0860-42b9-91f3-44a361441143",
    file_set_id="c41b5c9a-05f9-4ca5-ac50-74a125f5aeac",
)
new_file = client.files().create_asset_file(asset_id="1234567890abcdef", body=file_data)
```

### create_asset_filesets

Creates new file sets for an asset.

```python
from pythonik.models.files.file import FileSetCreate

fileset_data = FileSetCreate(
    name="4K Master",
    format_id="c41b5c9a-05f9-4ca5-ac50-74a125f5aeac",
    storage_id="2c5ac73d-0860-42b9-91f3-44a361441143",
)
new_filesets =client.files().create_asset_filesets(asset_id="1234567890abcdef", body=fileset_data)
```

### get_asset_filesets

Retrieves all file sets for a specific asset.

```python
filesets = client.files().get_asset_filesets(asset_id="1234567890abcdef")
```

### get_asset_formats

Retrieves all formats for a specific asset.

```python
formats = client.files().get_asset_formats(asset_id="1234567890abcdef")
```

### get_asset_format

Retrieves a specific format for an asset.

```python
asset_format = client.files().get_asset_format(asset_id="1234567890abcdef", format_id="format789")
```

### get_asset_files

Retrieves all files for a specific asset.

```python
files = client.files().get_asset_files(asset_id="1234567890abcdef")
```

### get_storage

Retrieves metadata for a specific storage.

```python
storage = client.files().get_storage(storage_id="storage123")
```

### get_storages

Retrieves metadata for all storages.

```python
storages = client.files().get_storages()
```

## Search

`SearchSpec` provides methods to search Iconik.

### search

Performs a search in Iconik.

```python
from pythonik.models.search.search_body import SearchBody

# In this example, we're searching for assets on a specific storage, has
# has the corresponding original_name and path
search_body = {
    "operator": "AND",
    "doc_types": ["assets"],
        "terms": [
            {
                "name": "files.storage_id",
                "value_in": [
                    "51cd6a7e-8f3d-4aaf-9db5-ce167b3d1c43"
                ]
            },
            {
                "name": "files.original_name",
                "value_in": [
                    "Lorem_ipsum_odor_amet.png"
                ]
            },
            {
                "name": "files.directory_path",
                "value_in": [
                    "_consectetuer/adipiscing/elit"
                ]
            }
        ]
}
body = SearchBody(**search_body)
search_results = client.search().search(search_body)
```

## Metadata
`MetadataSpec` provides methods for interacting with asset metadata in Iconik.

### get_asset_metadata

Fetches metadata from the asset's view.

```python
metadata = client.metadata().get_asset_metadata(asset_id="2c5ac73d-0860-42b9-91f3-44a361441143", view_id="51099c0f-9586-416e-ae47-e653fbc9a71f")
```

### update_asset_metadata

Update metadata in asset's view.

```python
from pythonik.models.mutation.metadata.mutate import UpdateMetadata

body = UpdateMetadata(metadata_values=[])
metadata = client.metadata().update_asset_metadata(
    asset_id="2c5ac73d-0860-42b9-91f3-44a361441143",
    view_id="51099c0f-9586-416e-ae47-e653fbc9a71f", metadata=body)
```

## Version Management

The Pythonik client provides several endpoints for managing asset versions:

### Update a Version

You can update an asset version using either a full update (PUT) or partial update (PATCH):

```python
from pythonik.client import PythonikClient
from pythonik.models.assets.versions import AssetVersion
from pythonik.models.base import Status

# Initialize client
client = PythonikClient(app_id="your_app_id", auth_token="your_auth_token")

# Create version data
version_data = AssetVersion(
    analyze_status="N/A",
    archive_status="NOT_ARCHIVED",
    created_by_user="user123",
    face_recognition_status="N/A",
    has_unconfirmed_persons=False,
    id="version_id",
    is_online=True,
    person_ids=[],
    status=Status.IN_PROGRESS,
    transcribe_status="N/A"
)

# Full update - replaces all fields
response = client.assets().update_version(
    asset_id="asset123",
    version_id="version456",
    body=version_data
)
updated_version = response.data

# Partial update - only updates specified fields
partial_version = AssetVersion(
    status=Status.ACTIVE,
    is_online=True
)
response = client.assets().partial_update_version(
    asset_id="asset123",
    version_id="version456",
    body=partial_version
)
updated_version = response.data
```

### Promote a Version

You can promote a specific version to be the latest version of an asset:

```python
client.assets().promote_version(
    asset_id="asset123",
    version_id="version456"
)
```

### Delete Versions

You have several options for deleting versions:

```python
# Delete a specific version
client.assets().delete_version(
    asset_id="asset123",
    version_id="version456"
)

# Hard delete a version (completely remove it)
client.assets().delete_version(
    asset_id="asset123",
    version_id="version456",
    hard_delete=True
)

# Delete all versions except the latest one
client.assets().delete_old_versions(
    asset_id="asset123"
)
```

### Required Permissions

- `can_write_versions`: Required for update and promote operations
- `can_delete_versions`: Required for delete operations

### Error Handling

All version management endpoints may raise the following errors:
- 400 Bad Request: Invalid request data
- 401 Unauthorized: Invalid authentication token
- 403 Forbidden: Missing required permissions
- 404 Not Found: Asset or version not found
