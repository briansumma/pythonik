# Changelog

## 2025-01-05 "Asset Management" - version 1.6.0

### Added
- Add single asset deletion endpoint:
  - New `delete()` method in `AssetSpec` class
  - Support for DELETE /v1/assets/{asset_id}/ endpoint
  - Role-based access control (requires can_delete_assets)
- Add test coverage for asset deletion operations

### Technical Details
This update adds support for deleting individual assets via the Iconik API. The implementation follows REST best practices with proper status code handling and role-based access control. This complements the existing bulk deletion functionality.

## 2024-12-24 "Alternative Environments" - version 1.5.0

### Added
- Add configurable base URL support:
  - New `base_url` parameter in `PythonikClient` constructor
  - Support for AWS Iconik deployments
  - Support for custom Iconik deployments
- Propagate base URL through all spec classes
- Add documentation for connecting to different Iconik environments

### Technical Details
This update enables connecting to different Iconik environments by making the base URL configurable. The implementation maintains consistent client behavior across all API operations while allowing flexibility in the target environment. This is particularly useful for AWS Iconik deployments.

## 2024-12-20 "View Management" - version 1.4.0

### Added
- Add comprehensive view management functionality:
  - `create_view()` for creating new metadata views
  - `get_views()` for listing all views
  - `update_view()` for partial view updates
  - `replace_view()` for full view replacements
  - `delete_view()` for removing views
- Add view-related models:
  - `ViewResponse` and `ViewListResponse` for API responses
  - `ViewField` and `ViewOption` for view configuration
  - `CreateViewRequest` and `UpdateViewRequest` for mutations
- Add comprehensive test coverage for all view operations

### Technical Details
This update introduces complete metadata view management capabilities, allowing programmatic control over view creation, modification, and deletion. The implementation supports both Pydantic models and raw dictionaries as inputs, maintaining consistency with existing API patterns. 

## 2024-12-12 "Standardize" - version 1.3.0

### Changed
- Refactor specs to improve type hints and standardize method signatures
- Add `Union[Model, Dict[str, Any]]` type hints to allow both Pydantic models and raw dicts
- Introduce `_prepare_model_data` helper method to standardize model/dict handling
- Improve docstrings with consistent Args/Returns sections
- Add `**kwargs` propagation to all API methods
- Make `exclude_defaults` parameter consistently typed as `bool`
- Standardize error handling and response parsing

### Technical Details
This update focuses on refactoring the codebase to enhance type safety and consistency across method signatures, improving both maintainability and readability. The changes provide greater flexibility by allowing developers to either pre-instantiate Pydantic models or pass raw dictionaries directly to API methods, streamlining integration patterns based on their specific needs.

## 2024-12-10 "Metadata Mastery" - version 1.2.0

### Added
- Add `put_metadata_direct()` method for fast, admin-level metadata updates
- Add comprehensive test suite for metadata direct updates including error cases (400, 401, 403, 404)
- Add documentation for direct metadata operations in `METADATA.md`

### Changed
- Improved docstring for `put_metadata_direct()` to clarify admin-only access and error cases

### Technical Details
Introduced a new admin-level API endpoint for direct metadata updates that bypasses view validation for improved performance. This method should be used with caution as it can modify metadata even if the target object doesn't exist. 

## 2024-12-05 "Content Contentment" - version 1.1.0

### Added
- Add `add_content()` method to collections API for adding assets to collections
- Add `AddContentResponse` model for handling collection content addition responses
- Add tests for collection content addition functionality

### Changed
- Update collection content handling to use proper object type enums

## 2024-11-25 "Exclusion Delusion" - version 1.0.2

### Fixed
- Remove default values from FileCreate model to prevent serialization issues with `model_dump(exclude_defaults=True)`
- Fields `type` and `status` are now required parameters without defaults
- Updated tests to explicitly set these required fields

### Technical Details
Worked around a Pydantic behavior where fields with default values would be excluded from serialization when using `model_dump(exclude_defaults=True)`, even when explicitly set.

## 2024-11-15 "Deprecation Emancipation" - version 1.0.1

### Changed
- Deprecated `get_asset_file_sets()` in favor of `get_asset_file_set_files()`
- Renamed `GET_ASSETS_FILE_SET_PATH` to `GET_ASSETS_FILE_SETS_PATH` for better URL path consistency
- Updated related test cases to match new method names

Note: Previous functionality remains available but will display deprecation warnings

## 2024-11-15 "filesets, more like files am i right? No? cool... cool... " - version 1.0.0

### Changed
- Renamed `GET_ASSETS_FILE_SET_PATH` to `GET_ASSETS_FILE_SETS_PATH` for better URL path consistency
- Renamed `get_asset_file_sets()` method to `get_asset_file_set_files()` to better reflect its purpose
- BACKWARDS INCOMPATIBLE CHANGE: `get_asset_file_sets()` is removed, use `get_asset_file_set_files()` instead
- Simplified docstring for file set retrieval endpoint
- Updated related test cases to match new method names

## 2024-11-14 "You want some, you lose some" - version 0.9.0

### Added
- Add collections API endpoints to asset spec
- Add bulk & permanent delete operations
- Add collection endpoints and models

### Fixed
- Fix incorrect path name for object metadata view mutations 
- Fix metadata field type to support multiple formats (changed to Any type)

### Changed
- Update metadata field types to be more flexible, supporting boolean, integer, and list values

## 2024-11-11 "Accidents Happen" - version 0.8.0

### Changed
- No substantial changes, just a version bump

## 2024-11-08 "Croissant" - version 0.7.0

