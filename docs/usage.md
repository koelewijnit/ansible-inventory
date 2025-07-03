# Usage Guide

This guide provides comprehensive instructions for using the Ansible Inventory Management System, including all commands, options, and practical examples.

## Quick Start

### Basic Usage

```bash
# Generate inventory from CSV
python3 scripts/ansible_inventory_cli.py generate

# Validate CSV data
python3 scripts/ansible_inventory_cli.py validate

# Check system health
python3 scripts/ansible_inventory_cli.py health
```

### Using Custom CSV File

```bash
# Use a different CSV file
python3 scripts/ansible_inventory_cli.py --csv-file /path/to/custom/hosts.csv generate

# Validate custom CSV file
python3 scripts/ansible_inventory_cli.py --csv-file /path/to/custom/hosts.csv validate
```

## Command Reference

### Main Commands

#### `generate` - Generate Ansible Inventory

Creates YAML inventory files and host_vars from CSV data.

```bash
python3 scripts/ansible_inventory_cli.py generate [OPTIONS]
```

**Options:**
- `--output-dir, -o PATH`: Output directory for inventory files (default: inventory)
- `--host-vars-dir PATH`: Output directory for host_vars files (default: inventory/host_vars)
- `--environments, -e ENV [ENV ...]`: Specific environments to generate (default: all)
- `--dry-run`: Show what would be generated without creating files
- `--inventory-key {hostname,cname}`: Key to use for inventory host entries (default: hostname)

**Examples:**
```bash
# Generate all environments
python3 scripts/ansible_inventory_cli.py generate

# Generate only production and test environments
python3 scripts/ansible_inventory_cli.py generate --environments production test

# Generate with custom output directory
python3 scripts/ansible_inventory_cli.py generate --output-dir custom_inventory

# Use CNAME as inventory key
python3 scripts/ansible_inventory_cli.py generate --inventory-key cname

# Dry run to see what would be generated
python3 scripts/ansible_inventory_cli.py generate --dry-run
```

#### `validate` - Validate CSV and Inventory

Validates CSV data, inventory structure, and Ansible compatibility.

```bash
python3 scripts/ansible_inventory_cli.py validate [OPTIONS]
```

**What it validates:**
- CSV file format and data types
- Required fields and values
- Inventory structure
- Ansible compatibility
- Group_vars and host_vars files

**Examples:**
```bash
# Validate current CSV
python3 scripts/ansible_inventory_cli.py validate

# Validate custom CSV file
python3 scripts/ansible_inventory_cli.py --csv-file custom.csv validate
```

#### `health` - System Health Check

Performs comprehensive health monitoring of the inventory system.

```bash
python3 scripts/ansible_inventory_cli.py health [OPTIONS]
```

**What it checks:**
- CSV file accessibility
- Host counts and status
- Orphaned files
- Missing files
- Overall system health

**Examples:**
```bash
# Check system health
python3 scripts/ansible_inventory_cli.py health

# Health check with custom CSV
python3 scripts/ansible_inventory_cli.py --csv-file custom.csv health
```

#### `lifecycle` - Lifecycle Management

Manages host lifecycle operations including decommissioning and cleanup.

```bash
python3 scripts/ansible_inventory_cli.py lifecycle <SUBCOMMAND> [OPTIONS]
```

**Subcommands:**
- `list-expired`: List hosts past their decommission date
- `cleanup`: Remove decommissioned hosts from CSV
- `extend`: Extend decommission dates for hosts

**Examples:**
```bash
# List expired hosts
python3 scripts/ansible_inventory_cli.py lifecycle list-expired

# Cleanup with dry run
python3 scripts/ansible_inventory_cli.py lifecycle cleanup --dry-run

# Actually cleanup expired hosts
python3 scripts/ansible_inventory_cli.py lifecycle cleanup

# Extend decommission date for a host
python3 scripts/ansible_inventory_cli.py lifecycle extend --host prd-web-use1-1 --days 30
```

### Global Options

All commands support these global options:

- `--csv-file PATH`: Specify custom CSV file location
- `--log-level {DEBUG,INFO,WARNING,ERROR}`: Set logging level
- `--json`: Output results in JSON format
- `--quiet`: Suppress non-error output
- `--timing`: Show timing information
- `--version`: Show version information
- `--help, -h`: Show help message

## Practical Examples

### Basic Workflow

```bash
# 1. Validate your CSV data
python3 scripts/ansible_inventory_cli.py validate

# 2. Generate inventory
python3 scripts/ansible_inventory_cli.py generate

# 3. Check system health
python3 scripts/ansible_inventory_cli.py health

# 4. Test with Ansible
ansible-inventory -i inventory/production.yml --list
```

### Environment-Specific Operations

```bash
# Generate only production environment
python3 scripts/ansible_inventory_cli.py generate --environments production

# Generate development and test environments
python3 scripts/ansible_inventory_cli.py generate --environments development test

# Validate specific environment
python3 scripts/ansible_inventory_cli.py validate --environments production
```

### Custom Configurations

```bash
# Use CNAME as primary identifier
python3 scripts/ansible_inventory_cli.py generate --inventory-key cname

# Custom output directory
python3 scripts/ansible_inventory_cli.py generate --output-dir /tmp/inventory

# Custom host_vars directory
python3 scripts/ansible_inventory_cli.py generate --host-vars-dir /tmp/host_vars
```

