# CSV Format Reference

This document describes the CSV format used by the Ansible Inventory Management System.

## File Location

The CSV file should be located at `inventory_source/hosts.csv` by default, but can be customized via configuration.

## Required Fields

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `hostname` | ⚠️ | **Primary host identifier** (required if using hostname as inventory key) | `prd-web-01` |
| `cname` | ⚠️ | **Canonical name** (required if using cname as inventory key) | `web01.example.com` |
| `environment` | ✅ | Environment name | `production`, `development`, `test`, `acceptance` |
| `status` | ✅ | Host status | `active`, `decommissioned` |

### Hostname vs CNAME Relationship

**Important:** You must provide **at least one** of `hostname` or `cname`, but you can provide both:

- **If using `hostname` as inventory key** (default): `hostname` is required, `cname` is optional
- **If using `cname` as inventory key**: `cname` is required, `hostname` is optional
- **Best practice**: Provide both for maximum flexibility

**Configuration:** Set your preference in `inventory-config.yml`:
```yaml
hosts:
  inventory_key: "hostname"  # or "cname"
```

## Optional Fields

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `instance` | ❌ | Instance number | `1`, `2`, `3` |
| `site_code` | ❌ | Datacenter/location code | `use1`, `usw2`, `euw1` |
| `ssl_port` | ❌ | SSL port number | `443`, `8443` |
| `application_service` | ❌ | Service type | `web_server`, `api_server`, `database_server` |
| `product_1` | ❌ | Primary product | `web`, `api`, `analytics` |
| `product_2` | ❌ | Secondary product | `monitoring`, `logging`, `cache` |
| `product_3` | ❌ | Tertiary product | `backup`, `security`, `load_balancer` |
| `product_4` | ❌ | Quaternary product | `cdn`, `dns`, `mail` |
| `batch_number` | ❌ | Patch batch number | `1`, `2`, `3` |
| `patch_mode` | ❌ | Patching mode | `auto`, `manual` |
| `dashboard_group` | ❌ | Monitoring dashboard group | `web_servers`, `api_servers` |
| `primary_application` | ❌ | Primary application | `wordpress`, `django`, `rails` |
| `function` | ❌ | Host function/role | `frontend`, `backend`, `database` |
| `decommission_date` | ❌ | Decommission date (YYYY-MM-DD) | `2025-12-31` |
| `ansible_tags` | ❌ | Comma-separated Ansible tags | `web,production,monitoring` |




## Dynamic Product Columns

The system supports **unlimited** product definitions using numbered columns:

- `product_1` - Primary product (recommended)
- `product_2` - Secondary product (optional)
- `product_3` - Tertiary product (optional)
- `product_4` - Quaternary product (optional)
- `product_5`, `product_6`, `product_7`, etc. - Additional products (unlimited)

**Benefits:**
- **Unlimited product assignments** - No artificial limit on number of products
- No need to modify code for new products
- Supports hosts with 1 to N products (where N is unlimited)
- Automatic group creation for each product
- Flexible CSV structure

**Example Usage:**
```csv
hostname,environment,product_1,product_2,product_3,product_4,product_5,product_6
web01,production,web,monitoring,analytics,cdn,ssl,backup
api01,production,api,logging,cache,load_balancer,,
db01,production,database,backup,monitoring,replication,,
```

**Important Notes:**
- Product columns should be sequential (product_1, product_2, product_3, etc.)
- Empty product columns are ignored
- Each non-empty product creates a `product_{product_id}` group
- No limit on the number of products per host

## Extra Variables

Any column not in the standard field list is treated as an extra variable:

```csv
hostname,environment,custom_role,monitoring_level,backup_retention
web01,production,frontend,high,30
api01,production,backend,medium,7
```

**Extra variables are:**
- ✅ Included in host_vars files
- ✅ Accessible in Ansible playbooks
- ✅ Preserved during processing
- ✅ Available in inventory queries

## Data Validation

### Required Field Validation
- `environment`: Must be one of `production`, `development`, `test`, `acceptance`
- `status`: Must be one of `active`, `decommissioned`
- **At least one of `hostname` or `cname` must be provided** (based on inventory key configuration)

