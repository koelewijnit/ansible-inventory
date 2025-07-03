# Frequently Asked Questions (FAQ)

This document answers common questions about the Ansible Inventory Management System.

## General Questions

### What is this system?

The Ansible Inventory Management System converts CSV host data into structured YAML inventories that Ansible can understand. It supports dynamic product columns, extra variables, and comprehensive lifecycle management.

### What are the main features?

- **Dynamic Product Support**: Flexible product definitions using `product_1`, `product_2`, etc.
- **Extra Variables**: Any CSV column becomes an Ansible variable
- **Automatic Grouping**: Creates logical groups based on CSV data
- **Validation**: Comprehensive data validation and health checks
- **Lifecycle Management**: Handles host decommissioning and cleanup
- **Makefile Integration**: Convenient commands for all operations

## CSV and Data Questions

### What CSV format does the system support?

The system supports a flexible CSV format with:
- **Required fields**: `environment`, `status` (plus either `hostname` or `cname`)
- **Optional fields**: Various infrastructure and application fields
- **Dynamic products**: `product_1`, `product_2`, `product_3`, `product_4`
- **Extra variables**: Any additional columns become host variables

See the [CSV Format Reference](csv_format.md) for complete details.

### How do dynamic product columns work?

Dynamic product columns allow **unlimited** product definitions:
- Use `product_1`, `product_2`, `product_3`, `product_4`, `product_5`, etc. (unlimited)
- Each product creates a `product_{product_id}` group
- Hosts can have 1 to N products (where N is unlimited)
- No code changes required for new products
- Product columns should be sequential (product_1, product_2, product_3, etc.)

Example:
```csv
hostname,environment,product_1,product_2,product_3,product_4,product_5
web01,production,web,monitoring,analytics,cdn,ssl
api01,production,api,logging,cache,load_balancer,
db01,production,database,backup,monitoring,replication,
```

### What is the group_path field?

The `group_path` field is currently **reserved for future use** but is not actively used in inventory generation.

**Current Status:**
- ✅ Field is accepted in CSV files
- ✅ Field is preserved during processing
- ❌ Field does not create inventory groups
- ❌ Field is not included in host_vars
- ❌ Field does not affect inventory structure

**Future Plans:**
- May be used for hierarchical group organization
- May create nested group structures
- May be used for organizational grouping

You can include this field in your CSV for organizational purposes, but it won't affect the generated inventory structure.

### How do extra variables work?

Any CSV column not in the standard field list becomes an extra variable:
- Automatically included in host_vars files
- Accessible in Ansible playbooks
- Preserved during processing
- No configuration required

Example:
```csv
hostname,environment,custom_role,monitoring_level
web01,production,frontend,high
api01,production,backend,medium
```

These become available in Ansible as `{{ custom_role }}` and `{{ monitoring_level }}`.

### What validation does the system perform?

The system validates:
- Required fields are present
- Environment values are valid
- Status values are valid
- Data types (integers, dates)
- Product consistency
- CSV structure integrity

## Configuration Questions

### How do I configure the system?

Copy `inventory-config.yml.example` to `inventory-config.yml` and customize:
- Environment settings
- Field mappings
- Group naming patterns
- Feature flags
- File paths

See the [Configuration Guide](configuration.md) for details.

### Can I use environment variables?

Yes, you can override any configuration value:
```bash
export INVENTORY_CSV_FILE="/path/to/custom/hosts.csv"
export INVENTORY_LOG_LEVEL="DEBUG"
export INVENTORY_KEY="cname"
```

### How do I add new environments?

1. Add to the supported environments list in config
2. Add environment code mapping
3. Add grace period if needed
4. Create environment group_vars file

## Usage Questions

### What are the basic commands?

```bash
# Generate inventory
make generate

# Validate structure
make validate

# Health check
make health-check

# Dry run
make generate-dry-run
```

### How do I use the Makefile?

