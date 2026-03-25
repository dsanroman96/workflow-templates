# consumer-generic template

Template for a generic consumer repository that tracks dependency versions in `deps/`.

## Includes

- Workflow that listens for dependency update events.
- Automatic update of `deps/<dependency>.version`.
- Commit and push when version changes.

## Triggered by dependency repositories

Expected `repository_dispatch` payload:

- `event_type`: `dependency-released`
- `client_payload`:
  - `dependency`: dependency name (for example `dep-beta`)
  - `version`: tag (for example `v0.0.1`)

## Manual testing

The workflow can also be run manually with:

- `dependency`: dependency name
- `version`: version tag