### Advanced Usage

```bash
# Generate with debug logging
python3 scripts/ansible_inventory_cli.py --log-level DEBUG generate

# Output results in JSON format
python3 scripts/ansible_inventory_cli.py --json health

# Quiet mode for scripting
python3 scripts/ansible_inventory_cli.py --quiet generate

# Show timing information
python3 scripts/ansible_inventory_cli.py --timing generate
```

## Ansible Integration

### Testing Generated Inventory

```bash
# List all hosts
ansible-inventory -i inventory/production.yml --list

# Show inventory structure
ansible-inventory -i inventory/production.yml --graph

# List hosts in specific group
ansible-inventory -i inventory/production.yml --list-hosts app_web_server

# Show host variables
ansible-inventory -i inventory/production.yml --host prd-web-use1-1
```

### Using in Playbooks

```yaml
# playbook.yml
---
- name: Example playbook
  hosts: app_web_server
  tasks:
    - name: Show host information
      debug:
        msg: "Host {{ inventory_hostname }} has products: {{ products }}"
```

### Targeting Specific Groups

```bash
# Run playbook on web servers
ansible-playbook playbook.yml -i inventory/production.yml --limit app_web_server

# Run on hosts with specific product
ansible-playbook playbook.yml -i inventory/production.yml --limit product_web

# Run on production environment
ansible-playbook playbook.yml -i inventory/production.yml --limit env_production
```

## CSV Management

### Creating CSV Template

```bash
# Get CSV template with headers
python3 -c "from scripts.core.utils import get_csv_template; print(get_csv_template())"
```

### CSV Validation

```bash
# Validate CSV structure
python3 scripts/ansible_inventory_cli.py validate

# Check specific validation aspects
python3 -c "from scripts.core.utils import validate_csv_structure; result = validate_csv_structure(Path('inventory_source/hosts.csv')); print(result.get_summary())"
```

### CSV Backup and Restore

```bash
# Create backup
cp inventory_source/hosts.csv inventory_source/hosts_$(date +%Y%m%d_%H%M%S).backup

# Restore from backup
cp inventory_source/hosts_20241201_120000.backup inventory_source/hosts.csv
```

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

```bash
# Enable debug logging
python3 scripts/ansible_inventory_cli.py --log-level DEBUG generate

# Debug specific component
python3 -c "import logging; logging.basicConfig(level=logging.DEBUG); from scripts.core.models import Host; print('Debug mode enabled')"
```

## Automation and Scripting

### Shell Scripts

```bash
#!/bin/bash
# inventory_update.sh

set -e

echo "Starting inventory update..."

# Validate CSV
python3 scripts/ansible_inventory_cli.py validate

# Generate inventory
python3 scripts/ansible_inventory_cli.py generate

# Check health
python3 scripts/ansible_inventory_cli.py health

echo "Inventory update completed successfully!"
```

### CI/CD Integration

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

### Python Scripts

```python
#!/usr/bin/env python3
# custom_inventory_script.py

from scripts.core.utils import load_csv_data
from scripts.core.models import Host
from scripts.managers.inventory_manager import InventoryManager

# Load CSV data
hosts_data = load_csv_data()

# Create Host objects
hosts = [Host.from_csv_row(row) for row in hosts_data]

# Use inventory manager
manager = InventoryManager()
manager.generate_inventory(hosts)

print(f"Generated inventory for {len(hosts)} hosts")
```

## Best Practices

### Regular Maintenance

```bash
# Daily health check
python3 scripts/ansible_inventory_cli.py health

# Weekly validation
python3 scripts/ansible_inventory_cli.py validate

# Monthly cleanup
python3 scripts/ansible_inventory_cli.py lifecycle cleanup
```

### Backup Strategy

```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp inventory_source/hosts.csv backups/hosts_${DATE}.csv
cp inventory/ backups/inventory_${DATE}/
```

### Monitoring

```bash
# Check for orphaned files
python3 scripts/ansible_inventory_cli.py health | grep "Orphaned Files"

# Monitor host counts
python3 scripts/ansible_inventory_cli.py health | grep "Total Hosts"
```

## Performance Optimization

### Large CSV Files

```bash
# Use quiet mode for large files
python3 scripts/ansible_inventory_cli.py --quiet generate

# Generate specific environments only
python3 scripts/ansible_inventory_cli.py generate --environments production
```

### Memory Usage

```bash
# Monitor memory usage
python3 scripts/ansible_inventory_cli.py --timing generate

# Use streaming for very large files
# (Built into the system automatically)
```

## Support and Help

### Getting Help

```bash
# General help
python3 scripts/ansible_inventory_cli.py --help

# Command-specific help
python3 scripts/ansible_inventory_cli.py generate --help
python3 scripts/ansible_inventory_cli.py validate --help
python3 scripts/ansible_inventory_cli.py health --help
python3 scripts/ansible_inventory_cli.py lifecycle --help
```

### Version Information

```bash
# Check version
python3 scripts/ansible_inventory_cli.py --version

# Check configuration version
python3 -c "from scripts.core.config import VERSION; print(f'Config version: {VERSION}')"
```
