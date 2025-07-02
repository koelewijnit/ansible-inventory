# CSV Format

Each row describes a host. Required columns are:

- `hostname`
- `environment`
- `status`

Example:

```csv
hostname,environment,status
web01,production,active
db01,production,active
```

Keep the file in `inventory_source/hosts.csv` unless overridden.
