# Configuration Guide

This guide explains how to configure the Ansible Inventory Management System to match your infrastructure and requirements.

## Overview

The system uses a YAML configuration file (`inventory-config.yml`) to control all aspects of inventory generation, validation, and behavior. This file allows you to customize the system without modifying code.

## Configuration File

### Location
- **Default**: `inventory-config.yml` in the project root
- **Template**: `inventory-config.yml.example` (copy this to get started)

### Creating Configuration
```bash
# Copy the example configuration
cp inventory-config.yml.example inventory-config.yml

# Edit the configuration
nano inventory-config.yml
```

## Configuration Sections

### Version and Metadata

```yaml
version: "2.0.0"
description: "Ansible Inventory Management System Configuration"
```

### Project Structure

```yaml
paths:
  project_root: "."
  inventory_source: "inventory_source"
  inventory: "inventory"
  host_vars: "inventory/host_vars"
  group_vars: "inventory/group_vars"
  backups: "backups"
  logs: "logs"
```

**Customization Options:**
- Modify paths to match your project structure
- Ensure directories exist or the system will create them

### Data Sources

```yaml
data:
  csv_file: "inventory_source/hosts.csv"
  csv_template_headers:
    - hostname
    - environment
    - status
    - cname
    - instance
    - site_code
    - ssl_port
    - application_service
    - product_1
    - product_2
    - product_3
    - product_4
    - primary_application
    - function
    - batch_number
    - patch_mode
    - dashboard_group
    - decommission_date
    - group_path
```

**Important Notes:**
- `csv_template_headers` should match your actual CSV file headers
- The order doesn't matter as the system uses dictionary-based parsing
- Add or remove headers to match your CSV structure

### Environment Configuration

```yaml
environments:
  supported:
    - production
    - development
    - test
    - acceptance
  codes:
    production: "prd"
    development: "dev"
    test: "tst"
    acceptance: "acc"
```

**Customization:**
- Add new environments to the `supported` list
- Define environment codes for hostname patterns
- Environment codes are used in hostname validation

### Host Configuration

```yaml
hosts:
  valid_status_values:
    - active
    - decommissioned
  default_status: "active"
  
  valid_patch_modes:
    - auto
    - manual
  
  inventory_key: "hostname"  # Options: "hostname" or "cname"
  
  grace_periods:
    production: 90
    acceptance: 30
    test: 14
    development: 7
```

**Key Settings:**
- `inventory_key`: Choose whether to use hostname or cname as the primary identifier
- `grace_periods`: Days to keep decommissioned hosts before cleanup
- `valid_status_values`: Allowed host status values
- `valid_patch_modes`: Allowed patch mode values

### Group Naming Patterns

```yaml
groups:
  prefixes:
    application: "app_"
    product: "product_"
    environment: "env_"
```

**Customization:**
- Modify prefixes to match your naming conventions
- These prefixes are used when creating inventory groups

### Patch Management

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

**Customization:**
- Define patch windows for each batch number
- Add new batches as needed
- Use any time format that makes sense for your organization

### File Formats and Patterns

```yaml
formats:
  date: "%Y-%m-%d"
  timestamp: "%Y%m%d_%H%M%S"
  
  yaml_extension: ".yml"
  backup_extension: ".backup"
  csv_extension: ".csv"
  
  inventory_file_pattern: "{environment}.yml"
  environment_group_var_pattern: "env_{environment}.yml"
  host_var_file_pattern: "{hostname}.yml"
```

**Customization:**
- Modify date/time formats to match your preferences
- Change file extensions if needed
- Adjust file naming patterns

### Display and UI Settings

```yaml
display:
  console_width: 60
  tree_max_depth: 3
```

### Logging Configuration

```yaml
logging:
  level: "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### File Headers and Comments

```yaml
headers:
  auto_generated: "AUTO-GENERATED FILE - DO NOT EDIT MANUALLY"
  host_vars: "Generated from enhanced CSV with CMDB and patch management fields"
```

### Validation Settings

```yaml
validation:
  required_directories:
    - "inventory"
    - "inventory/group_vars"
    - "inventory/host_vars"
  
  expected_env_files:
    - "env_production.yml"
    - "env_development.yml"
    - "env_test.yml"
    - "env_acceptance.yml"
```

### Feature Flags

```yaml
features:
  patch_management: true
  lifecycle_management: true
  backup_on_generate: false
  strict_validation: false
  cleanup_orphaned_on_generate: true
