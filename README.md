# Simplified Ansible Inventory with Batch Groups

[![Ansible 2.9+](https://img.shields.io/badge/ansible-2.9+-red.svg)](https://docs.ansible.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A simplified tool for creating Ansible inventories from CSV data using Ansible's native `constructed` plugin with automatic batch grouping.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/ansible-inventory-cli.git
cd ansible-inventory-cli

# Install dependencies (minimal)
pip install pyyaml

# Convert your CSV to inventory
python simple_csv_converter.py

# Use with Ansible
ansible-inventory -i inventory/constructed.yml --list-hosts batch_1
```

## ✨ Key Features

### 🎯 Automatic Batch Groups
- **Batch Groups**: Automatically creates `batch_1`, `batch_2`, `batch_3` based on `batch_number` column
- **Environment Groups**: `env_production`, `env_development`, `env_test`
- **Application Groups**: `app_web_server`, `app_api_server`, `app_database_server`
- **Product Groups**: `product_web`, `product_api`, `product_db`
- **Site Groups**: `site_us_east_1`, etc.

### 🔧 Simple & Powerful
- **Uses Ansible's Native Features**: Leverages `constructed` plugin with `keyed_groups`
- **Minimal Code**: ~150 lines vs 3000+ lines in complex systems
- **Better Performance**: Ansible's optimized C code handles grouping
- **Easy to Extend**: Add new groups with simple YAML configuration

### 📊 Flexible CSV Support
```csv
hostname,environment,status,application_service,product_1,batch_number,site_code
test-web-01,production,active,web_server,web,1,us-east-1
test-api-01,production,active,api_server,api,2,us-east-1
test-db-01,production,active,database_server,db,3,us-east-1
```

## 🛠️ Usage

### Convert CSV to Inventory
```bash
# Convert your CSV file
python simple_csv_converter.py
```

### Use with Ansible
```bash
# List hosts in batch_1
ansible-inventory -i inventory/constructed.yml --list-hosts batch_1

# List hosts in batch_2
ansible-inventory -i inventory/constructed.yml --list-hosts batch_2

# Run playbook on specific batch
ansible-playbook -i inventory/constructed.yml playbook.yml --limit batch_1

# Run on production batch_2 hosts only
ansible-playbook -i inventory/constructed.yml playbook.yml --limit production_batch_2

# Show inventory structure
ansible-inventory -i inventory/constructed.yml --graph
```

## 📁 Project Structure

```
ansible-inventory-cli/
├── inventory_source/
│   └── sample_hosts.csv           # Your CSV data
├── inventory/
│   ├── constructed.yml            # Ansible constructed plugin config
│   ├── hosts.yml                  # Simple base inventory
│   ├── host_vars/                 # Individual host variables
│   └── USAGE.md                   # Detailed usage examples
├── simple_csv_converter.py        # Main conversion tool
├── requirements.txt               # Python dependencies (just PyYAML)
└── README.md                      # This file
```

## 🎯 How It Works

### 1. CSV to Host Variables
The converter reads your CSV and creates individual `host_vars` files:
```yaml
# inventory/host_vars/test-web-01.yml
---
hostname: test-web-01
environment: production
batch_number: '1'
application_service: web_server
product_1: web
```

### 2. Ansible Creates Groups Automatically
The `constructed.yml` configuration tells Ansible to create groups:
```yaml
keyed_groups:
  - key: batch_number
    prefix: batch
    separator: "_"
```

### 3. Result: Dynamic Groups
Ansible automatically creates:
- `batch_1` - All hosts with batch_number: 1
- `batch_2` - All hosts with batch_number: 2  
- `batch_3` - All hosts with batch_number: 3
- Plus environment, application, product, and site groups

## 📊 Sample CSV Format

```csv
hostname,environment,status,application_service,product_1,batch_number,site_code,cname
test-web-01,production,active,web_server,web,1,us-east-1,test-web-01.example.com
test-api-01,production,active,api_server,api,2,us-east-1,test-api-01.example.com
test-db-01,production,active,database_server,db,3,us-east-1,test-db-01.example.com
dev-web-01,development,active,web_server,web,1,us-east-1,dev-web-01.example.com
dev-api-01,development,active,api_server,api,2,us-east-1,dev-api-01.example.com
```

## 🔧 Customization

### Add New Groups
Edit `inventory/constructed.yml` to add new grouping:
```yaml
keyed_groups:
  # Add custom groups based on any CSV column
  - key: environment
    prefix: env
  - key: custom_field
    prefix: custom
    
groups:
  # Add conditional groups
  critical_servers: batch_number == "3" and environment == "production"
  web_cluster: application_service == "web_server" and status == "active"
```

### Supported Group Types
- **keyed_groups**: Automatic groups based on host variables
- **groups**: Conditional groups using Jinja2 expressions  
- **compose**: Create computed variables

## 🚀 Migration from Complex Systems

This simplified approach provides the same functionality as complex inventory management systems:

| Feature | Complex System | Simplified System |
|---------|---------------|-------------------|
| Batch Groups | ✅ 50+ lines Python | ✅ 3 lines YAML |
| Environment Groups | ✅ Custom logic | ✅ keyed_groups |
| Performance | Slow (Python) | Fast (Ansible native) |
| Maintenance | High | Minimal |
| Flexibility | Limited | High |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Why This Approach?

- **95% Less Code**: Simple converter + Ansible native features
- **Better Performance**: Ansible's optimized code handles grouping
- **More Maintainable**: Standard Ansible patterns, community supported
- **Future Proof**: Compatible with all Ansible updates
- **Same Results**: Batch groups work exactly like complex systems

---

**Ready to simplify your inventory management?** Run `python simple_csv_converter.py` and start using batch groups immediately!
