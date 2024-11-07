To create an automated release and automatically publish to PyPI for the Pythonik project, follow these steps to ensure the process is smooth and automated:


### Step-by-Step Guide to Creating a Release

1. **Update the Changelog:**
   - Open the `docs/CHANGELOG.md` file.
   - Add a new entry for the version you are about to release. Ensure the version number is clearly mentioned and follows the format used in previous entries.
   - Include a descriptive release name within quotes, as this will be extracted automatically by the workflow. For example:
     ```markdown
     ## 1955-11-05 "Great Scott, Marty McFly!" - version 8.8.8
     "Exciting New Features"
     - Backwards compatibility with the future
     - flux capicator 
     ```

2. **Commit the Changes:**
   - After updating the changelog, commit your changes. Make sure your commit message is clear and descriptive.
   - Example commit message:
     ```
     Update changelog for version 8.8.8
     ```

3. **Tag the Commit:**
   - Tag the commit including or afteryour changelog update. This tag will trigger the release workflow. Pythonik uses semantic versioning. Please see the [semver.org](https://semver.org/) website for more information.
   - Use the following command to tag your commit:
     ```bash
     git tag 8.8.8 
     ```
   - Push the tag to the repository:
     ```bash
     git push --tags
     ```

4. **Automated Release Process:**
   - Once the tag is pushed, the GitHub Actions workflow `.github/workflows/create-release.yml` will automatically run.
   - The workflow will:
     - Extract the version and release name from the changelog.
     - Generate release notes based on the commit history.
     - Create a GitHub release with the extracted information.

5. **Publishing the Release:**
   - The release will be published to PyPI automatically. 

### Additional Notes

- **Release Name Extraction:** The workflow uses `awk` to find the version line in the changelog and extracts the release name from it. Ensure the release name is enclosed in quotes.

By following these steps, you can ensure that the release process for Pythonik is efficient and automated.