### Data Type Validation
- `ssl_port`: Must be an integer
- `batch_number`: Must be an integer
- `instance`: Must be a positive integer without leading zeros
- `decommission_date`: Must be in YYYY-MM-DD format

### Product Validation
- At least one product should be defined (recommended)
- No duplicate products allowed
- Product columns should be sequential (product_1, product_2, etc.)

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

## Host Variables vs Group Variables

Understanding how CSV fields are processed is crucial for effective Ansible integration.

### Host Variables (host_vars)

**Host variables** are stored in individual files for each host (e.g., `inventory/host_vars/hostname.yml`). These contain host-specific data that varies from host to host.

#### Fields That Become Host Variables

The following fields are automatically included in host_vars files:

| Field | Description | Example Value |
|-------|-------------|---------------|
| `hostname` | Host identifier | `prd-web-01` |
| `cname` | Canonical name | `web01.example.com` |
| `instance` | Instance number | `1` |
| `ssl_port` | SSL port number | `443` |
| `batch_number` | Patch batch | `1` |
| `patch_mode` | Patching mode | `auto` |
| `status` | Host status | `active` |
| `decommission_date` | Decommission date | `2025-12-31` |

**Plus all extra variables** (any column not in the standard field list).

#### Example Host Variables File
```yaml
# inventory/host_vars/prd-web-01.yml
---
hostname: prd-web-01
cname: web01.example.com
instance: 1
ssl_port: 443
batch_number: 1
patch_mode: auto
status: active
custom_role: frontend          # Extra variable
monitoring_level: high         # Extra variable
backup_retention: 30           # Extra variable
```

### Group Variables (group_vars)

**Group variables** are stored in files that apply to all hosts in a specific group. These contain shared configuration that applies to multiple hosts.

#### Fields That Create Groups

The following fields automatically create inventory groups:

| Field | Group Name | Description |
|-------|------------|-------------|
| `environment` | `env_{environment}` | Environment groups (env_production, env_development, etc.) |
| `application_service` | `app_{application_service}` | Application groups (app_web_server, app_api_server, etc.) |
| `product_1`, `product_2`, etc. | `product_{product_id}` | Product groups (product_web, product_api, etc.) |
| `site_code` | `site_{site_code}` | Site groups (site_use1, site_usw2, etc.) |
| `dashboard_group` | `dashboard_{dashboard_group}` | Dashboard groups (dashboard_web_servers, etc.) |

#### Required Group Variables Files

To make the system work properly, you need to create group_vars files for the groups you use. The system expects these files to exist:

##### Environment Group Variables
Create files for each environment you use:

```yaml
# inventory/group_vars/env_production.yml
---
# Production environment variables
environment_tag: production
critical_system: true

# Security policies
security:
  access_control: strict
  data_encryption: AES256
  firewall_rules:
    - allow http from any to any
    - allow https from any to any
    - deny all other

# Patch management
patch_management:
  policy: automated
  window: Saturday 02:00-04:00 UTC
  approval_process: required
  reboot_policy: automatic

# Monitoring
monitoring:
  enabled: true
  alert_thresholds:
    cpu_usage: 80
    memory_usage: 75
    disk_usage: 90
  alert_channels:
    - email: production-alerts@example.com
    - slack: "#production-alerts"

# Backup
backup:
  enabled: true
  frequency: daily
  retention_days: 30
  location: s3://production-backups
```

```yaml
# inventory/group_vars/env_development.yml
---
# Development environment variables
environment_tag: development
critical_system: false

# Less strict security for development
security:
  access_control: relaxed
  data_encryption: AES128

# Different patch window
patch_management:
  policy: manual
  window: Friday 18:00-20:00 UTC
  approval_process: none
  reboot_policy: manual

# Basic monitoring
monitoring:
  enabled: true
  alert_thresholds:
    cpu_usage: 90
    memory_usage: 85
    disk_usage: 95
  alert_channels:
    - email: dev-alerts@example.com

# Shorter backup retention
backup:
  enabled: true
  frequency: weekly
  retention_days: 7
  location: s3://development-backups
```

##### Application Group Variables
Create files for each application service you use:

