# FAQ

## The CLI cannot find `hosts.csv`

Check that `inventory_source/hosts.csv` exists or use `--csv-file` to specify a path.

## How do I remove a host?

Mark the host with status `decommissioned` and run `generate`.

## Where are inventories written?

By default to the `inventory/` directory. Use `--output-dir` to change.
