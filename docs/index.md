# Ansible Inventory Management Documentation

Welcome to the comprehensive documentation for the Ansible Inventory Management System. This system provides automated inventory generation from CSV data with support for dynamic product columns, extra variables, and advanced Ansible integration.

## Quick Start

1. **Install**: `make install-dev`
2. **Configure**: Copy `inventory-config.yml.example` to `inventory-config.yml`
3. **Prepare CSV**: Create `inventory_source/hosts.csv` with your host data
4. **Generate**: `make generate`
5. **Validate**: `make validate`

## Core Documentation

### [CSV Format Reference](csv_format.md)
Complete reference for CSV file format, including:
- Required and optional fields
- Dynamic product columns (product_1, product_2, etc.)
- Extra variables support
- Reserved fields (group_path)
- Data validation rules
- Best practices and examples

### [Configuration Guide](configuration.md)
Comprehensive configuration options:
- Environment setup
- Field mappings
- Group naming patterns
- Feature flags
- Environment variable overrides
- Customization examples

### [Usage Guide](usage.md)
Step-by-step usage instructions:
- Basic commands
- Advanced features
- Ansible integration
- Troubleshooting
- Best practices

### [Makefile Reference](makefile.md)
Complete reference for all Makefile commands:
- Inventory management commands
- Development and testing commands
- CI/CD integration
- Utility commands
- Best practices and workflows

## Reference Documentation

### [Ansible Inventory](ansible_inventory.md)
Generated inventory structure and usage:
- Inventory file format
- Group hierarchy
- Host variables
- Ansible integration examples

### [FAQ](faq.md)
Common questions and answers:
- Troubleshooting
- Configuration issues
- Best practices
- Advanced usage

## Legacy Documentation

### [Legacy Documentation](legacy/)
Historical documentation for reference:
- [Getting Started](legacy/getting-started/)
- [Development](legacy/development/)
- [Operations](legacy/operations/)
- [Reference](legacy/reference/)

## Key Features

### Dynamic Product Support
- **Unlimited** product definitions using `product_1`, `product_2`, etc.
- Automatic group creation for each product
- Support for hosts with 1 to N products (unlimited)
- No code changes required for new products

### Extra Variables
- Any CSV column becomes an Ansible variable
- Automatic inclusion in host_vars files
- Accessible in playbooks and inventory queries
- Preserved during processing

### Reserved Fields
- `group_path`: Reserved for future hierarchical organization
- Currently accepted but not used in inventory generation
- Future plans for nested group structures

### Advanced Features
- Automatic orphaned file cleanup
- Comprehensive validation
- Health monitoring
- Backup and recovery
- External inventory import

## Command Reference

### Core Commands
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

### Development Commands
```bash
# Install dependencies
make install-dev

# Run tests
make test

# Code quality
make lint
make format

# Security checks
make security
```

### CI/CD Commands
```bash
# CI installation
make ci-install

# CI testing
make ci-test

# CI linting
make ci-lint
```

## File Structure

```
inventory-structure-new/
├── inventory_source/
│   └── hosts.csv              # Source CSV file
├── inventory/
│   ├── production.yml         # Generated inventory files
│   ├── development.yml
│   ├── test.yml
│   ├── acceptance.yml
│   ├── host_vars/            # Host-specific variables
│   └── group_vars/           # Group variables
├── scripts/                   # Core application code
├── docs/                      # Documentation
├── tests/                     # Test suite
├── Makefile                   # Build and utility commands
├── inventory-config.yml       # Configuration
└── README.md                  # Project overview
```

## Getting Help

### Documentation
- Start with the [CSV Format Reference](csv_format.md)
- Review the [Configuration Guide](configuration.md)
- Check the [Usage Guide](usage.md) for examples
- Consult the [FAQ](faq.md) for common issues

### Commands
```bash
# Show all Makefile commands
make help

# Validate your setup
make validate

# Check system health
make health-check

# Get command help
python scripts/ansible_inventory_cli.py --help
```

### Support
- Check error messages carefully
- Review logs for detailed information
- Use dry-run commands to test changes
- Validate after any modifications

## Version Information

- **Current Version**: 4.0.0
- **Status**: Production Ready
- **Python**: 3.8+
- **Ansible**: 2.9+

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines and contribution information.

---

**Need help?** Start with the [Quick Start Guide](usage.md#quick-start) or check the [FAQ](faq.md) for common questions.