```yaml
# inventory/group_vars/app_web_server.yml
---
# Web server application variables
role: web_server
web_server_config:
  port: 80
  ssl_port: 443
  document_root: /var/www/html
  log_level: info
  max_connections: 1000

# Web-specific monitoring
monitoring:
  web_metrics: true
  response_time_threshold: 200ms
  uptime_monitoring: true

# Web-specific security
security:
  ssl_ciphers: HIGH:!aNULL:!MD5
  http_headers:
    - X-Frame-Options: DENY
    - X-Content-Type-Options: nosniff
    - X-XSS-Protection: 1; mode=block
```

```yaml
# inventory/group_vars/app_api_server.yml
---
# API server application variables
role: api_server
api_server_config:
  port: 8080
  ssl_port: 8443
  max_requests: 10000
  timeout: 30s

# API-specific monitoring
monitoring:
  api_metrics: true
  response_time_threshold: 100ms
  rate_limiting_monitoring: true

# API-specific security
security:
  authentication_required: true
  rate_limiting: true
  cors_policy: strict
```

##### Product Group Variables
Create files for each product you use:

```yaml
# inventory/group_vars/product_web.yml
---
# Web product variables
products:
  - web_product_suite

product_features:
  web_analytics: true
  cdn_integration: true
  seo_optimization: true

product_version: "1.0.0"
product_owner: "Web Team"

# Web-specific configurations
web_config:
  static_file_serving: true
  compression_enabled: true
  cache_headers: true
```

```yaml
# inventory/group_vars/product_api.yml
---
# API product variables
products:
  - api_product_suite

product_features:
  rest_api: true
  graphql_support: false
  rate_limiting: true

product_version: "2.1.0"
product_owner: "API Team"

# API-specific configurations
api_config:
  authentication_method: jwt
  rate_limit_requests: 1000
  rate_limit_window: 1h
```

```yaml
# inventory/group_vars/product_analytics.yml
---
# Analytics product variables
products:
  - analytics_product_suite

product_features:
  data_collection: true
  reporting: true
  dashboards: true

product_version: "3.0.0"
product_owner: "Data Team"

# Analytics-specific configurations
analytics_config:
  data_retention_days: 365
  sampling_rate: 100
  export_formats: ["json", "csv", "excel"]
```

##### Site Group Variables
Create files for each site/location you use:

```yaml
# inventory/group_vars/site_use1.yml
---
# US East 1 site variables
site_name: "US East 1"
site_region: us-east-1
site_timezone: "America/New_York"

# Site-specific networking
networking:
  vpc_id: vpc-12345678
  subnet_ids: ["subnet-12345678", "subnet-87654321"]
  security_groups: ["sg-12345678"]

# Site-specific monitoring
monitoring:
  site_latency_threshold: 50ms
  regional_alerts: true
```

```yaml
# inventory/group_vars/site_usw2.yml
---
# US West 2 site variables
site_name: "US West 2"
site_region: us-west-2
site_timezone: "America/Los_Angeles"

# Site-specific networking
networking:
  vpc_id: vpc-87654321
  subnet_ids: ["subnet-87654321", "subnet-12345678"]
  security_groups: ["sg-87654321"]

# Site-specific monitoring
monitoring:
  site_latency_threshold: 50ms
  regional_alerts: true
```

### How Group Variables Work

#### Hierarchy and Inheritance
Group variables follow Ansible's standard hierarchy:

1. **all** group variables (apply to all hosts)
2. **Environment** group variables (env_production, env_development, etc.)
3. **Application** group variables (app_web_server, app_api_server, etc.)
4. **Product** group variables (product_web, product_api, etc.)
5. **Site** group variables (site_use1, site_usw2, etc.)
6. **Host** variables (individual host_vars files)

#### Variable Precedence
Variables are merged in order, with later groups overriding earlier ones:

```yaml
# env_production.yml (applies to all production hosts)
monitoring:
  enabled: true
  alert_thresholds:
    cpu_usage: 80

# app_web_server.yml (overrides for web servers)
monitoring:
  enabled: true
  alert_thresholds:
    cpu_usage: 70  # Overrides the 80 from env_production
  web_metrics: true  # Adds web-specific monitoring
```

### Creating Group Variables Files

#### Step 1: Identify Required Groups
Based on your CSV data, identify which groups you need:

```bash
# Check what groups are being created
ansible-inventory -i inventory/production.yml --graph
```

#### Step 2: Create Group Variables Files
Create the necessary files in `inventory/group_vars/`:

