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

### Importing Existing Inventories

### Overview
The system can import existing Ansible inventories and convert them to the CSV format used by this management system. This is useful for migrating from traditional inventory files to the centralized CSV approach.

### Supported Import Sources
- **Ansible YAML inventory files** (single file)
- **JSON inventory files** 
- **Existing host_vars directories** (optional)

### Import Process
The import tool performs intelligent mapping to convert external inventory structures:

1. **Host Discovery**: Extracts all hosts from inventory groups
2. **Environment Detection**: Maps hosts to environments based on:
   - Hostname prefixes (`prd-`, `dev-`, `tst-`, `acc-`)
   - Group names containing environment keywords
   - Explicit environment variables
3. **Application Service Mapping**: Identifies application services from:
   - Group names (webservers → web_server, databases → database)
   - Hostname patterns (bastion → bastion_host, gitlab-runner → cicd_runner)
4. **Product Identification**: Maps products from group/host patterns:
   - apache/nginx → web servers
   - mysql/postgres → databases
   - gitlab → CI/CD runners
5. **Location Detection**: Extracts location from:
   - Hostname patterns (use1, euw1, norwalk, etc.)
   - Host variables (location, datacenter, region)
6. **Metadata Enhancement**: Generates missing fields with intelligent defaults

### Import Commands

#### Test Import (Dry Run)
```bash
# Test import without making changes
python scripts/ansible_inventory_cli.py import \
  --inventory-file /path/to/existing/inventory.yml \
  --dry-run

# Using Makefile
make import-dry-run INVENTORY_FILE=/path/to/inventory.yml
```

#### Full Import
```bash
# Import inventory file only
python scripts/ansible_inventory_cli.py import \
  --inventory-file /path/to/existing/inventory.yml \
  --output-csv inventory_source/imported_hosts.csv

# Import with existing host_vars
python scripts/ansible_inventory_cli.py import \
  --inventory-file /path/to/existing/inventory.yml \
  --host-vars-dir /path/to/existing/host_vars/ \
  --output-csv inventory_source/imported_hosts.csv

# Using Makefile with confirmation
make import-inventory INVENTORY_FILE=/path/to/inventory.yml
make import-inventory INVENTORY_FILE=/path/to/inventory.yml HOST_VARS_DIR=/path/to/host_vars/
```

#### Direct Script Usage
```bash
# Use standalone import script
python scripts/inventory_import.py \
  --inventory /path/to/inventory.yml \
  --host-vars /path/to/host_vars/ \
  --output imported_inventory.csv \
  --dry-run
```

### Import Examples

#### Example 1: Basic YAML Inventory
**Source inventory.yml:**
```yaml
all:
  children:
    production:
      children:
        webservers:
          hosts:
            prod-web-01:
              ansible_host: 10.0.1.10
            prod-web-02:
              ansible_host: 10.0.1.11
        databases:
          hosts:
            prod-db-01:
              ansible_host: 10.0.2.10
```

**Import command:**
```bash
python scripts/ansible_inventory_cli.py import \
  --inventory-file inventory.yml \
  --dry-run
```

**Result:** 3 hosts mapped to production environment with web_server and database application services.

#### Example 2: Import with Host Variables
**Source structure:**
```
existing_infrastructure/
├── inventory.yml
└── host_vars/
    ├── prod-web-01.yml
    ├── prod-web-02.yml
    └── prod-db-01.yml
```

**Import command:**
```bash
python scripts/ansible_inventory_cli.py import \
  --inventory-file existing_infrastructure/inventory.yml \
  --host-vars-dir existing_infrastructure/host_vars/ \
  --output-csv migrated_hosts.csv
```

### Post-Import Workflow

1. **Review Import Report**
   ```bash
   # Check generated report
   cat inventory_source/import_report_*.txt
   ```

2. **Validate Imported Data**
   ```bash
   # Review the generated CSV
   head -10 inventory_source/imported_hosts.csv
   
   # Check for any unmapped fields
   grep ",," inventory_source/imported_hosts.csv
   ```

3. **Backup Current CSV and Replace**
   ```bash
   # Backup existing CSV
   cp inventory_source/hosts.csv inventory_source/hosts.csv.backup
   
   # Replace with imported data
   cp inventory_source/imported_hosts.csv inventory_source/hosts.csv
   ```

4. **Generate New Inventory**
   ```bash
   # Generate inventory from imported CSV
   python scripts/ansible_inventory_cli.py generate
   
   # Validate health
   python scripts/ansible_inventory_cli.py health
   ```

### Import Mapping Reference

