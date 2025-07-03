# CSV Format Reference

The source file `inventory_source/hosts.csv` defines hosts for Ansible inventory generation. This document provides a complete reference for all supported columns and their functionality.

## Overview

The CSV file supports both standard columns and dynamic product columns, plus unlimited extra variables. The system automatically detects and processes all columns, making it highly flexible for different use cases.

## Column Reference

### Required Columns

| Column | Required | Description | Example Values |
|--------|----------|-------------|----------------|
| `hostname` | ✅ | Unique system identifier | `prd-web-use1-1`, `dev-api-use1-1` |
| `environment` | ✅ | Environment classification | `production`, `development`, `test`, `acceptance` |
| `status` | ✅ | Host operational status | `active`, `decommissioned` |

### Core Identity Columns

| Column | Required | Description | Example Values |
|--------|----------|-------------|----------------|
| `cname` | ❌ | DNS alias/CNAME | `web1.example.com`, `api1.example.com` |
| `instance` | ❌ | Instance number (plain integers) | `1`, `2`, `3` (no leading zeros) |

### Infrastructure Columns

| Column | Required | Description | Example Values |
|--------|----------|-------------|----------------|
| `site_code` | ❌ | Physical location/datacenter | `use1`, `usw2`, `euw1` |
| `ssl_port` | ❌ | HTTPS/SSL port number | `443`, `8443`, `9443` |

### Application Columns

| Column | Required | Description | Example Values |
|--------|----------|-------------|----------------|
| `application_service` | ❌ | Service type/functional group | `web_server`, `api_server`, `database_server` |
| `primary_application` | ❌ | Main application name | `web`, `api`, `database` |
| `function` | ❌ | Host purpose/role | `frontend`, `backend`, `api` |

### Dynamic Product Columns

The system supports flexible product definitions using dynamic columns. You can have any number of product columns:

| Column | Required | Description | Example Values |
|--------|----------|-------------|----------------|
| `product_1` | ❌ | Primary product | `web`, `api`, `database` |
| `product_2` | ❌ | Secondary product | `analytics`, `monitoring`, `logging` |
| `product_3` | ❌ | Tertiary product | `cache`, `queue`, `search` |
| `product_4` | ❌ | Quaternary product | `backup`, `archive`, `reporting` |
| `product_N` | ❌ | Additional products (N = 5, 6, 7, ...) | Any product identifier |

**Product Column Features:**
- **Flexible**: Use as many or as few product columns as needed
- **Automatic Groups**: Each product creates a `product_{product_id}` group
- **Multiple Products**: Hosts can belong to multiple product groups
- **Sequential Naming**: Columns should be named `product_1`, `product_2`, etc.

### Operational Columns

| Column | Required | Description | Example Values |
|--------|----------|-------------|----------------|
| `batch_number` | ❌ | Patch batch number | `1`, `2`, `3` |
| `patch_mode` | ❌ | Patching automation level | `auto`, `manual` |
| `dashboard_group` | ❌ | Monitoring dashboard group | `web_servers`, `api_servers`, `database_servers` |

### Lifecycle Columns

| Column | Required | Description | Example Values |
|--------|----------|-------------|----------------|
| `decommission_date` | ❌ | Planned decommission date | `2024-12-31`, `2025-06-30` |

### Organizational Columns

| Column | Required | Description | Example Values |
|--------|----------|-------------|----------------|
| `group_path` | ❌ | Organizational group path | `applications/web`, `applications/api` |

### Extra Variables (Metadata)

**Any column not listed above is automatically treated as an extra variable and stored in the host's metadata.**

Examples of extra variables:
- `custom_role` - Custom role definition
- `monitoring_level` - Monitoring intensity level
- `backup_retention` - Backup retention period
- `security_tier` - Security classification
- `ansible_tags` - Comma-separated Ansible tags
- `notes` - General notes/comments

## CSV Examples

### Basic Example

```csv
hostname,environment,status,cname,instance,site_code,ssl_port,application_service,product_1,primary_application,function,batch_number,patch_mode,dashboard_group,decommission_date
prd-web-use1-1,production,active,web1.example.com,1,use1,443,web_server,web,web,frontend,1,auto,web_servers,
prd-api-use1-1,production,active,api1.example.com,1,use1,443,api_server,api,api,backend,1,auto,api_servers,
prd-db-use1-1,production,active,db1.example.com,1,use1,,database_server,db,database,backend,1,auto,database_servers,
```

