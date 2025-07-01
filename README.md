# Ansible Inventory Management System

Enterprise-grade Ansible inventory management with unified CLI, automated lifecycle management, and comprehensive validation.

## 🆕 **New User? Start Here!**

**Want to add a new system to the inventory?** 
👉 **[Simple Guide: Adding New Systems](docs/ADDING_SYSTEMS.md)**

This guide walks you through the complete workflow:
1. Add system to CSV → 2. Generate inventory → 3. Commit to git → 4. Push changes

## 🚀 **Quick Start**

```bash
# 1. Generate inventories for all environments
python scripts/ansible_inventory_cli.py generate

# 2. Check system health
python scripts/ansible_inventory_cli.py health

# 3. Validate configuration
python scripts/ansible_inventory_cli.py validate

# 4. Get help for any command
python scripts/ansible_inventory_cli.py --help
```

## ✨ **Features**

- **🎯 Unified CLI**: Single tool for all inventory operations
- **📊 Health Monitoring**: Real-time health scoring with recommendations
- **🔄 Lifecycle Management**: Automated host decommissioning and cleanup
- **✅ Validation**: Infrastructure and configuration validation
- **🏗️ Template Creation**: Clean repository templates
- **📋 CSV-Driven**: Flexible CSV-based host definitions
- **🚀 Enterprise Ready**: JSON output, logging, error handling
- **⚡ High Performance**: Sub-second operations

## 📁 **Project Structure**

```
ansible-inventory/
├── scripts/
│   ├── ansible_inventory_cli.py    # 🎯 Main CLI tool
│   ├── config.py                   # 📋 Configuration
│   ├── utils.py                    # 🔧 Utilities
│   └── models.py                   # 📊 Data models
├── inventory_source/
│   └── hosts.csv                   # 📝 Host data (CSV format)
├── inventory/                      # 📂 Generated inventories
│   ├── group_vars/                 # 🏷️ Group variables
│   └── host_vars/                  # 🖥️ Host variables
└── README.md                       # 📚 This file
```

## 🔧 **Installation & Setup**

1. **Prerequisites**: Python 3.7+, PyYAML
2. **Make executable**: `chmod +x scripts/ansible_inventory_cli.py`
3. **Optional alias**: `alias inventory-cli='python scripts/ansible_inventory_cli.py'`

## 📋 **Core Commands**

### **Generate Inventories**
```bash
# Generate all environments
python scripts/ansible_inventory_cli.py generate

# Generate specific environments
python scripts/ansible_inventory_cli.py generate --environments production test

# Custom output directory
python scripts/ansible_inventory_cli.py generate --output-dir custom_inventory
```

### **Health Monitoring**
```bash
# Check inventory health
python scripts/ansible_inventory_cli.py health

# JSON output for automation
python scripts/ansible_inventory_cli.py --output-format json health
```

### **Infrastructure Validation**
```bash
# Validate structure and configuration
python scripts/ansible_inventory_cli.py validate

# Debug mode
python scripts/ansible_inventory_cli.py --log-level DEBUG validate
```

### **Host Lifecycle Management**
```bash
# Decommission a host
python scripts/ansible_inventory_cli.py lifecycle decommission \
  --hostname server-01 --date 2025-12-31

# List expired hosts
python scripts/ansible_inventory_cli.py lifecycle list-expired

# Cleanup expired hosts
python scripts/ansible_inventory_cli.py lifecycle cleanup --dry-run
```

### **Template Creation**
```bash
# Preview template creation
python scripts/ansible_inventory_cli.py template --preview

# Create clean template repository
python scripts/ansible_inventory_cli.py template --force
```

## 📊 **CSV Format**

