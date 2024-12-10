# Metadata Operations

This document describes the metadata operations available in the Pythonik SDK.

## Direct Metadata Updates

The `put_metadata_direct` method allows for fast, direct updates to metadata without requiring a view. This method is designed for admin-level operations where performance is critical.

### Example Usage

```python
from pythonik.client import PythonikClient
from pythonik.models.mutation.metadata.mutate import UpdateMetadata

# Initialize client
client = PythonikClient(app_id="your_app_id", auth_token="your_admin_token")

# Create metadata update
metadata_values = {
    "metadata_values": {
        "custom_field": {
            "field_values": [{"value": "new_value"}]
        }
    }
}
metadata = UpdateMetadata.model_validate(metadata_values)

# For empty metadata updates:
# metadata = UpdateMetadata.model_validate({"metadata_values": {}})

# Update metadata directly
response = client.metadata().put_metadata_direct(
    object_type="assets",
    object_id="your_asset_id",
    metadata=metadata
)

if response.response.ok:
    print(f"Metadata updated successfully: {response.data.metadata_values}")
else:
    print(f"Error updating metadata: {response.response.status_code}")
```

### Important Notes

1. **Admin Access Required**: This method requires admin-level access token.
2. **Performance vs Safety**: While this method is faster than view-based updates, it bypasses standard validation checks.
3. **Data Integrity**: The method will write to the database even if the `object_id` doesn't exist, so use with caution.
4. **Best Practices**:
   - Always verify the object exists before updating its metadata
   - Use standard view-based updates for non-admin operations
   - Monitor responses for any errors
   - Consider implementing additional validation in your application if needed

### Response Structure

A successful response will include:
- `date_created`: Creation timestamp
- `date_modified`: Last modification timestamp
- `metadata_values`: Updated metadata values
- `object_id`: Target object ID
- `object_type`: Type of object
- `version_id`: Version identifier

### Error Responses

- `400`: Bad request (invalid metadata format)
- `401`: Invalid authentication token
- `404`: Object type not found
  