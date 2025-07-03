# Frequently Asked Questions (FAQ)

This FAQ addresses common questions and issues when using the Ansible Inventory Management System.

## General Questions

### What is the Ansible Inventory Management System?

The Ansible Inventory Management System is a powerful tool that converts CSV host data into structured YAML inventories that Ansible understands. It supports dynamic product columns, extra variables, comprehensive validation, and lifecycle management.

### What are the main benefits?

- **Flexible CSV Structure**: Support for dynamic product columns and unlimited extra variables
- **Automatic Group Creation**: Creates logical groups based on CSV data
- **Comprehensive Validation**: Validates data integrity and Ansible compatibility
- **Lifecycle Management**: Handles host decommissioning and cleanup
- **Enterprise Features**: Patch management, health monitoring, backup support
- **Easy Configuration**: YAML-based configuration with environment variable overrides

### What versions of Python and Ansible are supported?

- **Python**: 3.8+ (recommended: 3.11+)
- **Ansible**: 2.9+ (recommended: 2.18+)
- **Operating Systems**: Linux, macOS, Windows (with WSL)

## CSV and Data Questions

### What CSV format is supported?

The system supports flexible CSV formats with these column types:
- **Required**: `hostname`, `environment`, `status`
- **Standard**: Identity, infrastructure, application, operational, and lifecycle columns
- **Dynamic Products**: `product_1`, `product_2`, `product_3`, etc.
- **Extra Variables**: Any additional columns become host metadata

### How do dynamic product columns work?

Dynamic product columns allow you to define multiple products per host:
- Use `product_1`, `product_2`, `product_3`, etc.
- Each product creates a `product_{product_id}` group
- Hosts can belong to multiple product groups
- No CSV parsing issues (unlike comma-separated values)

### Can I add custom columns to the CSV?

Yes! Any column not in the standard list becomes an "extra variable":
- Automatically stored in host metadata
- Accessible in Ansible playbooks
- No configuration required
- Examples: `custom_role`, `monitoring_level`, `backup_retention`

### What data types are supported?

- **Strings**: Most fields (hostname, environment, etc.)
- **Integers**: `instance`, `batch_number`, `ssl_port`
- **Dates**: `decommission_date` (YYYY-MM-DD format)
- **Enumerated**: `status` (active/decommissioned), `patch_mode` (auto/manual)

### How do I validate my CSV data?

```bash
# Basic validation
python3 scripts/ansible_inventory_cli.py validate

# Validate with custom CSV file
python3 scripts/ansible_inventory_cli.py --csv-file custom.csv validate
```

## Configuration Questions

### How do I configure the system?

1. Copy the example configuration:
   ```bash
   cp inventory-config.yml.example inventory-config.yml
   ```

2. Edit the configuration file to match your needs
3. See the [Configuration Guide](configuration.md) for detailed options

### Can I use environment variables for configuration?

Yes! You can override any configuration value:
```bash
export INVENTORY_CSV_FILE="/path/to/custom/hosts.csv"
export INVENTORY_LOG_LEVEL="DEBUG"
export INVENTORY_KEY="cname"
```

### How do I add new environments?

1. Add to the supported environments list in configuration
2. Define environment codes
3. Set grace periods for the new environment

### Can I customize group naming?

Yes! You can modify group prefixes in the configuration:
```yaml
groups:
  prefixes:
    application: "app_"
    product: "product_"
    environment: "env_"
    custom: "custom_"
```

## Usage Questions

### How do I generate inventory?

```bash
# Generate all environments
python3 scripts/ansible_inventory_cli.py generate

# Generate specific environments
python3 scripts/ansible_inventory_cli.py generate --environments production test

# Use custom CSV file
python3 scripts/ansible_inventory_cli.py --csv-file custom.csv generate
```

### How do I check system health?

```bash
# Basic health check
python3 scripts/ansible_inventory_cli.py health

# Health check with custom CSV
python3 scripts/ansible_inventory_cli.py --csv-file custom.csv health
```

### How do I manage host lifecycle?

```bash
# List expired hosts
python3 scripts/ansible_inventory_cli.py lifecycle list-expired

# Cleanup expired hosts (dry run)
python3 scripts/ansible_inventory_cli.py lifecycle cleanup --dry-run

# Actually cleanup expired hosts
python3 scripts/ansible_inventory_cli.py lifecycle cleanup
```

### Can I use CNAME instead of hostname as the primary identifier?

Yes! Set the inventory key in configuration or use the command line option:
```bash
# In configuration
hosts:
  inventory_key: "cname"

# Or via command line
python3 scripts/ansible_inventory_cli.py generate --inventory-key cname
```

## Ansible Integration Questions

### How do I test the generated inventory?

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

### What groups are automatically created?

The system creates these groups based on CSV data:
- **Application Groups**: `app_web_server`, `app_api_server`
- **Product Groups**: `product_web`, `product_api`, `product_analytics`
- **Environment Groups**: `env_production`, `env_development`
- **Site Groups**: `site_use1`, `site_usw2`
- **Dashboard Groups**: `dashboard_web_servers`

### How do I target specific groups in Ansible?

```bash
# Target application group
ansible-playbook playbook.yml -i inventory/production.yml --limit app_web_server

# Target product group
ansible-playbook playbook.yml -i inventory/production.yml --limit product_web

# Target environment group
ansible-playbook playbook.yml -i inventory/production.yml --limit env_production
```

### How do I access extra variables in Ansible playbooks?

