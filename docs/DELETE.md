# Deleting Assets in Pythonik

This guide explains how to delete assets using the Pythonik client library.

## Prerequisites

- A valid Iconik App ID and Auth Token
- The `pythonik` library installed
- Appropriate permissions (`can_delete_assets` role)

## Basic Usage

To delete a single asset, you'll need the asset's ID. Here's a basic example:

```python
from pythonik.client import PythonikClient

# Initialize the client
client = PythonikClient(
    app_id="your_app_id",
    auth_token="your_auth_token"
)

# Delete an asset
response = client.assets.delete(asset_id="your_asset_id")

# Check if deletion was successful
if response.status_code == 204:
    print("Asset deleted successfully")
```

## Error Handling

The delete operation may raise several types of errors:

- `400`: Bad request - The request was malformed
- `401`: Invalid token - Authentication failed
- `403`: Forbidden - User lacks the required permissions
- `404`: Asset not found - The specified asset ID doesn't exist

Here's an example with error handling:

```python
from pythonik.client import PythonikClient
from pythonik.exceptions import (
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError
)

client = PythonikClient(app_id="your_app_id", auth_token="your_auth_token")

try:
    response = client.assets.delete(asset_id="your_asset_id")
    print("Asset deleted successfully")
except BadRequestError:
    print("Invalid request format")
except UnauthorizedError:
    print("Invalid authentication credentials")
except ForbiddenError:
    print("Insufficient permissions")
except NotFoundError:
    print("Asset not found")
```

## Related Operations

- For bulk deletion of assets, see `client.assets.bulk_delete()`
- For permanent deletion of assets in the delete queue, see `client.assets.permanently_delete()`

## Best Practices

1. Always verify that you have the correct asset ID before deletion
2. Implement proper error handling
3. Consider using bulk delete operations when removing multiple assets
4. Keep track of deleted assets for audit purposes
