# Ansible Inventory Management - User Guide

Complete guide for using the unified CLI inventory management system.

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.7 or higher
- PyYAML package (`pip install PyYAML`)
- Ansible (optional, for validation)

### **Installation**
```bash
# 1. Make the CLI executable
chmod +x scripts/ansible_inventory_cli.py

# 2. Optional: Create a convenient alias
alias inventory-cli='python scripts/ansible_inventory_cli.py'

# 3. Verify installation
python scripts/ansible_inventory_cli.py --version
```

---

## 📋 **CLI Commands Reference**

### **Global Options**

All commands support these global options:

```bash
--csv-file PATH           # Use custom CSV file
--log-level LEVEL         # DEBUG, INFO, WARNING, ERROR
--output-format FORMAT    # text (default) or json
--version                 # Show version information
--help                    # Show help information
```

### **Generate Command**

Generate Ansible inventory files and host variables.

```bash
# Basic usage - generate all environments
python scripts/ansible_inventory_cli.py generate

# Generate specific environments
python scripts/ansible_inventory_cli.py generate --environments production test

# Custom output directories
python scripts/ansible_inventory_cli.py generate \
  --output-dir custom_inventory \
  --host-vars-dir custom_inventory/host_vars

# Using custom CSV file
python scripts/ansible_inventory_cli.py generate \
  --csv-file backup_hosts.csv
```

**Options:**
- `--output-dir, -o`: Output directory for inventory files (default: `inventory`)
- `--host-vars-dir`: Directory for host_vars files (default: `inventory/host_vars`)
- `--environments, -e`: Specific environments to generate

### **Health Command**

Monitor inventory health and get recommendations.

```bash
# Basic health check
python scripts/ansible_inventory_cli.py health

# JSON output for automation
python scripts/ansible_inventory_cli.py --output-format json health

# Health check with custom CSV
python scripts/ansible_inventory_cli.py --csv-file custom.csv health
```

**Health Scoring:**
- **EXCELLENT** (95-100%): Optimal health
- **GOOD** (85-94%): Minor issues
- **FAIR** (70-84%): Some attention needed
- **POOR** (50-69%): Significant issues
- **CRITICAL** (<50%): Immediate action required

### **CSV Management**

### Viewing CSV Data
```bash
# View CSV with column headers
head -5 inventory_source/hosts.csv

# Count hosts by environment
cut -d',' -f3 inventory_source/hosts.csv | sort | uniq -c

# Filter by specific environment
grep ",production," inventory_source/hosts.csv
```

### Manual CSV Editing
- Always backup before editing: `cp inventory_source/hosts.csv inventory_source/hosts.csv.backup`
- Use proper CSV format with quoted fields containing commas
- Validate after editing: `python scripts/ansible_inventory_cli.py validate`



## 🎯 **Common Workflows**

### **Daily Operations Workflow**

```bash
# 1. Check system health
python scripts/ansible_inventory_cli.py health

# 2. If health issues found, investigate
python scripts/ansible_inventory_cli.py --log-level DEBUG health

# 3. Generate updated inventories
python scripts/ansible_inventory_cli.py generate

# 4. Validate configuration
python scripts/ansible_inventory_cli.py validate

# 5. Test with Ansible (optional)
ansible-inventory -i inventory/production.yml --list
```

### **Host Decommissioning Workflow**

```bash
# 1. Mark host as decommissioned (dry run first)
python scripts/ansible_inventory_cli.py lifecycle decommission \
  --hostname old-server-01 --date 2025-12-31 --dry-run

# 2. Confirm and execute decommission
python scripts/ansible_inventory_cli.py lifecycle decommission \
  --hostname old-server-01 --date 2025-12-31 --reason "Hardware EOL"

# 3. Regenerate inventories
python scripts/ansible_inventory_cli.py generate

# 4. Verify health improvement
python scripts/ansible_inventory_cli.py health

# 5. Later: Cleanup expired hosts
python scripts/ansible_inventory_cli.py lifecycle list-expired
python scripts/ansible_inventory_cli.py lifecycle cleanup --dry-run
python scripts/ansible_inventory_cli.py lifecycle cleanup
```

---

## 📊 **CSV Data Management**

### **Required CSV Columns**

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| `hostname` | ✅ | Unique hostname | `prd-web-01` |
| `environment` | ✅ | Environment name | `production` |
| `status` | ✅ | Host status | `active`, `decommissioned` |
| `application_service` | ❌ | Service type | `web_server`, `database` |
| `product_id` | ❌ | Product identifier | `apache_httpd`, `postgresql` |
| `location` | ❌ | Geographic location | `us-east-1`, `europe-west1` |
| `batch_number` | ❌ | Patch batch | `batch_1`, `batch_2` |
| `patch_mode` | ❌ | Patching mode | `manual`, `auto` |
| `ansible_tags` | ❌ | Comma-separated list of custom Ansible tags | `web, database, critical` |

### **Using Ansible Tags**

The `ansible_tags` column allows you to assign arbitrary tags to your hosts directly in the CSV. These tags are then included in the generated `host_vars` for each host. This enables powerful and flexible targeting in your Ansible playbooks using the `--tags` or `--skip-tags` command-line options.

**How it works:**
- When you generate the inventory, the value from the `ansible_tags` column for each host is added to its `host_vars`.
- If a host has multiple tags, separate them with commas (e.g., `web, database, critical`).

