# Quick Reference Guide

Essential commands, examples, and patterns for the Ansible Inventory Management System.

## 🚀 Essential Commands

### Basic Operations
```bash
# Generate inventory from CSV
make generate

# Validate CSV data
make validate

# Health check
make health-check

# Show all available commands
make help
```

### Direct CLI Commands
```bash
# Generate inventory
python scripts/ansible_inventory_cli.py generate

# Generate specific environments
python scripts/ansible_inventory_cli.py generate --environments production test

# Validate data
python scripts/ansible_inventory_cli.py validate

# Health check
python scripts/ansible_inventory_cli.py health

# Dry run (see what would be generated)
python scripts/ansible_inventory_cli.py generate --dry-run
```

## 📊 CSV Format Quick Reference

### Required Fields
```csv
hostname,environment,status
web01,production,active
api01,production,active
```

### Complete Example
```csv
hostname,environment,status,cname,instance,site_code,ssl_port,application_service,product_1,product_2,product_3,product_4,batch_number,patch_mode,dashboard_group,primary_application,function,decommission_date,custom_role,monitoring_level
web01,production,active,web01.example.com,1,use1,443,web_server,web,monitoring,,,1,auto,web_servers,wordpress,frontend,,frontend,high
api01,production,active,api01.example.com,1,use1,8443,api_server,api,logging,cache,,2,auto,api_servers,django,backend,,backend,medium
db01,production,active,db01.example.com,1,use1,,database_server,database,backup,,,3,manual,database_servers,postgresql,database,,primary,high
```

### Field Types
| Field | Type | Required | Example |
|-------|------|----------|---------|
| `hostname` | Text | ⚠️ Conditional | `web01` |
| `cname` | Text | ⚠️ Conditional | `web01.example.com` |
| `environment` | Text | ✅ Required | `production` |
| `status` | Text | ✅ Required | `active` |
| `application_service` | Text | ❌ Optional | `web_server` |
| `product_1`, `product_2`, etc. | Text | ❌ Optional | `web`, `api` |
| `site_code` | Text | ❌ Optional | `use1` |
| `custom_role` | Text | ❌ Extra Variable | `frontend` |

## 🎯 Ansible Targeting Examples

### Basic Group Targeting
```bash
# Target all web servers
ansible app_web_server -i inventory/production.yml --list-hosts

# Target all production hosts
ansible env_production -i inventory/production.yml --list-hosts

# Target hosts with web product
ansible product_web -i inventory/production.yml --list-hosts

# Target hosts in use1 site
ansible site_use1 -i inventory/production.yml --list-hosts

# Target hosts by batch number for controlled deployments
ansible batch_1 -i inventory/production.yml --list-hosts
ansible batch_2 -i inventory/production.yml --list-hosts
ansible batch_3 -i inventory/production.yml --list-hosts
```

### Complex Targeting
```bash
# Production web servers in use1 site
ansible-playbook deploy.yml -i inventory/production.yml \
  --limit "env_production:&site_use1:&app_web_server"

# Hosts with monitoring product across all environments
ansible-playbook monitoring.yml -i inventory/production.yml \
  --limit "product_monitoring"

# Development hosts with auto patch mode
ansible-playbook patch.yml -i inventory/development.yml \
  --limit "env_development" \
  --extra-vars "patch_mode=auto"

# Staged deployment by batch (rolling deployment pattern)
ansible-playbook deploy.yml -i inventory/production.yml --limit batch_1
ansible-playbook deploy.yml -i inventory/production.yml --limit batch_2
ansible-playbook deploy.yml -i inventory/production.yml --limit batch_3
```

### Playbook Examples
```yaml
---
- name: Target specific hosts
  hosts: all
  gather_facts: false
  tasks:
    - name: Process web servers
      debug:
        msg: "Processing web server {{ inventory_hostname }}"
      when: hostvars[inventory_hostname].application_service == 'web_server'

    - name: Process high monitoring hosts
      debug:
        msg: "High monitoring host: {{ inventory_hostname }}"
      when: hostvars[inventory_hostname].monitoring_level == 'high'
```

## 📁 Group Variables Setup

### Environment Groups
```bash
# Create environment group_vars files
touch inventory/group_vars/env_production.yml
touch inventory/group_vars/env_development.yml
touch inventory/group_vars/env_test.yml
touch inventory/group_vars/env_acceptance.yml
```

```yaml
# inventory/group_vars/env_production.yml
---
environment_tag: "production"
critical_system: true
```

### Application Groups
```bash
# Create application group_vars files
touch inventory/group_vars/app_web_server.yml
touch inventory/group_vars/app_api_server.yml
touch inventory/group_vars/app_database_server.yml
```

```yaml
# inventory/group_vars/app_web_server.yml
---
role: web_server
web_server_config:
  port: 80
  ssl_port: 443
```

### Product Groups
```bash
# Create product group_vars files
touch inventory/group_vars/product_web.yml
touch inventory/group_vars/product_api.yml
touch inventory/group_vars/product_monitoring.yml
```

```yaml
# inventory/group_vars/product_web.yml
---
product_name: "Web Application"
product_version: "1.0.0"
product_owner: "Web Team"
```

## 🔍 Inventory Inspection