### Multiple Products Example

```csv
hostname,environment,status,application_service,product_1,product_2,product_3,product_4
prd-web-use1-1,production,active,web_server,web,analytics,monitoring,
prd-api-use1-1,production,active,api_server,api,monitoring,logging,
prd-db-use1-1,production,active,database_server,db,backup,monitoring,
```

### With Extra Variables Example

```csv
hostname,environment,status,application_service,product_1,custom_role,monitoring_level,backup_retention,security_tier,ansible_tags
prd-web-use1-1,production,active,web_server,web,load_balancer,high,30,production,"web,production,critical"
prd-api-use1-1,production,active,api_server,api,api_gateway,high,30,production,"api,production,critical"
prd-db-use1-1,production,active,database_server,db,database_server,critical,90,production,"database,production,critical"
dev-web-use1-1,development,active,web_server,web,web_server,low,7,development,"web,development"
```

## Data Types and Validation

### Integer Fields
- `instance`: Must be plain integers (1, 2, 3) - no leading zeros
- `batch_number`: Must be integers
- `ssl_port`: Must be integers

### Date Fields
- `decommission_date`: Must be in YYYY-MM-DD format

### Status Values
- `status`: Must be one of `active`, `decommissioned`
- `patch_mode`: Must be one of `auto`, `manual`

### Environment Values
- `environment`: Must be one of `production`, `development`, `test`, `acceptance`

## Generated Groups

The system automatically creates the following groups based on CSV data:

### Application Groups
- Format: `app_{application_service}`
- Example: `app_web_server`, `app_api_server`, `app_database_server`

### Product Groups
- Format: `product_{product_id}`
- Example: `product_web`, `product_api`, `product_analytics`

### Environment Groups
- Format: `env_{environment}`
- Example: `env_production`, `env_development`, `env_test`

### Site Groups
- Format: `site_{site_code}`
- Example: `site_use1`, `site_usw2`

### Dashboard Groups
- Format: `dashboard_{dashboard_group}`
- Example: `dashboard_web_servers`, `dashboard_api_servers`

## Host Variables

The following fields are automatically included in generated host_vars files:

### Core Variables
- `hostname`, `cname`, `instance`
- `ssl_port`, `batch_number`, `patch_mode`
- `status`, `decommission_date`

### Extra Variables
- All extra variables (columns not in the standard list) are included
- Accessible in Ansible playbooks and inventory queries

## Best Practices

### Column Order
While the system is flexible with column order, we recommend this logical grouping:
1. Required fields (hostname, environment, status)
2. Identity fields (cname, instance)
3. Infrastructure fields (site_code, ssl_port)
4. Application fields (application_service, products, primary_application, function)
5. Operational fields (batch_number, patch_mode, dashboard_group)
6. Lifecycle fields (decommission_date)
7. Organizational fields (group_path)
8. Extra variables

### Naming Conventions
- Use lowercase with underscores for column names
- Use descriptive names for extra variables
- Keep product names consistent across hosts

### Data Quality
- Avoid empty required fields
- Use consistent values for categorical fields
- Validate data types before importing
- Use meaningful values for extra variables

## File Location

- **Default**: `inventory_source/hosts.csv`
- **Custom**: Use `--csv-file` option to specify a different file
- **Backup**: Always backup your CSV before making changes

## Validation

The system validates CSV data during processing:
- Required fields are present and non-empty
- Data types match expected formats
- Values are within allowed ranges
- No duplicate hostnames within the same environment

Run validation with:
```bash
python3 scripts/ansible_inventory_cli.py validate
```

## Troubleshooting

### Common Issues
1. **Missing required fields**: Ensure hostname, environment, and status are present
2. **Invalid data types**: Check integer fields for non-numeric values
3. **Invalid status/environment**: Use only allowed values
4. **Duplicate hostnames**: Ensure unique hostnames per environment

### Validation Errors
- Check the validation output for specific error messages
- Verify CSV format and data types
- Ensure all required fields are populated