### Added
- Add asset version creation endpoints:
  - Create new versions of existing assets (/v1/assets/{asset_id}/versions/)
  - Create versions from other assets (/v1/assets/{asset_id}/versions/from/assets/{source_asset_id}/)
- Add comprehensive version models:
  - `AssetVersionCreate` for basic version creation
  - `AssetVersionFromAssetCreate` for cross-asset version creation
  - `AssetVersionResponse` for version creation responses
- Add support for version creation with:
  - Metadata copying
  - Segment copying with type filtering
  - Source version specification
- Add proper handling of 200+ status codes for async version operations

### Changed
- Update AssetSpec to include version-related endpoints and models
- Improve type hints and documentation for version creation methods

## 2024-11-07 "rm -rf" - version 0.6.3

### Added
- Add DELETE endpoint for asset file sets (/v1/assets/{asset_id}/file_sets/{file_set_id}/)
- Add delete_asset_file_set method with dual response handling:
  - 200: Returns FileSet model when file set is marked as deleted
  - 204: Returns empty response when immediate deletion occurs
  - Includes status code conditional logic and optional keep_source parameter support

### Changed
- Fix file path variable names and add tests

## 2024-11-06 "No Time Like the Prune-sent" - version 0.6.2

### Added
- Add DELETE endpoint for asset file entries (/v1/assets/{asset_id}/files/{file_id}/)

### Changed
- Improved code examples in README.md

## 2024-11-05 "PyPi Public Release" - version 0.6.1

### Changed
- Updated package distribution name to `nsa-pythonik` for PyPI publishing
- Updated installation instructions in README.md
- Note: Internal imports remain unchanged, still using `from pythonik import ...`

## 2024-11-05 "Public Metamorphosis" - version 0.6.0

### Added

- Add ability to update sub-object metadata for segments (Brant Goddard)

## 2024-09-09

- Merge branch 'feature/proxy-placeholder-workflow' into 'main' (Brant Goddard)

## 2024-09-08

- Add additional proxy endpoints (Prince Duepa)

## 2024-09-02

- Add ability to create asset proxy (Prince Duepa)

## 2024-08-19

- Merge branch 'feature/asset-spec-updates' into 'main' (Brant Goddard)

## 2024-08-19

- Fix date serializer (Giovann Wah)

## 2024-08-19

- Update assets create model to allow a placeholder to be created with only a title (Giovann Wah)

## 2024-07-26

- Merge branch 'bugfix/correct-fileset-url' into 'main' (Brandon Dedolph)

## 2024-07-26

- Fix file set url (Prince Duepa)

## 2024-07-16

- Merge branch 'feature/placeholder-asset-workflow' into 'main' (Brandon Dedolph)

## 2024-07-16

- Add endpoints to facilitate placeholder asset workflow (Prince Duepa)

## 2024-06-18

- Merge branch 'AKMV3-2301-pythonik-update-marker' into 'main' (Brant Goddard)

## 2024-06-18

- bugfix: missing segment id, pushing (brant)

## 2024-06-18

- add create, update, partial update to segments (brant)

## 2023-11-29

- add storages (brant)

## 2023-11-28

- fix bug, add get proxies instead (brant)

## 2023-11-28

- attempt to add get proxy by asset id only (brant)

## 2023-11-23

- fix typo (brant)

## 2023-11-23

- add getting files add test for getting files (brant)

## 2023-10-27

- bugfix, updating jobs to use patch instead of put (brant)

## 2023-10-27

- modify intercept 404 to use ViewMetadataModel (brant)

## 2023-10-26

- add intercept 404 (brant)

## 2023-10-26

- fix minor typo (brant)

## 2023-10-26

- fix search models (brant)

## 2023-10-25

- add optional metadata response (brant)

## 2023-10-25

- fix search spec server add exclude defaults add json body (brant)

## 2023-10-25

- change to response.ok instead of 200 check (brant)

## 2023-10-25

- add exclude defaults to jobs (brant)

## 2023-10-25

- removed id from job body (brant)

## 2023-10-25

- fix jobs missing job id fix jobs needing to be a put (brant)

## 2023-10-25

- add jobs create and update (brant)

## 2023-10-25

- update search response model to be more accurrate (brant)

## 2023-10-25

- fix broken metadata values (brant)

## 2023-10-25

- updating view models to be more accurate (brant)

## 2023-10-25

- removed metadata model and removed metadatum model (brant)

## 2023-10-25

- fix format defaults (brant)

## 2023-10-25

- add format model change old format model to formats (brant)

## 2023-10-25

- add get asset format fix bug wrong asset format path (brant)

## 2023-10-24

- readme changes (brant)

## 2023-10-24

- readme changes (brant)

## 2023-10-24

- pipeline changes (brant)

## 2023-10-24

- adding release (brant)

## 2023-10-24

- for now changing version to 0.0.0 (brant)

## 2023-10-24

- more gitlab changes (brant)

## 2023-10-24

- move build command to build stage (brant)

## 2023-10-24

- attempt to get package into this projects packages (brant)

## 2023-10-24

- pipeline changes (brant)

## 2023-10-24

- ci/cd change (brant)

## 2023-10-24

- testing ci/cd builds (brant)

## 2023-10-24

- add cleanup add search add readme changes (brant)

## 2023-10-23

- add metadata spec add put method add update metadata add get asset metadata view add more tests (brant)

## 2023-10-23

- add getting asset formats (brant)

## 2023-10-20

- clean up tests (brant)

## 2023-10-20

- add refactor add tests add files spec (brant)

## 2023-10-19

- add project scaffold example usage asset spec get asset (brant)

## 2023-10-18

- add initial dependencies (brant)

## 2023-10-18

- update readme (brant)

## 2023-10-18

- Initial commit (Brant Goddard)
