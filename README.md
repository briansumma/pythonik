# Pythonik

## Iconik Python SDK

## Description

A python SDK for the Iconik API. Provides convenient methods for interacting with the Iconik API.

## Installation

```bash
pip install pythonik
```

## Usage

```python

# get an asset from iconik

from pythonik.client import PythonikClient

client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=5)

client.assets().get(asset_id)

```

```python

# get metadata from a view

from pythonik.client import PythonikClient

asset_id = '123'
view_id = '456'

client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=5)

client.metadata().get_asset_metadata(asset_id, view_id)

```

## NSA Internal PyPI Gitlab Package

CI/CD pipeline will automatically build and add a new version as a PyPI package to the package registry for this project.

To build and publish a new PyPI package to this projects gitab package registry:

1. Create and push a tag on the default branch (main)
   - git tag {tag}
   - git push

## Support

NSA

## Roadmap

## Contributing

## Authors and acknowledgment

North Shore Automation Developers

- Brant Goddard

## License

Coming Soon

## Project status
