## Release Process ##
To create a release there are a few steps you should follow:
- We use [Semantic Versioning](https://semver.org/). If you're going to release a breaking change or a major new feature, do a minor version bump (x.y.z => x.y+1.z). Otherwise, do a patch version bump (x.y.z => x.y.z+1).
- If you decide to do a minor version change, handle deprecations. See (Pending)DeprecationWarning subclasses in `error.py`.
- Update the version number in `version.py` and push this to master.
- Create a new tag with the new version number in the following way: `git tag v<major.minor.patch>`.
- Push the tag by using `git push --tags`.
- Create a release on [GitHub](https://github.com/mollie/mollie-api-python/releases/new) with a summary of changes.
