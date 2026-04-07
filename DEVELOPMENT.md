# Development

## Running tests locally

To run tests locally, install [tox](https://tox.wiki/) using [uv](https://docs.astral.sh/uv/)
with [tox-uv](https://github.com/tox-dev/tox-uv):

```bash
uv tool install tox --with tox-uv
```

Install Python versions:

```bash
uv python install 3.10 3.11 3.12 3.13
```

To run tests for all Python versions:

```shell
tox
```

## Fixing codestyle issues

If the tests fail on the flake8 step, run:

    make fix-codestyle

TODO: Deduplicate Python version list in [tests.yaml](.github/workflows/tests.yaml)
