Here's your document with Python code blocks correctly formatted and a few adjustments for clarity:

---

# Advanced Usage of Pythonik SDK

This document covers advanced usage scenarios and features of the Pythonik SDK. These techniques are designed for users who are already familiar with the basic operations and want to leverage more complex functionalities.

## Table of Contents

1. [Custom Error Handling](#custom-error-handling)
2. [Batch Operations](#batch-operations)
3. [Pagination Handling](#pagination-handling)
4. [Working with Proxies](#working-with-proxies)
5. [Advanced Search Queries](#advanced-search-queries)
6. [Metadata Manipulation](#metadata-manipulation)
7. [Job Management](#job-management)

## Custom Error Handling

Pythonik provides detailed error information. You can implement custom error handling to manage specific error scenarios:

```python
from pythonik.client import PythonikClient
from pythonik.exceptions import PythonikException

client = PythonikClient(app_id=app_id, auth_token=auth_token)

try:
    asset = client.assets().get(asset_id="non_existent_id")
except PythonikException as e:
    if e.response.status_code == 404:
        print(f"Asset not found: {e}")
    else:
        print(f"An error occurred: {e}")
```

## Batch Operations

For efficiency, you can perform batch operations on multiple assets:

```python
asset_ids = ["id1", "id2", "id3"]
results = []

for asset_id in asset_ids:
    result = client.assets().get(asset_id=asset_id)
    results.append(result)

# Process results
```

## Pagination Handling

When dealing with large datasets, use pagination to efficiently retrieve data:

```python
from pythonik.models.search.search_body import SearchBody

search_body = SearchBody(doc_types=["assets"], query="*")
page = 1
per_page = 100

while True:
    results = client.search().search(search_body, params={"page": page, "per_page": per_page})

    for asset in results.data.objects:
        # Process each asset
        print(asset.title)

    if not results.data.next_url:
        break

    page += 1
```

## Working with Proxies

The Pythonik SDK supports creating and managing proxy placeholders. This is useful when you want to create an asset with a proxy before the actual media file is available:

```python
# Create a proxy placeholder
proxy = client.assets().create_proxy(asset_id="your_asset_id", proxy_id="your_proxy_id")

# Get the upload ID for the proxy
upload_id = client.files().get_upload_id_for_proxy(asset_id="your_asset_id", proxy_id="your_proxy_id")
```

Handling proxy uploads, especially for large files:

```python
asset_id = "your_asset_id"
proxy_id = "your_proxy_id"

# Get upload ID
upload_id = client.files().get_upload_id_for_proxy(asset_id, proxy_id)

# For S3 uploads
for part_number in range(1, total_parts + 1):
    presigned_url = client.files().get_s3_presigned_url(asset_id, proxy_id, upload_id, part_number)
    # Use presigned_url to upload the part

# Complete the upload
complete_url = client.files().get_s3_complete_url(asset_id, proxy_id, upload_id)
# Use complete_url to finalize the upload
```

## Advanced Search Queries

Construct complex search queries:

```python
from pythonik.models.search.search_body import SearchBody, Filter, Term, SortItem

search_body = SearchBody(
    doc_types=["assets"],
    query="project:myproject",
    filter=Filter(
        operator="AND",
        terms=[
            Term(name="status", value="active"),
            Term(name="date_created", range={"min": "2023-01-01", "max": "2023-12-31"})
        ]
    ),
    sort=[SortItem(name="date_created", order="desc")]
)

results = client.search().search(search_body)
```

## Metadata Manipulation

Update metadata for an asset:

```python
from pythonik.models.mutation.metadata.mutate import UpdateMetadata, MetadataValues, FieldValues, FieldValue

metadata_update = UpdateMetadata(
    metadata_values=MetadataValues({
        "custom_field": FieldValues(
            field_values=[FieldValue(value="new_value")]
        )
    })
)

client.metadata().update_asset_metadata(asset_id, view_id, metadata_update)
```

## Job Management

Create and manage custom jobs:

```python
from pythonik.models.jobs.job_body import JobBody, JobStatus, JobTypes

job = JobBody(
    title="Custom Processing Job",
    type=JobTypes.CUSTOM,
    status=JobStatus.STARTED,
    job_context={"asset_id": "your_asset_id"}
)

created_job = client.jobs().create(job)

# Update job status
updated_job = client.jobs().update(created_job.data.id, JobBody(status=JobStatus.FINISHED))
```

These advanced usage examples demonstrate some of the more complex operations you can perform with the Pythonik SDK. Always refer to the API documentation for the most up-to-date information on available methods and their parameters.
