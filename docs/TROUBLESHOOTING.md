# Troubleshooting Guide for Pythonik

This document provides solutions to common issues you might encounter while using the Pythonik SDK.

## Table of Contents

1. [Authentication Issues](#authentication-issues)
2. [Connection Timeouts](#connection-timeouts)
3. [Unexpected Responses](#unexpected-responses)
4. [Rate Limiting](#rate-limiting)
5. [Proxy Upload Issues](#proxy-upload-issues)

## Authentication Issues

If you're experiencing authentication problems:

1. Double-check your `app_id` and `auth_token`.
2. Ensure your authentication token hasn't expired.
3. Verify that your account has the necessary permissions for the operations you're trying to perform.

## Connection Timeouts

If you're encountering connection timeouts:

1. Check your internet connection.
2. Increase the timeout value when initializing the client:

   ```python
   client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=10)
   ```

3. If the issue persists, there might be a problem with the Iconik API. Check their status page or contact their support.

## Unexpected Responses

If you're receiving unexpected responses:

1. Ensure you're using the latest version of Pythonik.
2. Check the Iconik API documentation to verify if there have been any recent changes.
3. Use the `response` attribute of the returned object to inspect the raw API response:

   ```python
   result = client.assets().get(asset_id=asset_id)
   print(result.response.status_code)
   print(result.response.text)
   ```

## Rate Limiting

If you're hitting rate limits:

1. Implement exponential backoff and retry logic in your code.
2. Consider batching requests if you're making many calls in quick succession.
3. Contact Iconik support to discuss increasing your rate limits if necessary.

## Proxy Upload Issues

If you're having trouble with proxy uploads:

1. Ensure you're using the correct storage method (S3 or GCS) for your proxy.
2. Double-check that you have the necessary permissions on the storage bucket.
3. Verify that the file you're trying to upload meets Iconik's requirements (file type, size, etc.).
4. If using multipart uploads, ensure all parts are uploaded successfully before completing the upload.

For more detailed information on using Pythonik, refer to the [README.md](../README.md) file.

If you continue to experience issues after trying these troubleshooting steps, please open an issue on the Pythonik GitHub repository or contact NSA support.