| Source Pattern | Target Field | Example |
|---------------|--------------|---------|
| `prd-*`, `prod-*` | environment | `production` |
| `dev-*` | environment | `development` |
| `tst-*`, `test-*` | environment | `test` |
| `acc-*` | environment | `acceptance` |
| Group: `webservers`, `web*`, `apache`, `nginx` | application_service | `web_server` |
| Group: `databases`, `db*`, `mysql`, `postgres` | application_service | `database` |
| Group: `bastion*`, `jump*` | application_service | `bastion_host` |
| Group: `*runner*`, `gitlab*`, `ci*` | application_service | `cicd_runner` |
| Pattern: `apache`, `httpd` | product_id | `apache_httpd` |
| Pattern: `nginx` | product_id | `nginx` |
| Pattern: `mysql` | product_id | `mysql` |
| Pattern: `postgres*` | product_id | `postgresql` |
| Pattern: `use1`, `us-east-1` | location | `use1` |
| Pattern: `euw1`, `eu-west-1` | location | `euw1` |
| Hostname: `*-01`, `*01` | instance | `01` |
| Production hosts | patch_mode | `manual` |
| Non-production hosts | patch_mode | `auto` |

### Troubleshooting Import Issues

#### Common Issues and Solutions

**1. Unable to detect environment**
```bash
# Check hostname patterns
grep -E "^(prd|dev|tst|acc)-" /path/to/inventory.yml

# Manual fix: Add environment field to host_vars
echo "environment: production" >> host_vars/hostname.yml
```

**2. Missing application service mapping**
```bash
# Check group names in inventory
grep -A5 "children:" /path/to/inventory.yml

# Add custom mapping by editing CSV after import
```

**3. Location not detected**
```bash
# Check for region patterns
grep -E "(use|euw|apse)" /path/to/inventory.yml

# Manually set location in CSV or host_vars
```

**4. Import fails with YAML error**
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('/path/to/inventory.yml'))"

# Check for common YAML issues (tabs vs spaces, quotes)
```

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
  --hostname old-server-01 --date 2024-12-31 --dry-run

# 2. Confirm and execute decommission
python scripts/ansible_inventory_cli.py lifecycle decommission \
  --hostname old-server-01 --date 2024-12-31 --reason "Hardware EOL"

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

---

## 🌍 **Geographic Location Management**

The system includes standardized geographic location codes for consistent infrastructure naming.

### **Standard Location Codes**

| Code | Location | Country | Region | Legacy ID |
|------|----------|---------|---------|-----------|
| `shh` | Shanwei | China | Asia Pacific | `shanwei` |
| `tpe` | Taipei | Taiwan | Asia Pacific | `taipei` |
| `lvg` | Las Vegas | United States | Americas | `lasvegas` |
| `nrw` | Norwalk | United States | Americas | `norwalk` |
| `htc` | Eindhoven | Netherlands | Europe | `eindhoven-htc` |
| `eid` | Eindhoven | Netherlands | Europe | `eindhoven-eid` |

### **Geographic Commands**

#### **Using Make Commands**
```bash
# List all locations
make geo-list

# Lookup location details
make geo-lookup-taipei
make geo-lookup-shh

# Validate location codes
make geo-validate-eindhoven-eid

# Convert between legacy and standard codes
make geo-convert-shanwei
```

#### **Direct Script Usage**
```bash
# List all locations
python scripts/geographic_utils.py list

# Lookup specific location
python scripts/geographic_utils.py lookup taipei

# Validate location identifier
python scripts/geographic_utils.py validate shh

# Convert legacy to standard code
python scripts/geographic_utils.py convert shanwei

# Different output formats
python scripts/geographic_utils.py list --format json
python scripts/geographic_utils.py lookup taipei --format yaml
```

### **Location Information Includes**

- **Standard Code**: Official 3-letter code (e.g., `shh`)
- **Full Name**: Human-readable name (e.g., `Shanwei`)
- **Country & Region**: Geographic classification
- **Legacy Identifier**: Current naming in CSV files
- **Timezone**: Local timezone for the location
- **Currency**: Local currency code
- **DNS/NTP Servers**: Regional infrastructure settings

### **Usage in Infrastructure**

The location codes are used in:
- Host naming conventions (`prd-web-{location}-01`)
- CSV location column values
- Ansible group variables for regional settings
- Network infrastructure configuration

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
ERROR: Invalid date format: 12/31/2024. Use YYYY-MM-DD
```
**Solution**: Use ISO date format: `2024-12-31`

### **Exit Codes**

- **0**: Success
- **1**: Command error (validation failed, invalid input)
- **2**: File not found
- **3**: Unexpected error

---

**Version**: 4.0.0  
**Status**: Production Ready  
**Team**: Infrastructure as Code Team
