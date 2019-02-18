## Release Process ##
To create a release there are a few steps you should follow:
- Update the version number in `version.py` and push this to master. We use [Semantic Versioning](https://semver.org/).
- Create a new tag with the new version number in the following way: `git tag v<major.minor.patch>`.
- Push the tag by using `git push --tags`.
- Create a release on [GitHub](https://github.com/mollie/mollie-api-python/releases/new) with a summary of changes.
