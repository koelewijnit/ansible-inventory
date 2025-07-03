# Ansible Inventory Management System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Ansible 2.9+](https://img.shields.io/badge/ansible-2.9+-red.svg)](https://docs.ansible.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A powerful, flexible tool for managing Ansible inventories from CSV data with support for dynamic product columns, extra variables, and comprehensive lifecycle management.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/ansible-inventory-cli.git
cd ansible-inventory-cli

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy configuration
cp inventory-config.yml.example inventory-config.yml

# Generate inventory from CSV
python3 scripts/ansible_inventory_cli.py generate
```

## ✨ Key Features

### 🔄 Dynamic Product Columns
- **Flexible Product Definitions**: Use `product_1`, `product_2`, `product_3`, etc.
- **Multiple Products per Host**: Hosts can belong to multiple product groups
- **Automatic Group Creation**: Each product creates a `product_{product_id}` group
- **No CSV Parsing Issues**: Unlike comma-separated values, no quoting problems

### 📊 Extra Variables (Metadata)
- **Automatic Detection**: Any CSV column not in the standard list becomes an extra variable
- **Host Metadata**: Automatically stored in host_vars files
- **Ansible Integration**: Accessible in playbooks and inventory queries
- **No Configuration Required**: Works out of the box

### 🏗️ Comprehensive Group Structure
- **Application Groups**: `app_web_server`, `app_api_server`
- **Product Groups**: `product_web`, `product_api`, `product_analytics`
- **Environment Groups**: `env_production`, `env_development`
- **Site Groups**: `site_use1`, `site_usw2`
- **Dashboard Groups**: `dashboard_web_servers`

### 🔧 Enterprise Features
- **Patch Management**: Batch windows and scheduling
- **Lifecycle Management**: Decommission date handling
- **Health Monitoring**: System health checks
- **Validation**: Comprehensive data validation
- **Backup Support**: Automatic CSV backups

## 📚 Documentation

- **[📖 Documentation Index](docs/index.md)** - Complete documentation overview
- **[📋 CSV Format Reference](docs/csv_format.md)** - CSV structure and columns
- **[⚙️ Configuration Guide](docs/configuration.md)** - System configuration
- **[🛠️ Usage Guide](docs/usage.md)** - Command reference and examples
- **[❓ FAQ](docs/faq.md)** - Frequently asked questions

## 📊 CSV Structure

The system supports a flexible CSV structure:

### Required Columns
```csv
hostname,environment,status
prd-web-01,production,active
dev-api-01,development,active
```

### Full Example with Dynamic Products
```csv
hostname,environment,status,application_service,product_1,product_2,custom_role,monitoring_level
prd-web-01,production,active,web_server,web,analytics,load_balancer,high
prd-api-01,production,active,api_server,api,monitoring,api_gateway,high
prd-db-01,production,active,database_server,db,,database_server,critical
```

## 🛠️ Core Commands

### Basic Operations
```bash
# Generate inventory
python3 scripts/ansible_inventory_cli.py generate

# Validate CSV data
python3 scripts/ansible_inventory_cli.py validate

# Check system health
python3 scripts/ansible_inventory_cli.py health
```

### Advanced Operations
```bash
# Generate specific environments
python3 scripts/ansible_inventory_cli.py generate --environments production test

# Use custom CSV file
python3 scripts/ansible_inventory_cli.py --csv-file custom.csv generate

# Lifecycle management
python3 scripts/ansible_inventory_cli.py lifecycle list-expired
python3 scripts/ansible_inventory_cli.py lifecycle cleanup
```

## 🎯 Ansible Integration

### Generated Inventory Structure
```yaml
# inventory/production.yml
app_web_server:
  children:
    product_web: {}
    product_analytics: {}
  hosts:
    prd-web-01: {}

app_api_server:
  children:
    product_api: {}
    product_monitoring: {}
  hosts:
    prd-api-01: {}
```

### Using with Ansible
```bash
# List all web servers
ansible-inventory -i inventory/production.yml --list-hosts app_web_server

# Show host variables
ansible-inventory -i inventory/production.yml --host prd-web-01

# Run playbook on specific group
ansible-playbook playbook.yml -i inventory/production.yml --limit product_web
```

### Accessing Extra Variables in Playbooks
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

## 🔧 Configuration

The system is highly configurable through `inventory-config.yml`:

```yaml
# Example configuration
environments:
  supported: [production, development, test, acceptance]

hosts:
  inventory_key: "hostname"  # or "cname"
  grace_periods:
    production: 90
    development: 7

features:
  patch_management: true
  lifecycle_management: true
  cleanup_orphaned_on_generate: true
```

## 🚀 Getting Started

1. **Install Dependencies**: See [Installation Guide](docs/installation.md)
2. **Configure System**: See [Configuration Guide](docs/configuration.md)
3. **Prepare CSV**: See [CSV Format Reference](docs/csv_format.md)
4. **Generate Inventory**: See [Usage Guide](docs/usage.md)
5. **Test with Ansible**: Use generated inventory files

## 📈 Use Cases

### Infrastructure Management
- **Multi-environment deployments**: Production, development, test, acceptance
- **Product-based grouping**: Organize hosts by installed products
- **Site-based organization**: Group by physical location
- **Application-based targeting**: Target specific application types

### Automation Workflows
- **Patch management**: Batch-based patching schedules
- **Monitoring setup**: Dashboard group assignments
- **Security compliance**: Security tier classifications
- **Backup management**: Retention period configuration

### DevOps Integration
- **CI/CD pipelines**: Automated inventory generation
- **Configuration management**: Dynamic host configuration
- **Monitoring integration**: Health check automation
- **Lifecycle management**: Automated host cleanup

## 🏗️ Project Structure

```
ansible-inventory-cli/
├── docs/                          # Documentation
│   ├── index.md                   # Main documentation index
│   ├── csv_format.md              # CSV format reference
│   ├── configuration.md           # Configuration guide
│   ├── usage.md                   # Usage guide
│   └── faq.md                     # Frequently asked questions
├── scripts/                       # Main application
│   ├── ansible_inventory_cli.py   # Main CLI entry point
│   ├── core/                      # Core functionality
│   ├── commands/                  # CLI commands
│   └── managers/                  # Business logic managers
├── inventory_source/              # CSV data source
│   └── hosts.csv                  # Host definitions
├── inventory/                     # Generated inventory
│   ├── production.yml             # Production environment
│   ├── development.yml            # Development environment
│   ├── host_vars/                 # Host-specific variables
│   └── group_vars/                # Group-specific variables
├── inventory-config.yml           # Configuration file
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing.md) for details on:
- Code style and standards
- Testing requirements
- Pull request process
- Development setup

## 📞 Support

For support and questions:
1. Check the [FAQ](docs/faq.md)
2. Review the [documentation](docs/index.md)
3. Search existing issues
4. Create a new issue with details

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for the Ansible community
- Inspired by real-world infrastructure management needs
- Designed for flexibility and extensibility

---

**Ready to get started?** Begin with the [Installation Guide](docs/installation.md) or jump straight to the [CSV Format Reference](docs/csv_format.md) to understand the data structure.
