# Water Column Sonar Catalog

🌊 STAC Catalog for Water Column Sonar Data ⭐

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/CI-CMG/water-column-sonar-catalog/test_action.yaml)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/CI-CMG/water-column-sonar-catalog) ![GitHub repo size](https://img.shields.io/github/repo-size/CI-CMG/water-column-sonar-catalog)

# Browser

Copy url of stac catalog and
goto: https://radiantearth.github.io/stac-browser/#/?.language=en
or: https://radiantearth.github.io/stac-browser/#/external/raw.githubusercontent.com/CI-CMG/water-column-sonar-catalog/refs/heads/main/level_2_stac_catalog/HB1906/collection.json

# Ecosystem

The following are all the projects under the 'water-column-sonar' processing portfolio:

- https://github.com/CI-CMG/water-column-sonar-annotation (convert EVR files)
- https://github.com/CI-CMG/water-column-sonar-processing (main python processing)
- https://github.com/CI-CMG/water-column-sonar-visualization (experimental WebGL)
- https://github.com/CI-CMG/water-column-sonar-ospool (converting files in bulk)
- https://github.com/CI-CMG/water-column-sonar-ui (echofish ui)
- https://github.com/CI-CMG/water-column-sonar-resampling (experimental DataTree)
- https://github.com/CI-CMG/water-column-sonar-api (spring boot api w neo4j)
- https://github.com/CI-CMG/water-column-sonar-knowledge-graph (neo4j graph + IaC)
- https://github.com/CI-CMG/water-column-sonar-ai (experimental work w SonarAI)
- https://github.com/CI-CMG/water-column-sonar-catalog (STAC Catalog)

# Setting up the Python Environment

```
uv python install --reinstall
uv venv
Python 3.12.12
```

# Installing Dependencies

```
source .venv/bin/activate
# or ".venv\Scripts\activate" in windows
uv sync --all-groups
uv pip install --upgrade pi
uv run pre-commit install
```

# Pytest

```
uv run pytest --cache-clear tests # -W ignore::DeprecationWarning
```

or
> pytest --cache-clear --cov=src tests/ --cov-report=xml

# Test Coverage

```commandline
uv run pytest --cov=water_column_sonar_catalog
```

With line numbers

```commandline
uv run pytest tests/geometry --cov=water_column_sonar_catalog --cov-report term-missing
```

Current status:
...

# Pre Commit Hook

see here for installation: https://pre-commit.com/
https://dev.to/rafaelherik/using-trufflehog-and-pre-commit-hook-to-prevent-secret-exposure-edo

```
uv run pre-commit install --allow-missing-config
# or
uv run pre-commit install
```

# Tag a Release

Step 1: Increment the semantic version in the zarr_manager.py "metadata" & the "pyproject.toml"

Step 2:

```commandline
git tag -a v26.1.17 -m "Releasing v26.1.17"
git push origin --tags
#gh release create v26.1.14
```

# To Publish To PROD

```
uv build --no-sources
uv publish
```

# Data Debugging

HB0707 Zoomable Cruise:
https://hb0707.s3.us-east-1.amazonaws.com/index.html

# UV Debugging

```
uv pip install --upgrade pip
#uv sync --all-groups
uv run pre-commit install
uv lock --check
uv lock
uv sync --all-groups
uv run pytest --cache-clear tests
```

# Slack

```
/github subscribe CI-CMG/water-column-sonar-catalog issues pulls commits releases deployments reviews branches comments discussions workflows:{event: "push"}
```
