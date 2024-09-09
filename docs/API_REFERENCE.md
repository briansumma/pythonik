# Pythonik SDK API Reference

This document provides detailed documentation for the classes and methods available in the Pythonik SDK.

## Table of Contents

1. [AssetSpec](#assetspec)
   - [get](#get)
   - [create](#create)
   - [create_segment](#create_segment)
   - [update_segment](#update_segment)
   - [partial_update_segment](#partial_update_segment)
2. [CollectionSpec](#collectionspec)
   - [get](#get-1)
   - [create](#create-1)
   - [update](#update)
3. [JobSpec](#jobspec)
   - [create](#create-2)
   - [update](#update-1)
4. [FilesSpec](#filesspec)
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
5. [SearchSpec](#searchspec)
   - [search](#search)

## AssetSpec

`AssetSpec` is a class that provides methods for interacting with assets in the Iconik system.

### get

Retrieves an Iconik asset by its ID.

```python
asset = AssetSpec().get(asset_id="1234567890abcdef")
```

### create

Creates a new Iconik asset.

```python
asset_data = {
    "title": "My New Asset",
    "description": "This is a sample asset",
    "metadata": {
        "custom_field": "Custom value"
    }
}
asset = AssetSpec().create(asset_data)
```

### create_segment

Creates a new segment for an Iconik asset.

```python
segment_data = {
    "title": "Segment 1",
    "in_timecode": "00:00:10:00",
    "out_timecode": "00:00:30:00",
    "metadata": {
        "segment_type": "interview"
    }
}
segment = AssetSpec().create_segment(asset_id="1234567890abcdef", segment_data=segment_data)
```

### update_segment

Updates an existing segment for an Iconik asset.

```python
updated_segment_data = {
    "title": "Updated Segment 1",
    "out_timecode": "00:00:35:00"
}
updated_segment = AssetSpec().update_segment(asset_id="1234567890abcdef", segment_id="seg123456", segment_data=updated_segment_data)
```

### partial_update_segment

Partially updates an existing segment for an Iconik asset.

```python
partial_update_data = {
    "metadata": {
        "segment_type": "b-roll"
    }
}
partially_updated_segment = AssetSpec().partial_update_segment(asset_id="1234567890abcdef", segment_id="seg123456", segment_data=partial_update_data)
```

## CollectionSpec

`CollectionSpec` is a class that provides methods for interacting with collections in the Iconik system.

### get

Retrieves an Iconik collection by its ID.

```python
collection = CollectionSpec().get(collection_id="coll987654")
```

### create

Creates a new Iconik collection.

```python
collection_data = {
    "name": "My New Collection",
    "description": "This is a sample collection",
    "metadata": {
        "project": "Project A"
    }
}
collection = CollectionSpec().create(collection_data)
```

### update

Updates an existing Iconik collection.

```python
update_data = {
    "name": "Updated Collection Name",
    "metadata": {
        "status": "In Progress"
    }
}
updated_collection = CollectionSpec().update(collection_id="coll987654", collection_data=update_data)
```

## JobSpec

`JobSpec` is a class that provides methods for interacting with jobs in the Iconik system.

### create

Creates a new Iconik job.

```python
job_body = {
    "job_type": "TRANSCODE",
    "asset_id": "1234567890abcdef",
    "parameters": {
        "output_format": "MP4",
        "resolution": "1920x1080"
    }
}
job = JobSpec().create(job_body)
```

### update

Updates an existing Iconik job.

```python
job_update = {
    "status": "COMPLETED",
    "progress": 100
}
updated_job = JobSpec().update(job_id="job123456", job_body=job_update)
```

## FilesSpec

`FilesSpec` is a class that provides methods for interacting with files, proxies, formats, and storages in the Iconik system.

### get_asset_proxy

Retrieves a proxy for a specific asset.

```python
proxy = FilesSpec().get_asset_proxy(asset_id="1234567890abcdef", proxy_id="proxy123")
```

### update_asset_proxy

Updates an existing proxy for an asset.

```python
proxy_update = {
    "status": "READY",
    "file_size": 1024000
}
updated_proxy = FilesSpec().update_asset_proxy(asset_id="1234567890abcdef", proxy_id="proxy123", proxy_data=proxy_update)
```

### create_asset_proxy

Creates a new proxy for an asset.

```python
proxy_data = {
    "type": "VIDEO",
    "format": "MP4",
    "resolution": "1280x720"
}
new_proxy = FilesSpec().create_asset_proxy(asset_id="1234567890abcdef", proxy_data=proxy_data)
```

### get_upload_id_for_proxy

Retrieves an upload ID for a proxy, which is required for uploading proxy files.

```python
upload_id = FilesSpec().get_upload_id_for_proxy(asset_id="1234567890abcdef", proxy_id="proxy123")
```

### get_s3_presigned_url

Retrieves a signed part URL for uploading a proxy to S3.

```python
presigned_url = FilesSpec().get_s3_presigned_url(asset_id="1234567890abcdef", proxy_id="proxy123", upload_id="upload456", part_number=1)
```

### get_s3_complete_url

Retrieves the URL to complete an S3 multipart upload.

```python
complete_url = FilesSpec().get_s3_complete_url(asset_id="1234567890abcdef", proxy_id="proxy123", upload_id="upload456")
```

### get_asset_proxies

Retrieves all proxies for a specific asset.

```python
proxies = FilesSpec().get_asset_proxies(asset_id="1234567890abcdef")
```

### create_asset_format

Creates a new format for an asset.

```python
format_data = {
    "name": "High Resolution",
    "file_extension": "mov",
    "mime_type": "video/quicktime"
}
new_format = FilesSpec().create_asset_format(asset_id="1234567890abcdef", format_data=format_data)
```

### create_asset_file

Creates a new file for an asset.

```python
file_data = {
    "filename": "sample_video.mp4",
    "size": 1024000,
    "checksum": "abcdef1234567890"
}
new_file = FilesSpec().create_asset_file(asset_id="1234567890abcdef", file_data=file_data)
```

### create_asset_filesets

Creates new file sets for an asset.

```python
fileset_data = {
    "name": "4K Master",
    "files": ["file_id_1", "file_id_2"]
}
new_filesets = FilesSpec().create_asset_filesets(asset_id="1234567890abcdef", fileset_data=fileset_data)
```

### get_asset_filesets

Retrieves all file sets for a specific asset.

```python
filesets = FilesSpec().get_asset_filesets(asset_id="1234567890abcdef")
```

### get_asset_formats

Retrieves all formats for a specific asset.

```python
formats = FilesSpec().get_asset_formats(asset_id="1234567890abcdef")
```

### get_asset_format

Retrieves a specific format for an asset.

```python
format = FilesSpec().get_asset_format(asset_id="1234567890abcdef", format_id="format789")
```

### get_asset_files

Retrieves all files for a specific asset.

```python
files = FilesSpec().get_asset_files(asset_id="1234567890abcdef")
```

### get_storage

Retrieves metadata for a specific storage.

```python
storage = FilesSpec().get_storage(storage_id="storage123")
```

### get_storages

Retrieves metadata for all storages.

```python
storages = FilesSpec().get_storages()
```

## SearchSpec

`SearchSpec` is a class that provides methods for searching in the Iconik system.

### search

Performs a search in Iconik.

```python
search_body = {
    "query": "sample asset",
    "filters": {
        "asset_type": ["video", "image"],
        "created_date": {
            "from": "2023-01-01",
            "to": "2023-12-31"
        }
    },
    "sort": [{"field": "created_date", "order": "desc"}],
    "limit": 50,
    "offset": 0
}
search_results = SearchSpec().search(search_body)
```

## Conclusion

This API reference provides an overview of the main classes and methods available in the Pythonik SDK. For more detailed information on method parameters and return values, please refer to the inline documentation in the source code.
