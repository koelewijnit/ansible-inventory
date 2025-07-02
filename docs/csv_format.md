# CSV Format

The source file `inventory_source/hosts.csv` defines hosts. Required columns are listed first, followed by optional metadata.

| Column | Description |
| ------ | ----------- |
| `hostname` | Unique system name |
| `environment` | Environment such as `production` or `development` |
| `status` | `active` or `decommissioned` |
| `cname` | DNS alias (optional) |
| `instance` | Instance number (optional) |
| `datacenter` | Physical location |
| `ssl_port` | HTTPS port |
| `application_service` | Functional group, e.g. `web` |
| `product_id` | Product identifier |
| `primary_application` | Main application |
| `function` | Purpose of the host |
| `batch_number` | Patch batch |
| `patch_mode` | `auto` or `manual` |
| `dashboard_group` | Monitoring group |
| `decommission_date` | Planned removal date |
| `ansible_tags` | Extra tags for playbooks |

Example snippet:

```csv
hostname,environment,status,cname
web01,production,active,
db01,production,active,
```

Keep the file in `inventory_source/hosts.csv` unless overridden with `--csv-file`.