```bash
# Create environment group vars
touch inventory/group_vars/env_production.yml
touch inventory/group_vars/env_development.yml
touch inventory/group_vars/env_test.yml
touch inventory/group_vars/env_acceptance.yml

# Create application group vars (based on your application_service values)
touch inventory/group_vars/app_web_server.yml
touch inventory/group_vars/app_api_server.yml
touch inventory/group_vars/app_database_server.yml

# Create product group vars (based on your product_1, product_2, etc. values)
touch inventory/group_vars/product_web.yml
touch inventory/group_vars/product_api.yml
touch inventory/group_vars/product_analytics.yml

# Create site group vars (based on your site_code values)
touch inventory/group_vars/site_use1.yml
touch inventory/group_vars/site_usw2.yml
```

#### Step 3: Add Variables to Each File
Use the examples above as templates and customize for your environment.

#### Step 4: Test Your Configuration
```bash
# Test that variables are accessible
ansible-inventory -i inventory/production.yml --host prd-web-01

# Test group targeting
ansible product_web -i inventory/production.yml --list-hosts
```

### Best Practices

#### Group Variables Organization
1. **Environment-specific**: Put environment-wide settings in env_*.yml files
2. **Application-specific**: Put application-wide settings in app_*.yml files
3. **Product-specific**: Put product-wide settings in product_*.yml files
4. **Site-specific**: Put location-specific settings in site_*.yml files

#### Variable Naming
- Use descriptive, hierarchical names
- Avoid conflicts between different group types
- Use consistent naming conventions

#### Testing
- Always test group variable inheritance
- Verify variable precedence works as expected
- Test group targeting in playbooks

### Troubleshooting

#### Common Issues
1. **Missing group_vars files**: Groups won't have variables if files don't exist
2. **Variable conflicts**: Later groups override earlier ones
3. **Incorrect file names**: Must match exact group names
4. **YAML syntax errors**: Invalid YAML will cause failures

#### Debug Commands
```bash
# Check what groups exist
ansible-inventory -i inventory/production.yml --graph

# Check host variables (including inherited group vars)
ansible-inventory -i inventory/production.yml --host hostname

# Check specific group variables
ansible-inventory -i inventory/production.yml --list | grep -A 10 "group_name"
```

## File Location

The CSV file should be located at `inventory_source/hosts.csv` by default, but can be customized via configuration.

## Example CSV

```csv
hostname,environment,status,cname,instance,site_code,ssl_port,application_service,product_1,product_2,product_3,product_4,batch_number,patch_mode,dashboard_group,primary_application,function,decommission_date,custom_role,monitoring_level
prd-web-01,production,active,web01.example.com,1,use1,443,web_server,web,monitoring,,,1,auto,web_servers,wordpress,frontend,,frontend,high
prd-api-01,production,active,api01.example.com,1,use1,8443,api_server,api,logging,cache,,2,auto,api_servers,django,backend,,backend,medium
prd-db-01,production,active,db01.example.com,1,use1,,database_server,database,backup,,,3,manual,database_servers,postgresql,database,,primary,high
dev-web-01,development,active,dev-web01.example.com,1,use1,443,web_server,web,,,1,auto,dev_servers,wordpress,frontend,,frontend,low
```

## Configuration

The CSV format can be customized via `inventory-config.yml`:

```yaml
data:
  csv_file: "inventory_source/hosts.csv"
  csv_template_headers:
    - hostname
    - environment
    - status
    # ... other headers

field_mappings:
  host_vars:
    - hostname
    - cname
    - instance
    # ... fields to include in host_vars
  
  group_references:
    - application_service
    - product_1
    - product_2
    - product_3
    - product_4
    - site_code
    - dashboard_group
```

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
1. **Missing required fields**: Ensure environment and status are present, plus either hostname or cname (based on inventory key)
2. **Invalid data types**: Check integer fields for non-numeric values
3. **Invalid status/environment**: Use only allowed values
4. **Duplicate identifiers**: Ensure unique hostname/cname per environment (based on inventory key)
5. **Wrong inventory key**: Check that you're providing the field specified in `inventory_key` configuration

### Validation Errors
- Check the validation output for specific error messages
- Verify CSV format and data types
- Ensure all required fields are populated