### List and Explore
```bash
# List all hosts
ansible-inventory -i inventory/production.yml --list

# Show inventory structure
ansible-inventory -i inventory/production.yml --graph

# List hosts in specific group
ansible-inventory -i inventory/production.yml --list-hosts app_web_server

# Show host variables
ansible-inventory -i inventory/production.yml --host web01
```

### Group Structure
```
all
├── env_production
│   ├── app_web_server
│   │   ├── product_web
│   │   └── product_monitoring
│   ├── app_api_server
│   │   ├── product_api
│   │   └── product_logging
│   ├── batch_1
│   ├── batch_2
│   ├── batch_3
│   └── site_use1
└── env_development
    └── app_web_server
        └── product_web
```

## ⚙️ Configuration Quick Reference

### Basic Configuration
```yaml
# inventory-config.yml
environments:
  supported:
    - production
    - development
    - test
    - acceptance

hosts:
  inventory_key: "hostname"  # or "cname"

field_mappings:
  host_vars:
    - hostname
    - cname
    - instance
    - ssl_port
    - batch_number
    - patch_mode
    - status
  
  group_references:
    - application_service
    - product_1
    - product_2
    - product_3
    - product_4
    - site_code
    - dashboard_group
    - batch_number
```

### Environment Variables
```bash
# Override CSV file location
export INVENTORY_CSV_FILE="/path/to/custom/hosts.csv"

# Override logging level
export INVENTORY_LOG_LEVEL="DEBUG"

# Override inventory key
export INVENTORY_KEY="cname"
```

## 🛠️ Common Patterns

### Development Workflow
```bash
# 1. Edit CSV file
vim inventory_source/hosts.csv

# 2. Validate changes
make validate

# 3. Generate inventory
make generate

# 4. Test targeting
ansible app_web_server -i inventory/production.yml --list-hosts

# 5. Run playbook
ansible-playbook deploy.yml -i inventory/production.yml --limit app_web_server
```

### CI/CD Integration
```bash
# Install dependencies
make ci-install

# Validate
make validate

# Generate inventory
make generate

# Run tests
make test

# Lint code
make lint
```

### Troubleshooting
```bash
# Check for errors
python scripts/ansible_inventory_cli.py validate

# Health check
python scripts/ansible_inventory_cli.py health

# Dry run
python scripts/ansible_inventory_cli.py generate --dry-run

# Check orphaned files
python scripts/ansible_inventory_cli.py lifecycle --check-orphaned
```

## 📋 Common Scenarios

### Scenario 1: Deploy to Production Web Servers
```bash
# Target production web servers in use1 site
ansible-playbook deploy.yml -i inventory/production.yml \
  --limit "env_production:&site_use1:&app_web_server" \
  --extra-vars "version=2.1.0"
```

### Scenario 2: Monitor All Hosts with Monitoring Product
```bash
# Target all hosts with monitoring product
ansible-playbook monitoring.yml -i inventory/production.yml \
  --limit "product_monitoring"
```

### Scenario 3: Patch Development Hosts
```bash
# Target development hosts with auto patch mode
ansible-playbook patch.yml -i inventory/development.yml \
  --limit "env_development" \
  --extra-vars "patch_mode=auto"
```

### Scenario 4: Database Maintenance
```bash
# Target database servers in production
ansible-playbook db-maintenance.yml -i inventory/production.yml \
  --limit "env_production:&app_database_server"
```

## 🔧 Advanced Features

### Custom CSV Fields
```csv
# Any additional columns become host variables
hostname,environment,status,custom_role,monitoring_level,backup_retention
web01,production,active,frontend,high,30
api01,production,active,backend,medium,7
```

### Unlimited Products
```csv
# Support unlimited product columns
hostname,environment,product_1,product_2,product_3,product_4,product_5,product_6
web01,production,web,monitoring,analytics,cdn,ssl,backup
api01,production,api,logging,cache,load_balancer,,
```

### Host Variable Access
```yaml
# In playbooks, access any CSV field
- name: Use host variables
  debug:
    msg: |
      Host: {{ inventory_hostname }}
      Environment: {{ environment_tag }}
      Application: {{ application_service }}
      Products: {{ products }}
      Custom Role: {{ custom_role }}
      Monitoring Level: {{ monitoring_level }}
```

## 🚨 Common Issues

### CSV Parsing Errors
```bash
# Check CSV format
python scripts/ansible_inventory_cli.py validate

# Verify headers
head -1 inventory_source/hosts.csv
```

### Missing Group Variables
```bash
# Check health
python scripts/ansible_inventory_cli.py health

# Create missing files
touch inventory/group_vars/env_production.yml
```

### Targeting Issues
```bash
# List available groups
ansible-inventory -i inventory/production.yml --graph

# Test targeting
ansible app_web_server -i inventory/production.yml --list-hosts
```

## 📞 Getting Help

### Documentation
- **[Getting Started Guide](docs/getting-started.md)** - Complete tutorial
- **[CSV Format Reference](docs/csv_format.md)** - Field details
- **[Configuration Guide](docs/configuration.md)** - Advanced settings
- **[FAQ](docs/faq.md)** - Common questions

### Commands
```bash
# Get help for any command
python scripts/ansible_inventory_cli.py --help

# Show all Makefile commands
make help

# Validate setup
python scripts/ansible_inventory_cli.py validate
```

---

**Need more help?** Start with the [Getting Started Guide](docs/getting-started.md) for a complete tutorial.