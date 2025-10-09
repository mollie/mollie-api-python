# Development

## Running tests locally

To run tests locally, install [tox](https://tox.wiki/) using [uv](https://docs.astral.sh/uv/)
with [tox-uv](https://github.com/tox-dev/tox-uv):

```bash
uv tool install tox --with tox-uv
```

Install Python versions:

```bash
uv python install 3.8 3.9 3.10 3.11 3.12
```

To run tests for all Python versions:

```shell
tox
```

TODO: Deduplicate Python version list in [tests.yaml](.github/workflows/tests.yaml)
