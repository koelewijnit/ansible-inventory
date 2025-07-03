# Getting Started Guide

This guide will walk you through setting up and using the Ansible Inventory Management System from scratch.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed
- **Git** for cloning the repository
- **Ansible** (will be installed automatically)
- Basic familiarity with YAML and CSV files

## Step 1: Installation

### Clone the Repository
```bash
git clone <repository-url>
cd inventory-structure-new
```

### Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation
```bash
# Check if everything is installed correctly
python scripts/ansible_inventory_cli.py --help
```

## Step 2: Initial Configuration

### Copy Configuration File
```bash
cp inventory-config.yml.example inventory-config.yml
```

### Review and Customize Configuration
Edit `inventory-config.yml` to match your environment:

```yaml
# Basic configuration - modify these for your environment
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
```

## Step 3: Create Your First CSV File

### Create the CSV Structure
Create `inventory_source/hosts.csv` with your host data:

```csv
hostname,environment,status,cname,instance,site_code,ssl_port,application_service,product_1,product_2,product_3,product_4,batch_number,patch_mode,dashboard_group,primary_application,function,decommission_date,custom_role,monitoring_level
web01,production,active,web01.example.com,1,use1,443,web_server,web,monitoring,,,1,auto,web_servers,wordpress,frontend,,frontend,high
api01,production,active,api01.example.com,1,use1,8443,api_server,api,logging,cache,,2,auto,api_servers,django,backend,,backend,medium
db01,production,active,db01.example.com,1,use1,,database_server,database,backup,,,3,manual,database_servers,postgresql,database,,primary,high
dev-web01,development,active,dev-web01.example.com,1,use1,443,web_server,web,,,1,auto,dev_servers,wordpress,frontend,,frontend,low
```

### CSV Field Explanation

#### Required Fields
- **`hostname`**: Unique identifier for the host (e.g., `web01`)
- **`environment`**: Environment name (`production`, `development`, `test`, `acceptance`)
- **`status`**: Host status (`active`, `decommissioned`)

#### Optional Fields
- **`cname`**: Canonical name (e.g., `web01.example.com`)
- **`instance`**: Instance number (e.g., `1`, `2`)
- **`site_code`**: Datacenter/location code (e.g., `use1`, `usw2`)
- **`ssl_port`**: SSL port number (e.g., `443`, `8443`)
- **`application_service`**: Service type (e.g., `web_server`, `api_server`)
- **`product_1`, `product_2`, etc.**: Products running on the host (e.g., `web`, `api`, `monitoring`)
- **`batch_number`**: Patch batch number (e.g., `1`, `2`)
- **`patch_mode`**: Patching mode (`auto`, `manual`)

#### Extra Variables
Any additional columns become host variables automatically:
- **`custom_role`**: Custom role for the host
- **`monitoring_level`**: Monitoring level (`high`, `medium`, `low`)

## Step 4: Create Group Variables Files

### Environment Group Variables
Create environment-specific group variables:

```bash
# Create environment group_vars files
touch inventory/group_vars/env_production.yml
touch inventory/group_vars/env_development.yml
touch inventory/group_vars/env_test.yml
touch inventory/group_vars/env_acceptance.yml
```

Add content to each file:

```yaml
# inventory/group_vars/env_production.yml
---
environment_tag: "production"
critical_system: true
```

```yaml
# inventory/group_vars/env_development.yml
---
environment_tag: "development"
critical_system: false
```

### Application Group Variables
Create application-specific group variables:

```bash
# Create application group_vars files
touch inventory/group_vars/app_web_server.yml
touch inventory/group_vars/app_api_server.yml
touch inventory/group_vars/app_database_server.yml
```

Add content to each file:

```yaml
# inventory/group_vars/app_web_server.yml
---
role: web_server
web_server_config:
  port: 80
  ssl_port: 443
  document_root: /var/www/html
```

```yaml
# inventory/group_vars/app_api_server.yml
---
role: api_server
api_server_config:
  port: 8080
  ssl_port: 8443
```

### Product Group Variables
Create product-specific group variables:

```bash
# Create product group_vars files
touch inventory/group_vars/product_web.yml
touch inventory/group_vars/product_api.yml
touch inventory/group_vars/product_monitoring.yml
```

Add content to each file:

```yaml
# inventory/group_vars/product_web.yml
---
product_name: "Web Application"
product_version: "1.0.0"
product_owner: "Web Team"
```

```yaml
# inventory/group_vars/product_api.yml
---
product_name: "API Service"
product_version: "2.1.0"
product_owner: "API Team"
```

## Step 5: Generate Your First Inventory

### Generate All Environments
```bash
# Generate inventory for all environments
python scripts/ansible_inventory_cli.py generate
```

### Generate Specific Environment
```bash
# Generate only production inventory
python scripts/ansible_inventory_cli.py generate --environments production
```

### Verify Generation
```bash
# Check what was generated
ls -la inventory/

# List all hosts in production
ansible-inventory -i inventory/production.yml --list-hosts all

# Show inventory structure
ansible-inventory -i inventory/production.yml --graph
```