```

**Feature Descriptions:**
- `patch_management`: Enable patch window calculations
- `lifecycle_management`: Enable decommission date handling
- `backup_on_generate`: Create CSV backups before generation
- `strict_validation`: Enable strict validation rules
- `cleanup_orphaned_on_generate`: Remove orphaned host_vars files

### Environment/Location Code Mappings

```yaml
location_codes:
  PRD:
    name: production
    inventory_file: production.yml
  TST:
    name: test
    inventory_file: test.yml
  DT:
    name: development
    inventory_file: development.yml
  ACC:
    name: acceptance
    inventory_file: acceptance.yml
```

### Field Mapping Configuration

```yaml
field_mappings:
  host_vars:
    - hostname
    - cname
    - instance
    - decommission_date
    - ssl_port
    - batch_number
    - patch_mode
    - patching_window
    - status
    - cmdb_discovery.classification
  
  group_references:
    - application_service
    - product_1
    - product_2
    - product_3
    - product_4
    - site_code
    - dashboard_group
```

**Field Mapping Options:**
- `host_vars`: Fields to include in host_vars files
- `group_references`: Fields that create inventory groups

## Environment Variable Overrides

You can override any configuration value using environment variables:

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

## Common Customizations

### Adding New Environments

1. **Add to supported list:**
   ```yaml
   environments:
     supported:
       - production
       - staging      # New environment
       - development
   ```

2. **Add environment code:**
   ```yaml
   environments:
     codes:
       staging: "stg"  # New environment code
   ```

3. **Add grace period:**
   ```yaml
   hosts:
     grace_periods:
       staging: 21     # 3 weeks
   ```

### Custom CSV Fields

1. **Add to csv_template_headers:**
   ```yaml
   data:
     csv_template_headers:
       - hostname
       - environment
       - status
       - custom_field_1  # New field
       - custom_field_2  # Another new field
   ```

2. **Add to field mappings if needed:**
   ```yaml
   field_mappings:
     host_vars:
       - custom_field_1  # Include in host_vars
     group_references:
       - custom_field_2  # Create groups from this field
   ```

### Custom Group Prefixes

```yaml
groups:
  prefixes:
    application: "app_"
    product: "product_"
    environment: "env_"
    custom: "custom_"  # New prefix
```

### Custom Patch Windows

```yaml
patch_management:
  windows:
    batch_1: "Saturday 02:00-04:00 UTC"
    batch_2: "Saturday 04:00-06:00 UTC"
    emergency: "Anytime with approval"  # Custom window
    maintenance: "Sunday 00:00-06:00 UTC"  # Another custom window
```

## Configuration Validation

The system validates your configuration on startup:

```bash
# Check configuration status
python3 scripts/ansible_inventory_cli.py --help
```

Common validation issues:
- Missing required sections
- Invalid file paths
- Unsupported environment values
- Invalid data types

## Best Practices

### Configuration Management
- Use version control for your configuration file
- Document customizations with comments
- Test configuration changes in a development environment
- Use environment variables for sensitive or environment-specific values

### Security Considerations
- Don't commit sensitive data to version control
- Use environment variables for API keys and passwords
- Restrict access to configuration files
- Regularly review and update configuration

### Performance Optimization
- Use appropriate logging levels
- Disable unused features
- Optimize CSV file size
- Use efficient file paths

## Troubleshooting Configuration

### Common Issues

1. **Configuration not found:**
   ```bash
   cp inventory-config.yml.example inventory-config.yml
   ```

2. **Invalid YAML syntax:**
   - Use a YAML validator
   - Check indentation (use spaces, not tabs)
   - Verify quotes around strings with special characters

3. **Path not found:**
   - Ensure directories exist
   - Check file permissions
   - Verify relative vs absolute paths

4. **Environment not supported:**
   - Add environment to `environments.supported` list
   - Add environment code to `environments.codes`

### Configuration Testing

```bash
# Test configuration without generating files
python3 scripts/ansible_inventory_cli.py generate --dry-run

# Validate CSV with current configuration
python3 scripts/ansible_inventory_cli.py validate

# Check configuration status
python3 -c "from scripts.core.config import print_configuration_status; print_configuration_status()"
```

## Migration Guide

### From Legacy Configuration

If you're migrating from an older version:

1. **Backup existing configuration**
2. **Copy the new example configuration**
3. **Migrate your custom settings**
4. **Test thoroughly**
5. **Update documentation**

### Configuration Version History

- **v2.0.0**: Current version with dynamic product columns and enhanced features
- **v1.x**: Legacy version with single product_id column

## Support

For configuration issues:
1. Check the validation output
2. Review the example configuration
3. Test with minimal configuration
4. Check the logs for detailed error messages 