**Use Cases:**
- **Granular Playbook Execution:** Run specific tasks only on hosts with certain tags.
  ```bash
  # Run tasks tagged 'security' only on hosts with 'web' tag
  ansible-playbook my_playbook.yml --limit @web --tags security
  ```
- **Excluding Hosts from Tasks:** Skip tasks on hosts with specific tags.
  ```bash
  # Run all tasks except those tagged 'maintenance' on all production web servers
  ansible-playbook webservers.yml -i inventory/production.yml --skip-tags maintenance
  ```
- **Categorizing Hosts:** Group hosts by custom criteria not covered by other fields.
  ```csv
  hostname,environment,ansible_tags
  server1,production,frontend,nginx,critical
  server2,production,backend,database
  server3,development,test,experimental
  ```
  In your playbook, you can then target:
  ```bash
  # Target all 'critical' hosts
  ansible all -i inventory/production.yml --list-hosts --limit @critical
  ```
- **Feature Rollouts:** Tag hosts participating in a new feature rollout.
- **Compliance Audits:** Tag hosts that require specific compliance checks.

**Important Considerations:**
- Tags are free-form strings. Ensure consistency in naming to avoid issues.
- Avoid using spaces within a single tag (e.g., use `web_server` instead of `web server`).
---

### **Group Targeting**

#### **Application Service Groups**
Target hosts by function across all products:

```bash
# All web servers (Apache + Nginx + others)
ansible app_web_server -i inventory/production.yml --list-hosts

# All databases (PostgreSQL + MongoDB + others)
ansible app_database -i inventory/production.yml --list-hosts

# All identity management systems
ansible app_identity_management -i inventory/production.yml --list-hosts
```

#### **Product-Specific Groups**
Target hosts by specific software:

```bash
# Only Apache HTTP servers
ansible product_apache_httpd -i inventory/production.yml --list-hosts

# Only PostgreSQL databases
ansible product_postgresql -i inventory/production.yml --list-hosts

# Only Kubernetes infrastructure
ansible product_kubernetes -i inventory/production.yml --list-hosts
```

---

## 🛡️ **Best Practices**

### **Operational Best Practices**

1. **Regular Health Checks**: Monitor inventory health daily
2. **Staged Changes**: Always use `--dry-run` for lifecycle operations
3. **Backup Before Changes**: CSV files are automatically backed up
4. **Validate After Changes**: Run validation after any modifications
5. **Environment Consistency**: Keep environments synchronized

### **CSV Management Best Practices**

1. **Version Control**: Keep CSV files in version control
2. **Regular Backups**: Use automated backup strategies
3. **Data Validation**: Validate data before importing
4. **Consistent Formats**: Maintain consistent naming conventions
5. **Documentation**: Document any custom fields or conventions

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **CSV File Not Found**
```bash
ERROR: CSV file not found: inventory_source/hosts.csv
```
**Solution**: Verify file path and permissions, or use `--csv-file` to specify correct path.

#### **Invalid Date Format**
```bash
ERROR: Invalid date format: 12/31/2025. Use YYYY-MM-DD
```
**Solution**: Use ISO date format: `2025-12-31`

### **Exit Codes**

- **0**: Success
- **1**: Command error (validation failed, invalid input)
- **2**: File not found
- **3**: Unexpected error

---

**Version**: 4.0.0  
**Status**: Production Ready  
**Team**: Infrastructure as Code Team

---



## 🎯 **Ansible Integration**

### **Group Targeting**

#### **Application Service Groups**
Target hosts by function across all products:

```bash
# All web servers (Apache + Nginx + others)
ansible app_web_server -i inventory/production.yml --list-hosts

# All databases (PostgreSQL + MongoDB + others)
ansible app_database -i inventory/production.yml --list-hosts

# All identity management systems
ansible app_identity_management -i inventory/production.yml --list-hosts
```

#### **Product-Specific Groups**
Target hosts by specific software:

```bash
# Only Apache HTTP servers
ansible product_apache_httpd -i inventory/production.yml --list-hosts

# Only PostgreSQL databases
ansible product_postgresql -i inventory/production.yml --list-hosts

# Only Kubernetes infrastructure
ansible product_kubernetes -i inventory/production.yml --list-hosts
```

---

## 🛡️ **Best Practices**

### **Operational Best Practices**

1. **Regular Health Checks**: Monitor inventory health daily
2. **Staged Changes**: Always use `--dry-run` for lifecycle operations
3. **Backup Before Changes**: CSV files are automatically backed up
4. **Validate After Changes**: Run validation after any modifications
5. **Environment Consistency**: Keep environments synchronized

### **CSV Management Best Practices**

1. **Version Control**: Keep CSV files in version control
2. **Regular Backups**: Use automated backup strategies
3. **Data Validation**: Validate data before importing
4. **Consistent Formats**: Maintain consistent naming conventions
5. **Documentation**: Document any custom fields or conventions

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **CSV File Not Found**
```bash
ERROR: CSV file not found: inventory_source/hosts.csv
```
**Solution**: Verify file path and permissions, or use `--csv-file` to specify correct path.

#### **Invalid Date Format**
```bash
ERROR: Invalid date format: 12/31/2025. Use YYYY-MM-DD
```
**Solution**: Use ISO date format: `2025-12-31`

### **Exit Codes**

- **0**: Success
- **1**: Command error (validation failed, invalid input)
- **2**: File not found
- **3**: Unexpected error

---

**Version**: 4.0.0  
**Status**: Production Ready  
**Team**: Infrastructure as Code Team