## Step 6: Test Your Inventory

### Basic Inventory Commands
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

### Test Group Targeting
```bash
# Test targeting web servers
ansible app_web_server -i inventory/production.yml --list-hosts

# Test targeting production hosts
ansible env_production -i inventory/production.yml --list-hosts

# Test targeting hosts with web product
ansible product_web -i inventory/production.yml --list-hosts
```

## Step 7: Create Your First Playbook

### Create a Simple Playbook
Create `test-playbook.yml`:

```yaml
---
- name: Test Inventory Playbook
  hosts: all
  gather_facts: false
  tasks:
    - name: Show host information
      debug:
        msg: |
          Host: {{ inventory_hostname }}
          Environment: {{ environment_tag }}
          Application: {{ application_service }}
          Products: {{ products }}
          Site: {{ site_code }}
          Custom Role: {{ custom_role }}
          Monitoring Level: {{ monitoring_level }}
```

### Run the Playbook
```bash
# Run on all hosts
ansible-playbook test-playbook.yml -i inventory/production.yml

# Run only on web servers
ansible-playbook test-playbook.yml -i inventory/production.yml --limit app_web_server

# Run only on production web servers in use1 site
ansible-playbook test-playbook.yml -i inventory/production.yml --limit "env_production:&site_use1:&app_web_server"
```

## Step 8: Advanced Usage Examples

### Complex Targeting Examples
```bash
# Target hosts with specific criteria
ansible-playbook deploy.yml -i inventory/production.yml \
  --limit "env_production:&site_use1:&app_web_server:&product_web"

# Target hosts with monitoring product across all environments
ansible-playbook monitoring.yml -i inventory/production.yml \
  --limit "product_monitoring"

# Target hosts in development with auto patch mode
ansible-playbook patch.yml -i inventory/development.yml \
  --limit "env_development" \
  --extra-vars "patch_mode=auto"
```

### Using Host Variables in Playbooks
```yaml
---
- name: Conditional Tasks Based on Host Variables
  hosts: all
  gather_facts: false
  tasks:
    - name: Process web servers
      debug:
        msg: "Processing web server {{ inventory_hostname }}"
      when: hostvars[inventory_hostname].application_service == 'web_server'

    - name: Process high monitoring level hosts
      debug:
        msg: "High monitoring host: {{ inventory_hostname }}"
      when: hostvars[inventory_hostname].monitoring_level == 'high'

    - name: Process production hosts in use1 site
      debug:
        msg: "Production use1 host: {{ inventory_hostname }}"
      when: >
        hostvars[inventory_hostname].environment == 'production' and
        hostvars[inventory_hostname].site_code == 'use1'
```

## Step 9: Validation and Health Checks

### Validate Your Setup
```bash
# Validate CSV data
python scripts/ansible_inventory_cli.py validate

# Run health check
python scripts/ansible_inventory_cli.py health

# Check for orphaned files
python scripts/ansible_inventory_cli.py lifecycle --check-orphaned
```

### Common Validation Issues
- **Missing required fields**: Ensure `environment` and `status` are present
- **Invalid environment values**: Use only `production`, `development`, `test`, `acceptance`
- **Invalid status values**: Use only `active`, `decommissioned`
- **Missing group_vars files**: Create the required group_vars files

## Step 10: Best Practices

### CSV Management
- Use consistent naming conventions
- Keep CSV files in version control
- Document custom columns
- Regular validation and cleanup

### Group Variables Organization
- Environment-specific settings in `env_*.yml` files
- Application-specific settings in `app_*.yml` files
- Product-specific settings in `product_*.yml` files
- Site-specific settings in `site_*.yml` files

### Playbook Targeting
- Use group targeting for broad operations
- Use host variables for specific conditions
- Combine multiple criteria for precise targeting
- Test targeting before running playbooks

## Troubleshooting

### Common Issues

#### CSV Parsing Errors
```bash
# Check CSV format
python scripts/ansible_inventory_cli.py validate

# Verify CSV headers match configuration
cat inventory_source/hosts.csv | head -1
```

#### Missing Group Variables
```bash
# Check which group_vars files are missing
python scripts/ansible_inventory_cli.py health

# Create missing files
touch inventory/group_vars/env_production.yml
```

#### Inventory Generation Issues
```bash
# Check for errors
python scripts/ansible_inventory_cli.py generate --dry-run

# Verify configuration
cat inventory-config.yml
```

### Getting Help
- Check the [FAQ](faq.md) for common questions
- Review the [Configuration Guide](configuration.md) for advanced settings
- Use the [CSV Format Reference](csv_format.md) for field details
- Run `python scripts/ansible_inventory_cli.py --help` for command options

## Next Steps

Now that you have the basics working:

1. **Customize your configuration** for your specific environment
2. **Add more hosts** to your CSV file
3. **Create more group_vars files** for your applications and products
4. **Build playbooks** that leverage the inventory structure
5. **Set up CI/CD** to automatically generate inventory
6. **Explore advanced features** like lifecycle management and patch management

Congratulations! You now have a fully functional Ansible inventory management system. 