Extra variables are automatically available in host_vars:
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
```

## Troubleshooting Questions

### CSV parsing errors

**Q: I'm getting CSV parsing errors. What should I check?**

A: Common issues and solutions:
1. **Check CSV format**: Ensure proper comma separation and quoting
2. **Validate data types**: Check integer fields for non-numeric values
3. **Check required fields**: Ensure hostname, environment, and status are present
4. **Run validation**: Use `python3 scripts/ansible_inventory_cli.py validate`

### Configuration issues

**Q: The system can't find my configuration file.**

A: Solutions:
1. **Copy example configuration**: `cp inventory-config.yml.example inventory-config.yml`
2. **Check file location**: Ensure `inventory-config.yml` is in the project root
3. **Check permissions**: Ensure the file is readable
4. **Validate YAML syntax**: Use a YAML validator

### Permission errors

**Q: I'm getting permission errors when generating inventory.**

A: Solutions:
1. **Check file permissions**: `ls -la inventory_source/hosts.csv`
2. **Fix permissions**: `chmod 644 inventory_source/hosts.csv`
3. **Check directory permissions**: `chmod -R 755 inventory/`
4. **Run as appropriate user**: Ensure you have write permissions

### Missing groups or hosts

**Q: Some hosts or groups are missing from the generated inventory.**

A: Check these common issues:
1. **Host status**: Ensure hosts have `status: active`
2. **Environment values**: Check that environment values match configuration
3. **Required fields**: Ensure hostname and environment are populated
4. **Data validation**: Run validation to check for data issues

### Ansible compatibility issues

**Q: Ansible can't read the generated inventory.**

A: Troubleshooting steps:
1. **Check inventory format**: `ansible-inventory -i inventory/production.yml --list`
2. **Validate YAML syntax**: Check for YAML syntax errors
3. **Check file permissions**: Ensure Ansible can read the files
4. **Test with simple inventory**: Create a minimal test case

## Performance Questions

### Large CSV files

**Q: How does the system handle large CSV files?**

A: The system is optimized for large files:
- **Streaming processing**: Processes CSV data in chunks
- **Memory efficient**: Doesn't load entire file into memory
- **Progress reporting**: Shows progress for large operations
- **Quiet mode**: Use `--quiet` for scripting with large files

### Generation speed

**Q: How can I improve generation speed?**

A: Optimization tips:
1. **Generate specific environments**: Use `--environments` to limit scope
2. **Use quiet mode**: `--quiet` reduces output overhead
3. **Optimize CSV**: Remove unnecessary columns and rows
4. **SSD storage**: Use fast storage for large files

## Migration Questions

### From legacy systems

**Q: How do I migrate from a legacy inventory system?**

A: Migration steps:
1. **Export data**: Export your current inventory to CSV format
2. **Map fields**: Map your fields to the new CSV structure
3. **Test migration**: Use validation to check data integrity
4. **Generate inventory**: Create new inventory files
5. **Test with Ansible**: Verify everything works correctly

### From old product_id format

**Q: I have CSV files with the old product_id column. How do I migrate?**

A: The system automatically handles this:
- **Automatic detection**: Detects old `product_id` columns
- **Backward compatibility**: Still supports the old format
- **Migration tools**: Use the conversion script if needed
- **Validation**: Run validation to ensure compatibility

## Advanced Questions

### Custom group logic

**Q: Can I create custom group logic beyond the standard groups?**

A: Yes! You can:
1. **Add custom columns**: Create columns that will generate groups
2. **Modify configuration**: Add custom fields to group_references
3. **Use extra variables**: Create groups based on metadata
4. **Post-processing**: Modify generated inventory files

### Integration with external systems

**Q: Can I integrate with external systems like CMDB or monitoring?**

A: The system supports integration through:
1. **Extra variables**: Store external system data in CSV
2. **Environment variables**: Override configuration from external sources
3. **API integration**: Use the Python API for programmatic access
4. **Custom scripts**: Extend functionality with custom scripts

### Backup and recovery

**Q: How do I backup and recover my inventory data?**

A: Backup strategies:
1. **CSV backup**: `cp inventory_source/hosts.csv backups/hosts_$(date +%Y%m%d).csv`
2. **Inventory backup**: `cp -r inventory/ backups/inventory_$(date +%Y%m%d)/`
3. **Configuration backup**: `cp inventory-config.yml backups/config_$(date +%Y%m%d).yml`
4. **Automated backups**: Create scripts for regular backups

### Monitoring and alerting

**Q: How can I monitor the inventory system?**

A: Monitoring options:
1. **Health checks**: Regular `health` command execution
2. **Validation monitoring**: Monitor validation results
3. **File monitoring**: Watch for changes in CSV and inventory files
4. **Integration**: Integrate with existing monitoring systems

## Support Questions

### Getting help

**Q: Where can I get help if I have issues?**

A: Support resources:
1. **Documentation**: Check the comprehensive documentation
2. **FAQ**: Review this FAQ for common issues
3. **Validation**: Use built-in validation tools
4. **Community**: Check for existing issues or create new ones
5. **Debug mode**: Use `--log-level DEBUG` for detailed information

### Reporting bugs

**Q: How do I report a bug?**

A: When reporting bugs, please include:
1. **Version information**: System version and configuration
2. **Error messages**: Complete error output
3. **Steps to reproduce**: Detailed reproduction steps
4. **Sample data**: Minimal CSV example that reproduces the issue
5. **Environment details**: OS, Python version, Ansible version

### Feature requests

**Q: How do I request a new feature?**

A: Feature request guidelines:
1. **Clear description**: Explain what you want to achieve
2. **Use case**: Describe the specific use case
3. **Benefits**: Explain the benefits of the feature
4. **Implementation ideas**: Suggest how it might be implemented
5. **Priority**: Indicate the priority level

---

**Still have questions?** Check the [Usage Guide](usage.md) for detailed examples or the [Configuration Guide](configuration.md) for advanced configuration options.
