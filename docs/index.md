# Ansible Inventory Management Documentation

Welcome to the comprehensive documentation for the Ansible Inventory Management System. This system provides automated inventory generation from CSV data with support for dynamic product columns, extra variables, and advanced Ansible integration.

## 🚀 Quick Start for New Users

**New to the system? Start here:**

1. **[Getting Started Guide](getting-started.md)** - Complete step-by-step tutorial for new users
2. **[Quick Reference](QUICK_REFERENCE.md)** - Essential commands and examples
3. **[User Guide](USER_GUIDE.md)** - Comprehensive user manual

## 📚 Core Documentation

### [Getting Started Guide](getting-started.md) ⭐ **NEW USERS START HERE**
Complete tutorial covering:
- Installation and setup
- Creating your first CSV file
- Setting up group variables
- Generating your first inventory
- Testing and validation
- Common scenarios and examples

### [CSV Format Reference](csv_format.md)
Complete reference for CSV file format, including:
- Required and optional fields
- Dynamic product columns (product_1, product_2, etc.) - **unlimited support**
- Extra variables support

- Host variables vs group variables
- Step-by-step group_vars setup

### [Configuration Guide](configuration.md)
Detailed configuration options:
- Environment settings
- Field mappings
- Group naming patterns
- Feature flags
- Environment variable overrides
- Common customizations

### [Usage Guide](usage.md)
How to use the system effectively:
- Basic commands
- Advanced targeting
- Playbook integration
- Best practices
- Troubleshooting

### [Makefile Reference](makefile.md)
Complete reference for all Makefile commands:
- Inventory management shortcuts
- Development commands
- Testing and validation
- CI/CD integration

## 🔧 Reference Documentation

### [FAQ](faq.md)
Common questions and answers:
- General questions about the system
- CSV and data questions
- Configuration questions
- Usage questions
- Troubleshooting questions

### [User Guide](USER_GUIDE.md)
Comprehensive user manual with:
- Detailed explanations
- Advanced examples
- Best practices
- Real-world scenarios

## 🎯 Key Features

### Dynamic Product Support
- **Unlimited** product definitions using `product_1`, `product_2`, etc.
- Automatic group creation for each product
- Support for hosts with 1 to N products (unlimited)
- No code changes required for new products

### Extra Variables
- Any CSV column becomes an Ansible variable
- Automatically included in host_vars files
- Accessible in Ansible playbooks
- No configuration required

### Automatic Grouping
- Environment groups (`env_production`, `env_development`, etc.)
- Application groups (`app_web_server`, `app_api_server`, etc.)
- Product groups (`product_web`, `product_api`, etc.)
- Site groups (`site_use1`, `site_usw2`, etc.)
- Dashboard groups (`dashboard_web_servers`, etc.)

### Advanced Features
- **Validation**: Comprehensive data validation and health checks
- **Lifecycle Management**: Handles host decommissioning and cleanup
- **Makefile Integration**: Convenient commands for all operations
- **CI/CD Ready**: Designed for automated deployment

## 🛠️ Quick Commands

```bash
# Generate inventory
make generate

# Validate structure
make validate

# Health check
make health-check

# Show all commands
make help
```

## 📖 Learning Path

### For New Users
1. **Start with** [Getting Started Guide](getting-started.md)
2. **Review** [Quick Reference](QUICK_REFERENCE.md)
3. **Explore** [CSV Format Reference](csv_format.md)
4. **Customize** [Configuration Guide](configuration.md)

### For Experienced Users
1. **Review** [Usage Guide](usage.md)
2. **Check** [Makefile Reference](makefile.md)
3. **Explore** [User Guide](USER_GUIDE.md)
4. **Reference** [FAQ](faq.md) for specific questions

### For Administrators
1. **Study** [Configuration Guide](configuration.md)
2. **Review** [User Guide](USER_GUIDE.md)
3. **Check** [Makefile Reference](makefile.md) for CI/CD integration
4. **Explore** advanced features in [Usage Guide](usage.md)

## 🔍 Finding What You Need

### By Task
- **Setting up**: [Getting Started Guide](getting-started.md)
- **Configuring**: [Configuration Guide](configuration.md)
- **Using**: [Usage Guide](usage.md)
- **Troubleshooting**: [FAQ](faq.md)

### By Experience Level
- **Beginner**: [Getting Started Guide](getting-started.md) → [Quick Reference](QUICK_REFERENCE.md)
- **Intermediate**: [Usage Guide](usage.md) → [User Guide](USER_GUIDE.md)
- **Advanced**: [Configuration Guide](configuration.md) → [Makefile Reference](makefile.md)

### By Feature
- **CSV format**: [CSV Format Reference](csv_format.md)
- **Group variables**: [CSV Format Reference](csv_format.md#group-variables-group_vars)
- **Product columns**: [CSV Format Reference](csv_format.md#dynamic-product-columns)
- **Extra variables**: [CSV Format Reference](csv_format.md#extra-variables)
- **Makefile**: [Makefile Reference](makefile.md)

## 📞 Getting Help

### Documentation
- **Start here**: [Getting Started Guide](getting-started.md)
- **Quick answers**: [FAQ](faq.md)
- **Command reference**: [Quick Reference](QUICK_REFERENCE.md)

### System Commands
```bash
# Get help for any command
python scripts/ansible_inventory_cli.py --help

# Validate your setup
python scripts/ansible_inventory_cli.py validate

# Check system health
python scripts/ansible_inventory_cli.py health

# Show all Makefile commands
make help
```

### Common Issues
- **CSV parsing errors**: Check [CSV Format Reference](csv_format.md)
- **Missing group_vars**: See [Getting Started Guide](getting-started.md#step-4-create-group-variables-files)
- **Configuration issues**: Review [Configuration Guide](configuration.md)
- **Targeting problems**: Check [Usage Guide](usage.md#advanced-targeting)

## 🎉 Welcome!

You're now ready to start using the Ansible Inventory Management System. Whether you're a beginner or an experienced user, this documentation will guide you through every aspect of the system.

**Happy automating!** 🚀
