# Getting Started with Simplified Ansible Inventory

## Overview

This repository provides a simplified approach to creating Ansible inventories with automatic batch grouping using Ansible's native `constructed` plugin.

## What You Get

- **Automatic Batch Groups**: `batch_1`, `batch_2`, `batch_3` based on CSV `batch_number` column
- **Environment Groups**: `env_production`, `env_development`, `env_test`
- **Application Groups**: `app_web_server`, `app_api_server`, etc.
- **Product Groups**: `product_web`, `product_api`, etc.
- **Site Groups**: `site_us_east_1`, etc.

## Step-by-Step Setup

### 1. Prepare Your CSV File

Place your CSV file in `inventory_source/` with these columns (minimum):
```csv
hostname,environment,batch_number
```

Example with all supported columns:
```csv
hostname,environment,status,application_service,product_1,batch_number,site_code,cname
test-web-01,production,active,web_server,web,1,us-east-1,test-web-01.example.com
test-api-01,production,active,api_server,api,2,us-east-1,test-api-01.example.com
test-db-01,production,active,database_server,db,3,us-east-1,test-db-01.example.com
```

### 2. Install Dependencies

```bash
pip install pyyaml
```

### 3. Convert CSV to Inventory

```bash
python simple_csv_converter.py
```

This creates:
- `inventory/hosts.yml` - Simple base inventory
- `inventory/constructed.yml` - Dynamic grouping configuration
- `inventory/host_vars/*.yml` - Individual host variables
- `inventory/USAGE.md` - Detailed usage examples

### 4. Test the Inventory

```bash
# List all hosts
ansible-inventory -i inventory/constructed.yml --list

# Show inventory structure
ansible-inventory -i inventory/constructed.yml --graph

# List hosts in batch_1
ansible-inventory -i inventory/constructed.yml --list-hosts batch_1
```

### 5. Use with Ansible Playbooks

```bash
# Run playbook on batch_1 hosts
ansible-playbook -i inventory/constructed.yml site.yml --limit batch_1

# Run on production batch_2 hosts only
ansible-playbook -i inventory/constructed.yml site.yml --limit production_batch_2

# Run on all web servers
ansible-playbook -i inventory/constructed.yml site.yml --limit web_servers
```

## Common Use Cases

### Patch Management by Batches
```bash
# Patch batch_1 (typically non-critical systems)
ansible-playbook -i inventory/constructed.yml patch.yml --limit batch_1

# Patch batch_2 (application servers)
ansible-playbook -i inventory/constructed.yml patch.yml --limit batch_2

# Patch batch_3 (critical systems like databases)
ansible-playbook -i inventory/constructed.yml patch.yml --limit batch_3
```

### Environment-Specific Operations
```bash
# Deploy to development environment
ansible-playbook -i inventory/constructed.yml deploy.yml --limit development_hosts

# Restart all production web servers
ansible-playbook -i inventory/constructed.yml restart.yml --limit "production_hosts:&web_servers"
```

### Application-Specific Tasks
```bash
# Update all API servers
ansible-playbook -i inventory/constructed.yml update-api.yml --limit api_servers

# Backup all database servers
ansible-playbook -i inventory/constructed.yml backup.yml --limit db_servers
```

## Customizing Groups

### Add New Automatic Groups

Edit `inventory/constructed.yml`:
```yaml
keyed_groups:
  # Add groups based on any CSV column
  - key: datacenter
    prefix: dc
    separator: "_"
  - key: team
    prefix: team
    separator: "_"
```

### Add Conditional Groups

```yaml
groups:
  # Custom conditional groups
  critical_prod: environment == "production" and batch_number == "3"
  web_cluster: application_service == "web_server" and status == "active"
  emergency_contact: team == "oncall" and environment == "production"
```

### Create Computed Variables

```yaml
compose:
  # Create new variables from existing ones
  full_env_batch: environment + "_batch_" + (batch_number | string)
  server_tier: '"critical" if batch_number == "3" else "standard"'
```

## Advanced Features

### Multiple Product Support

If your CSV has multiple product columns:
```csv
hostname,product_1,product_2,product_3
web-01,frontend,monitoring,logging
```

Add to `keyed_groups`:
```yaml
keyed_groups:
  - key: product_1
    prefix: product
  - key: product_2
    prefix: product
  - key: product_3
    prefix: product
```

### Site-Based Grouping

For multi-site deployments:
```yaml
groups:
  primary_site: site_code == "us-east-1"
  disaster_recovery: site_code == "us-west-2"
  cross_site_db: application_service == "database_server" and (site_code == "us-east-1" or site_code == "us-west-2")
```

## Troubleshooting

### Check Inventory Generation
```bash
# Validate inventory syntax
ansible-inventory -i inventory/constructed.yml --list > /dev/null

# Show parsing details
ansible-inventory -i inventory/constructed.yml --list -vvv
```

### Debug Group Membership
```bash
# Check which groups a host belongs to
ansible-inventory -i inventory/constructed.yml --host test-web-01

# List all groups
ansible-inventory -i inventory/constructed.yml --list | jq 'keys[]'
```

### Common Issues

1. **CSV Encoding**: Ensure CSV is UTF-8 encoded
2. **Empty Values**: Empty CSV cells are converted to empty strings
3. **Special Characters**: Use underscores instead of spaces in group names
4. **Case Sensitivity**: Group names are case-sensitive

## Migration Tips

### From Complex Inventory Systems

1. **Export existing data to CSV format**
2. **Run the converter**: `python simple_csv_converter.py`
3. **Test compatibility**: Compare old vs new group membership
4. **Update playbooks**: Replace old inventory file paths with `inventory/constructed.yml`
5. **Remove old system**: Delete complex Python code

### Maintaining Existing Workflows

The simplified system maintains compatibility:
- Same group names (batch_1, batch_2, etc.)
- Same Ansible commands work
- Same playbook --limit patterns work
- Host variables available in same format

## Next Steps

1. **Read the detailed usage guide**: `inventory/USAGE.md`
2. **Customize grouping rules**: Edit `inventory/constructed.yml`
3. **Set up automation**: Add CSV conversion to your CI/CD pipeline
4. **Explore Ansible features**: Check out other `constructed` plugin capabilities

The simplified approach gives you all the power of complex inventory systems with 95% less code to maintain!