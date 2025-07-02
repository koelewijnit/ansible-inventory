# FAQ

## The CLI cannot find `hosts.csv`

Ensure `inventory_source/hosts.csv` exists or pass `--csv-file` with the path.

## How do I remove a host?

Set its status to `decommissioned` in the CSV and run `generate`.

## Where are inventories written?

By default to `inventory/`. Use `--output-dir` to change the location.
