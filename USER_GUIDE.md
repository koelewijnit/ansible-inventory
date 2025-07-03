# User Guide - Ansible Inventory Management System

This comprehensive user guide provides everything you need to know to effectively use the Ansible Inventory Management System.

## Table of Contents

1. [Getting Started](#getting-started)
2. [CSV Data Management](#csv-data-management)
3. [Configuration](#configuration)
4. [Core Operations](#core-operations)
5. [Advanced Features](#advanced-features)
6. [Ansible Integration](#ansible-integration)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- **Python**: 3.8+ (recommended: 3.11+)
- **Ansible**: 2.9+ (recommended: 2.18+)
- **Operating System**: Linux, macOS, Windows (with WSL)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/ansible-inventory-cli.git
cd ansible-inventory-cli

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy configuration
cp inventory-config.yml.example inventory-config.yml
```

### First Steps

1. **Configure the system**: Edit `inventory-config.yml` to match your environment
2. **Prepare your CSV**: Create or modify `inventory_source/hosts.csv`
3. **Generate inventory**: Run `python3 scripts/ansible_inventory_cli.py generate`
4. **Test with Ansible**: Use the generated inventory files

## CSV Data Management

### Understanding the CSV Structure

The system supports a flexible CSV structure with these column types:

#### Required Columns
```csv
hostname,environment,status
prd-web-01,production,active
dev-api-01,development,active
```

#### Standard Columns
- **Identity**: `cname`, `instance`
- **Infrastructure**: `site_code`, `ssl_port`
- **Application**: `application_service`, `primary_application`, `function`
- **Operational**: `batch_number`, `patch_mode`, `dashboard_group`
- **Lifecycle**: `decommission_date`

#### Dynamic Product Columns
```csv
hostname,environment,status,product_1,product_2,product_3
prd-web-01,production,active,web,analytics,
prd-api-01,production,active,api,monitoring,logging
```

#### Extra Variables
Any additional columns become host metadata:
```csv
hostname,environment,status,custom_role,monitoring_level,backup_retention
prd-web-01,production,active,load_balancer,high,30
prd-api-01,production,active,api_gateway,high,30
```

### Creating Your First CSV

1. **Start with required fields**:
   ```csv
   hostname,environment,status
   prd-web-01,production,active
   ```

2. **Add application information**:
   ```csv
   hostname,environment,status,application_service,product_1
   prd-web-01,production,active,web_server,web
   ```

3. **Add infrastructure details**:
   ```csv
   hostname,environment,status,application_service,product_1,site_code,ssl_port
   prd-web-01,production,active,web_server,web,use1,443
   ```

4. **Add operational data**:
   ```csv
   hostname,environment,status,application_service,product_1,site_code,ssl_port,batch_number,patch_mode
   prd-web-01,production,active,web_server,web,use1,443,1,auto
   ```

### CSV Best Practices

#### Data Quality
- Use consistent naming conventions
- Validate data types (integers for numeric fields)
- Avoid empty required fields
- Use meaningful values for extra variables

#### Organization
- Group related columns together
- Use descriptive column names
- Document custom columns
- Keep data consistent across environments

#### Maintenance
- Regular backups of CSV files
- Version control for CSV changes
- Validation before committing changes
- Regular cleanup of obsolete data

## Configuration

### Configuration File Overview

The system uses `inventory-config.yml` for all configuration:

```yaml
# Version and metadata
version: "2.0.0"
description: "Ansible Inventory Management System Configuration"

# Project structure
paths:
  project_root: "."
  inventory_source: "inventory_source"
  inventory: "inventory"
  host_vars: "inventory/host_vars"
  group_vars: "inventory/group_vars"

# Data sources
data:
  csv_file: "inventory_source/hosts.csv"
  csv_template_headers:
    - hostname
    - environment
    - status
    # ... other headers

# Environment configuration
environments:
  supported:
    - production
    - development
    - test
    - acceptance
  codes:
    production: "prd"
    development: "dev"
```

### Key Configuration Sections

#### Environment Configuration
```yaml
environments:
  supported:
    - production
    - development
    - test
    - acceptance
    - staging  # Add new environments here
  codes:
    production: "prd"
    development: "dev"
    staging: "stg"  # Add environment codes
```

#### Host Configuration
```yaml
hosts:
  valid_status_values:
    - active
    - decommissioned
  default_status: "active"
  
  valid_patch_modes:
    - auto
    - manual
  
  inventory_key: "hostname"  # or "cname"
  
  grace_periods:
    production: 90
    development: 7
    staging: 21  # Add grace periods
```

#### Feature Flags
```yaml
features:
  patch_management: true
  lifecycle_management: true
  backup_on_generate: false
  strict_validation: false
  cleanup_orphaned_on_generate: true
```

### Environment Variable Overrides

Override any configuration value using environment variables:

```bash
# Override CSV file location
export INVENTORY_CSV_FILE="/path/to/custom/hosts.csv"

# Override logging level
export INVENTORY_LOG_LEVEL="DEBUG"

# Override inventory key preference
export INVENTORY_KEY="cname"

# Override support group
export INVENTORY_SUPPORT_GROUP="DevOps Team"
```

## Core Operations

### Basic Commands

#### Generate Inventory
```bash
# Generate all environments
python3 scripts/ansible_inventory_cli.py generate

# Generate specific environments
python3 scripts/ansible_inventory_cli.py generate --environments production test

# Use custom CSV file
python3 scripts/ansible_inventory_cli.py --csv-file custom.csv generate

# Dry run (preview without creating files)
python3 scripts/ansible_inventory_cli.py generate --dry-run
```

#### Validate Data
```bash
# Validate current CSV
python3 scripts/ansible_inventory_cli.py validate

# Validate with custom CSV
python3 scripts/ansible_inventory_cli.py --csv-file custom.csv validate

# Validate with debug output
python3 scripts/ansible_inventory_cli.py --log-level DEBUG validate
```

#### Health Check
```bash
# Check system health
python3 scripts/ansible_inventory_cli.py health

# Health check with custom CSV
python3 scripts/ansible_inventory_cli.py --csv-file custom.csv health

# Health check with JSON output
python3 scripts/ansible_inventory_cli.py --json health
```

### Advanced Commands

#### Lifecycle Management
```bash
# List expired hosts
python3 scripts/ansible_inventory_cli.py lifecycle list-expired

# Cleanup with dry run
python3 scripts/ansible_inventory_cli.py lifecycle cleanup --dry-run

# Actually cleanup expired hosts
python3 scripts/ansible_inventory_cli.py lifecycle cleanup

# Extend decommission date
python3 scripts/ansible_inventory_cli.py lifecycle extend --host prd-web-01 --days 30
```

#### Custom Options
```bash
# Use CNAME as inventory key
python3 scripts/ansible_inventory_cli.py generate --inventory-key cname

# Custom output directory
python3 scripts/ansible_inventory_cli.py generate --output-dir /tmp/inventory

# Custom host_vars directory
python3 scripts/ansible_inventory_cli.py generate --host-vars-dir /tmp/host_vars

# Quiet mode for scripting
python3 scripts/ansible_inventory_cli.py --quiet generate
```

## Advanced Features

### Dynamic Product Columns

The system supports flexible product definitions:

#### Basic Product Usage
```csv
hostname,environment,status,product_1
prd-web-01,production,active,web
prd-api-01,production,active,api
```

#### Multiple Products per Host
```csv
hostname,environment,status,product_1,product_2,product_3
prd-web-01,production,active,web,analytics,
prd-api-01,production,active,api,monitoring,logging
prd-db-01,production,active,db,backup,monitoring
```

#### Generated Groups
Each product creates a group:
- `product_web` - All hosts with web product
- `product_api` - All hosts with api product
- `product_analytics` - All hosts with analytics product

### Extra Variables (Metadata)

Any CSV column not in the standard list becomes an extra variable:

#### Adding Extra Variables
```csv
hostname,environment,status,custom_role,monitoring_level,backup_retention,security_tier
prd-web-01,production,active,load_balancer,high,30,production
prd-api-01,production,active,api_gateway,high,30,production
prd-db-01,production,active,database_server,critical,90,production
```

#### Accessing in Ansible
```yaml
# playbook.yml
---
- name: Example playbook
  hosts: all
  tasks:
    - name: Show custom role
      debug:
        msg: "Host {{ inventory_hostname }} has custom role: {{ custom_role }}"
    
    - name: Show monitoring level
      debug:
        msg: "Host {{ inventory_hostname }} has monitoring level: {{ monitoring_level }}"
    
    - name: Configure backup retention
      debug:
        msg: "Setting backup retention to {{ backup_retention }} days"
```

### Patch Management

Configure patch windows in your configuration:

```yaml
patch_management:
  windows:
    batch_1: "Saturday 02:00-04:00 UTC"
    batch_2: "Saturday 04:00-06:00 UTC"
    batch_3: "Saturday 06:00-08:00 UTC"
    dev_batch: "Friday 18:00-20:00 UTC"
    test_batch: "Friday 20:00-22:00 UTC"
    acc_batch: "Friday 22:00-24:00 UTC"
```

### Lifecycle Management

Manage host decommissioning:

```bash
# Mark host for decommissioning
# Edit CSV: set status to "decommissioned" and add decommission_date

# List hosts past decommission date
python3 scripts/ansible_inventory_cli.py lifecycle list-expired

# Preview cleanup
python3 scripts/ansible_inventory_cli.py lifecycle cleanup --dry-run

# Perform cleanup
python3 scripts/ansible_inventory_cli.py lifecycle cleanup
```

## Ansible Integration

### Testing Generated Inventory

#### Basic Inventory Commands
```bash
# List all hosts
ansible-inventory -i inventory/production.yml --list

# Show inventory structure
ansible-inventory -i inventory/production.yml --graph

# List hosts in specific group
ansible-inventory -i inventory/production.yml --list-hosts app_web_server

# Show host variables
ansible-inventory -i inventory/production.yml --host prd-web-01
```

#### Group Targeting
```bash
# Target application group
ansible-playbook playbook.yml -i inventory/production.yml --limit app_web_server

# Target product group
ansible-playbook playbook.yml -i inventory/production.yml --limit product_web

# Target environment group
ansible-playbook playbook.yml -i inventory/production.yml --limit env_production

# Target site group
ansible-playbook playbook.yml -i inventory/production.yml --limit site_use1
```

### Using in Playbooks

#### Basic Playbook Example
```yaml
# playbook.yml
---
- name: Configure web servers
  hosts: app_web_server
  tasks:
    - name: Show host information
      debug:
        msg: "Configuring {{ inventory_hostname }} ({{ cname }})"
    
    - name: Show products
      debug:
        msg: "Host has products: {{ products }}"
```

#### Advanced Playbook Example
```yaml
# advanced_playbook.yml
---
- name: Configure based on custom variables
  hosts: all
  tasks:
    - name: Configure monitoring based on level
      debug:
        msg: "Configuring {{ monitoring_level }} monitoring for {{ inventory_hostname }}"
      when: monitoring_level is defined
    
    - name: Configure backup retention
      debug:
        msg: "Setting backup retention to {{ backup_retention }} days"
      when: backup_retention is defined
    
    - name: Configure security tier
      debug:
        msg: "Applying {{ security_tier }} security configuration"
      when: security_tier is defined
```

### Generated Groups Reference

#### Application Groups
- `app_web_server` - All web servers
- `app_api_server` - All API servers
- `app_database_server` - All database servers

#### Product Groups
- `product_web` - All hosts with web product
- `product_api` - All hosts with api product
- `product_analytics` - All hosts with analytics product

#### Environment Groups
- `env_production` - All production hosts
- `env_development` - All development hosts
- `env_test` - All test hosts

#### Site Groups
- `site_use1` - All hosts in use1 site
- `site_usw2` - All hosts in usw2 site

#### Dashboard Groups
- `dashboard_web_servers` - All hosts in web_servers dashboard
- `dashboard_api_servers` - All hosts in api_servers dashboard

## Best Practices

### CSV Management

#### Data Organization
- Use consistent naming conventions
- Group related columns together
- Document custom columns
- Regular validation and cleanup

#### Version Control
- Commit CSV changes with descriptive messages
- Use branches for major changes
- Review changes before merging
- Keep backups of important data

### Configuration Management

#### Environment-Specific Configuration
```yaml
# Use environment variables for sensitive data
environments:
  production:
    backup_location: "s3://production-backups"
  development:
    backup_location: "s3://development-backups"
```

#### Feature Management
```yaml
# Enable/disable features as needed
features:
  patch_management: true
  lifecycle_management: true
  backup_on_generate: false  # Disable in development
  strict_validation: true    # Enable in production
```

### Automation

#### CI/CD Integration
```yaml
# .gitlab-ci.yml example
stages:
  - validate
  - generate
  - test

validate_inventory:
  stage: validate
  script:
    - python3 scripts/ansible_inventory_cli.py validate

generate_inventory:
  stage: generate
  script:
    - python3 scripts/ansible_inventory_cli.py generate
  artifacts:
    paths:
      - inventory/

test_inventory:
  stage: test
  script:
    - ansible-inventory -i inventory/production.yml --list
    - ansible-inventory -i inventory/production.yml --graph
```

#### Monitoring Scripts
```bash
#!/bin/bash
# inventory_monitor.sh

set -e

echo "Starting inventory monitoring..."

# Check health
python3 scripts/ansible_inventory_cli.py health

# Validate data
python3 scripts/ansible_inventory_cli.py validate

# Generate inventory
python3 scripts/ansible_inventory_cli.py generate

echo "Inventory monitoring completed successfully!"
```

### Performance Optimization

#### Large CSV Files
- Use `--quiet` mode for large files
- Generate specific environments only
- Use SSD storage for better performance
- Optimize CSV by removing unnecessary columns

#### Memory Usage
- Monitor memory usage with `--timing`
- Use streaming for very large files
- Regular cleanup of old data
- Optimize configuration for your use case

## Troubleshooting

### Common Issues

#### CSV Parsing Errors
```bash
# Check CSV format
python3 scripts/ansible_inventory_cli.py validate

# Debug CSV loading
python3 -c "from scripts.core.utils import load_csv_data; print(load_csv_data())"
```

#### Configuration Issues
```bash
# Check configuration status
python3 -c "from scripts.core.config import print_configuration_status; print_configuration_status()"

# Validate configuration
python3 -c "from scripts.core.config import validate_configuration; warnings = validate_configuration(); print(warnings)"
```

#### Permission Issues
```bash
# Check file permissions
ls -la inventory_source/hosts.csv
ls -la inventory/

# Fix permissions if needed
chmod 644 inventory_source/hosts.csv
chmod -R 755 inventory/
```

### Debug Mode

#### Enable Debug Logging
```bash
# Enable debug logging
python3 scripts/ansible_inventory_cli.py --log-level DEBUG generate

# Debug specific component
python3 -c "import logging; logging.basicConfig(level=logging.DEBUG); from scripts.core.models import Host; print('Debug mode enabled')"
```

#### Validation Debugging
```bash
# Detailed validation
python3 scripts/ansible_inventory_cli.py --log-level DEBUG validate

# Check specific validation aspects
python3 -c "from scripts.core.utils import validate_csv_structure; result = validate_csv_structure(Path('inventory_source/hosts.csv')); print(result.get_summary())"
```

### Getting Help

#### Documentation
- Check the [CSV Format Reference](docs/csv_format.md)
- Review the [Configuration Guide](docs/configuration.md)
- Read the [Usage Guide](docs/usage.md)
- Consult the [FAQ](docs/faq.md)

#### Support Resources
- Use built-in validation tools
- Check error messages carefully
- Review logs for detailed information
- Test with minimal examples

---

**Need more help?** Check the [FAQ](docs/faq.md) for common questions or review the [Configuration Guide](docs/configuration.md) for advanced configuration options.
- **Feature Rollouts:** Tag hosts participating in a new feature rollout.
- **Compliance Audits:** Tag hosts that require specific compliance checks.

**Important Considerations:**
- Tags are free-form strings. Ensure consistency in naming to avoid issues.
- Avoid using spaces within a single tag (e.g., use `web_server` instead of `web server`).
---

### **Group Targeting**

#### **Application Service Groups**
Target hosts by function across all products:

```bash
# All web servers (Apache + Nginx + others)
ansible app_web_server -i inventory/production.yml --list-hosts

# All databases (PostgreSQL + MongoDB + others)
ansible app_database -i inventory/production.yml --list-hosts

# All identity management systems
ansible app_identity_management -i inventory/production.yml --list-hosts
```

#### **Product-Specific Groups**
Target hosts by specific software:

```bash
# Only Apache HTTP servers
ansible product_apache_httpd -i inventory/production.yml --list-hosts

# Only PostgreSQL databases
ansible product_postgresql -i inventory/production.yml --list-hosts

# Only Kubernetes infrastructure
ansible product_kubernetes -i inventory/production.yml --list-hosts
```

---

## 🛡️ **Best Practices**

### **Operational Best Practices**

1. **Regular Health Checks**: Monitor inventory health daily
2. **Staged Changes**: Always use `--dry-run` for lifecycle operations
3. **Backup Before Changes**: CSV files are automatically backed up
4. **Validate After Changes**: Run validation after any modifications
5. **Environment Consistency**: Keep environments synchronized

### **CSV Management Best Practices**

1. **Version Control**: Keep CSV files in version control
2. **Regular Backups**: Use automated backup strategies
3. **Data Validation**: Validate data before importing
4. **Consistent Formats**: Maintain consistent naming conventions
5. **Documentation**: Document any custom fields or conventions

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **CSV File Not Found**
```bash
ERROR: CSV file not found: inventory_source/hosts.csv
```
**Solution**: Verify file path and permissions, or use `--csv-file` to specify correct path.

#### **Invalid Date Format**
```bash
ERROR: Invalid date format: 12/31/2025. Use YYYY-MM-DD
```
**Solution**: Use ISO date format: `2025-12-31`

### **Exit Codes**

- **0**: Success
- **1**: Command error (validation failed, invalid input)
- **2**: File not found
- **3**: Unexpected error

---

**Version**: 4.0.0  
**Status**: Production Ready  
**Team**: Infrastructure as Code Team

---



## 🎯 **Ansible Integration**

### **Group Targeting**

#### **Application Service Groups**
Target hosts by function across all products:

```bash
# All web servers (Apache + Nginx + others)
ansible app_web_server -i inventory/production.yml --list-hosts

# All databases (PostgreSQL + MongoDB + others)
ansible app_database -i inventory/production.yml --list-hosts

# All identity management systems
ansible app_identity_management -i inventory/production.yml --list-hosts
```

#### **Product-Specific Groups**
Target hosts by specific software:

```bash
# Only Apache HTTP servers
ansible product_apache_httpd -i inventory/production.yml --list-hosts

# Only PostgreSQL databases
ansible product_postgresql -i inventory/production.yml --list-hosts

# Only Kubernetes infrastructure
ansible product_kubernetes -i inventory/production.yml --list-hosts
```

---

## 🛡️ **Best Practices**

### **Operational Best Practices**

1. **Regular Health Checks**: Monitor inventory health daily
2. **Staged Changes**: Always use `--dry-run` for lifecycle operations
3. **Backup Before Changes**: CSV files are automatically backed up
4. **Validate After Changes**: Run validation after any modifications
5. **Environment Consistency**: Keep environments synchronized

### **CSV Management Best Practices**

1. **Version Control**: Keep CSV files in version control
2. **Regular Backups**: Use automated backup strategies
3. **Data Validation**: Validate data before importing
4. **Consistent Formats**: Maintain consistent naming conventions
5. **Documentation**: Document any custom fields or conventions

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **CSV File Not Found**
```bash
ERROR: CSV file not found: inventory_source/hosts.csv
```
**Solution**: Verify file path and permissions, or use `--csv-file` to specify correct path.

#### **Invalid Date Format**
```bash
ERROR: Invalid date format: 12/31/2025. Use YYYY-MM-DD
```
**Solution**: Use ISO date format: `2025-12-31`

### **Exit Codes**

- **0**: Success
- **1**: Command error (validation failed, invalid input)
- **2**: File not found
- **3**: Unexpected error

---

**Version**: 4.0.0  
**Status**: Production Ready  
**Team**: Infrastructure as Code Team