The Makefile provides convenient shortcuts for all operations:
- `make help` - Show all commands
- `make generate` - Generate inventory
- `make validate` - Validate structure
- `make test` - Run tests
- `make lint` - Code quality checks

See the [Makefile Reference](makefile.md) for complete documentation.

### How do I test my inventory?

```bash
# Validate with Ansible
make validate

# List all hosts
ansible-inventory -i inventory/production.yml --list

# Show inventory structure
ansible-inventory -i inventory/production.yml --graph

# List hosts in group
ansible-inventory -i inventory/production.yml --list-hosts app_web_server
```

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
4. **Run validation**: Use `make validate`

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
1. **Host status**: Only active hosts are included in inventory
2. **Environment filtering**: Ensure hosts have correct environment values
3. **Required fields**: Check that required fields are populated
4. **Validation errors**: Run `make validate` to check for issues

### Makefile command not found

**Q: I'm getting "command not found" for make commands.**

A: Solutions:
1. **Install make**: `sudo apt-get install make` (Ubuntu/Debian) or `sudo yum install make` (RHEL/CentOS)
2. **Check Makefile**: Ensure Makefile is in the project root
3. **Check permissions**: Ensure Makefile is executable
4. **Use direct commands**: Use Python commands directly if make is unavailable

## Advanced Questions

### How do I import existing inventory?

```bash
# Test import (dry run)
make import-dry-run INVENTORY_FILE=/path/to/inventory.yml

# Import with host_vars
make import-inventory INVENTORY_FILE=/path/to/inventory.yml HOST_VARS_DIR=/path/to/host_vars/

# Get import help
make import-help
```

### How do I customize group naming?

Configure group prefixes in `inventory-config.yml`:
```yaml
groups:
  prefixes:
    application: "app_"
    product: "product_"
    environment: "env_"
    custom: "custom_"  # Add new prefix
```

### How do I add custom validation?

1. Extend the validation logic in `scripts/core/utils.py`
2. Add custom validation functions
3. Update the validation command to include your checks
4. Test with `make validate`

### How do I integrate with CI/CD?

```yaml
# .gitlab-ci.yml example
stages:
  - validate
  - generate
  - test

validate_inventory:
  stage: validate
  script:
    - make validate

generate_inventory:
  stage: generate
  script:
    - make generate
  artifacts:
    paths:
      - inventory/

test_inventory:
  stage: test
  script:
    - make health-check
```

## Performance Questions

### How does the system handle large inventories?

The system is optimized for:
- Efficient CSV parsing
- Minimal memory usage
- Fast inventory generation
- Scalable group creation

For very large inventories (>10,000 hosts), consider:
- Using database backends
- Implementing caching
- Optimizing CSV structure

### How can I improve performance?

1. **Optimize CSV**: Remove unnecessary columns
2. **Use efficient data types**: Use integers instead of strings where possible
3. **Limit extra variables**: Only include necessary extra variables
4. **Use dry runs**: Test changes before full generation

## Security Questions

### How secure is the system?

The system includes several security features:
- Input validation
- File permission checks
- Safe file operations
- Security scanning with bandit
- No arbitrary code execution

### How do I handle sensitive data?

1. **Use environment variables** for sensitive configuration
2. **Store secrets** in external secret management systems
3. **Use Ansible vault** for sensitive host variables
4. **Implement access controls** on CSV files

## Exit Codes

- **0**: Success
- **1**: Command error (validation failed, invalid input)
- **2**: File not found
- **3**: Unexpected error

## Getting Help

### Documentation
- Check the [CSV Format Reference](csv_format.md)
- Review the [Configuration Guide](configuration.md)
- Read the [Usage Guide](usage.md)
- Consult the [FAQ](docs/faq.md)

### Support Resources
- Use built-in validation tools
- Check error messages carefully
- Review logs for detailed information
- Test with minimal examples

---

**Need more help?** Check the [FAQ](docs/faq.md) for common questions or review the [Configuration Guide](configuration.md) for advanced configuration options.
