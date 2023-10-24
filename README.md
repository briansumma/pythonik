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

## NSA Internal PyPI Gitlab Package - Publishing

CI/CD pipeline will automatically build and add a new version as a PyPI package to the package registry for this project.

To build and publish a new PyPI package to this projects gitab package registry:

1. Create and push a tag on the default branch (main)
   - git tag {tag}
   - git push

## NSA Internal PyPI Gitlab Package - Installing

Installing in another project using Poetry

```bash
poetry source add --priority=supplemental gitlab https://gitlab.com/api/v4/projects/51363622/packages/pypi/simple
# your gitlab user name and access token
# example
# username = <your_personal_access_token_name>
# password = <your_personal_access_token>
# or
# username = <deploy token username>
# password = <deploy token>
# Note: If using a personal access token for authentication it needs scope set to api.
# If using a deploy token set scope to read_package_registry.
poetry config http-basic.gitlab <username> <password>
# install the package
poetry add --source gitlab pythonik
```

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