Your `inventory_source/hosts.csv` should include these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `hostname` | Unique hostname | `prd-web-01` |
| `environment` | Environment name | `production` |
| `status` | Host status | `active`, `decommissioned` |
| `application_service` | Service type | `web_server`, `database` |
| `product_id` | Product identifier | `apache_httpd`, `postgresql` |
| `location` | Geographic location | `us-east-1`, `europe` |
| `batch_number` | Patch batch | `batch_1`, `batch_2` |
| `patch_mode` | Patching mode | `manual`, `auto` |

Additional fields for CMDB integration: `primary_application`, `function`, `dashboard_group`, `ssl_port`, `cname`, `decommission_date`

## 🎯 **Group Targeting**

The system generates both functional and product-specific groups:

### **Application Service Groups**
Target hosts by function across all products:

```bash
# All web servers (Apache + Nginx + others)
ansible app_web_server -i inventory/production.yml --list-hosts

# All databases (PostgreSQL + MongoDB + others)
ansible app_database -i inventory/production.yml --list-hosts

# All identity management systems
ansible app_identity_management -i inventory/production.yml --list-hosts
```

### **Product-Specific Groups**
Target hosts by specific software:

```bash
# Only Apache HTTP servers
ansible product_apache_httpd -i inventory/production.yml --list-hosts

# Only PostgreSQL databases
ansible product_postgresql -i inventory/production.yml --list-hosts

# Only Kubernetes infrastructure
ansible product_kubernetes -i inventory/production.yml --list-hosts
```

## 🔄 **Common Workflows**

### **Daily Operations**
```bash
# 1. Check system health
python scripts/ansible_inventory_cli.py health

# 2. Generate updated inventories
python scripts/ansible_inventory_cli.py generate

# 3. Validate configuration
python scripts/ansible_inventory_cli.py validate
```

### **Host Decommissioning**
```bash
# 1. Mark host as decommissioned
python scripts/ansible_inventory_cli.py lifecycle decommission \
  --hostname old-server-01 --date 2025-12-31

# 2. Regenerate inventories
python scripts/ansible_inventory_cli.py generate

# 3. Verify health
python scripts/ansible_inventory_cli.py health
```

### **Maintenance Operations**
```bash
# 1. Check for expired hosts
python scripts/ansible_inventory_cli.py lifecycle list-expired

# 2. Preview cleanup
python scripts/ansible_inventory_cli.py lifecycle cleanup --dry-run

# 3. Perform cleanup
python scripts/ansible_inventory_cli.py lifecycle cleanup
```

## ⚙️ **Configuration**

### **Global Options**
- `--csv-file`: Custom CSV data source
- `--output-format`: text (default) or json
- `--log-level`: DEBUG, INFO, WARNING, ERROR

### **Environment Variables**
The system supports configuration through `scripts/config.py` for:
- Default paths and directories
- Environment definitions
- Grace periods for cleanup
- Patch management windows

## 🚀 **Enterprise Features**

- **JSON Output**: Machine-readable output for automation and CI/CD
- **Comprehensive Logging**: Configurable logging levels with structured output
- **Error Handling**: Proper exit codes and detailed error messages
- **Performance**: Sub-second operations for typical workloads
- **Type Safety**: Full type hints and validation throughout
- **Health Scoring**: 0-100% health scores with actionable recommendations

## 📖 **Documentation**

- **USER_GUIDE.md**: Complete user documentation with examples
- **MIGRATION.md**: Migration guide from older script-based systems
- **scripts/archive/**: Historical documentation and implementation details

## 🛡️ **Production Ready**

This system is designed for enterprise use with:
- Comprehensive error handling and recovery
- Performance monitoring (sub-second generation times)
- Backup and rollback capabilities
- Extensive logging and audit trails
- Type-safe data models and validation

## 🤝 **Contributing**

1. Follow the existing code structure and patterns
2. Add comprehensive type hints
3. Include proper error handling
4. Update documentation for any changes
5. Test thoroughly with various CSV formats

---

**Version**: 4.0.0  
**Status**: Production Ready  
**Team**: Infrastructure as Code Team
