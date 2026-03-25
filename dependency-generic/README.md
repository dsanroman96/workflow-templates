# dependency-generic template

Template for a dependency repository that versions itself and notifies consumer repositories.

## Includes

- Manual release workflow that:
  - bumps version (`patch`, `minor`, `major`) for:
    - `generic` projects via `VERSION`
    - `typescript` projects via `package.json`
    - `python` projects via `pyproject.toml` (`[project]` or `[tool.poetry]`)
  - supports monorepo paths with `version_file_path` input
  - commits and tags (`vX.Y.Z`)
  - creates a GitHub Release
  - dispatches an update event to one or many consumer repos

## Required repository secrets

- `CONSUMER_REPOS` -> one or many target repositories in `owner/repo` format.
  - supports comma-separated or newline-separated values
  - example: `owner/consumer-alpha,owner/consumer-beta`
- `CONSUMER_REPO_PAT` -> token with permission to dispatch events to the consumer repository.

## Event payload sent

- `event_type`: `dependency-released`
- `client_payload`:
  - `dependency`: dependency repository name
  - `version`: version tag (for example `v0.0.1`)

## Workflow inputs

- `bump` -> `patch`, `minor`, `major`
- `project_type` -> `generic`, `typescript`, `python`
- `version_file_path` (optional) -> override default path for monorepos
  - defaults:
    - `generic`: `VERSION`
    - `typescript`: `package.json`
    - `python`: `pyproject.toml`
  - examples:
    - `mcp/package.json`
    - `ingest/pyproject.toml`
