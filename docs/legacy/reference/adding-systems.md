# Adding New Systems to Inventory

A simple guide for adding new systems to the Ansible inventory.

## 🚀 Quick Workflow

1. **Add system to CSV** → 2. **Generate inventory** → 3. **Commit to git** → 4. **Push changes**

---

## 📝 Step 1: Add System to CSV

### Open the CSV file:
```bash
# Edit the main CSV file
nano inventory_source/hosts.csv
```

### Add your new system:
Add a new row with your system details. Here's the format:

```csv
hostname,environment,status,cname,instance,datacenter,ssl_port,application_service,product_id,primary_application,function,batch_number,patch_mode,dashboard_group,decommission_date
your-new-server,production,active,,1,us-east-1,443,web,webapp,WebApp,frontend,1,auto,Web,
```

### Required Fields:
- **hostname**: Your server name (e.g., `prod-web-01`)
- **environment**: `production`, `development`, `test`, or `acceptance`
- **status**: `active` or `decommissioned`

### Example Systems:
```csv
# Web server
prod-web-01,production,active,,1,us-east-1,443,web,webapp,WebApp,frontend,1,auto,Web,

# Database server  
prod-db-01,production,active,,1,us-east-1,5432,db,postgres,Database,backend,2,manual,DB,

# Test server
test-app-01,test,active,,1,us-east-1,8080,app,appsvc,AppService,api,3,auto,API,
```

---

## 🔧 Step 2: Generate Inventory Files

### Run the generate command:
```bash
# Generate all inventory files
python scripts/ansible_inventory_cli.py generate
```

### What this does:
- Creates `inventory/production.yml`, `inventory/development.yml`, etc.
- Generates host variable files in `inventory/host_vars/`
- Updates group variable files in `inventory/group_vars/`

### Verify the generation:
```bash
# Check what was created
ls -la inventory/
ls -la inventory/host_vars/
```

---

## ✅ Step 3: Validate Your Changes

### Run validation:
```bash
# Validate the CSV and inventory structure
python scripts/ansible_inventory_cli.py validate
```

### Check health:
```bash
# Monitor inventory health
python scripts/ansible_inventory_cli.py health
```

---

## 📁 Step 4: Add Files to Git

### Stage your changes:
```bash
# Add the CSV file
git add inventory_source/hosts.csv

# Add the generated inventory files
git add inventory/

# Check what will be committed
git status
```

### Commit your changes:
```bash
# Commit with a descriptive message
git commit -m "Add new system: your-new-server"
```

---

## 🚀 Step 5: Push to Git

### Push your changes:
```bash
# Push to the main branch
git push origin main
```

---

## 🛠️ Using Makefile (Alternative)

If you prefer using the Makefile:

```bash
# Generate inventory
make generate

# Validate changes  
make validate

# Check health
make health-check

# Add and commit (manual)
git add .
git commit -m "Add new system"
git push origin main
```

---

## 📋 CSV Template

Need a template? Run this command:
```bash
# Create a new CSV template
python scripts/ansible_inventory_cli.py validate --create-csv new_systems.csv
```

---

## 🔍 Troubleshooting

### Common Issues:

**"Invalid hostname" error:**
- Use lowercase letters, numbers, and hyphens only
- Example: `prod-web-01` ✅, `PROD_WEB_01` ❌

**"Invalid environment" error:**
- Use only: `production`, `development`, `test`, `acceptance`
- Example: `production` ✅, `prod` ❌

**"CSV validation failed" error:**
- Check that all required fields are filled
- Ensure proper CSV formatting (commas, quotes)

### Get Help:
```bash
# Show all available commands
python scripts/ansible_inventory_cli.py --help

# Show specific command help
python scripts/ansible_inventory_cli.py generate --help
python scripts/ansible_inventory_cli.py validate --help
```

---

## 📚 Field Reference

| Field | Required | Example | Description |
|-------|----------|---------|-------------|
| `hostname` | ✅ | `prod-web-01` | Server name |
| `environment` | ✅ | `production` | Environment |
| `status` | ✅ | `active` | Server status |
| `cname` | ❌ | `web.example.com` | DNS alias |
| `instance` | ❌ | `1` | Instance number |
| `datacenter` | ❌ | `us-east-1` | Datacenter/geographic location |
| `ssl_port` | ❌ | `443` | SSL port number |
| `application_service` | ❌ | `web` | Service type |
| `product_id` | ❌ | `webapp` | Product identifier |
| `primary_application` | ❌ | `WebApp` | Main application |
| `function` | ❌ | `frontend` | Server function |
| `batch_number` | ❌ | `1` | Patching batch |
| `patch_mode` | ❌ | `auto` | Patching mode |
| `dashboard_group` | ❌ | `Web` | Monitoring group |
| `decommission_date` | ❌ | `2024-12-31` | Decommission date |
| `notes` | ❌ | `Migrated from old cluster` | General notes or comments |
| `ansible_tags` | ❌ | `web, database, critical` | Comma-separated list of custom Ansible tags |

---

**Need more help?** Check the [User Guide](USER_GUIDE.md) or [Troubleshooting Guide](troubleshooting.md). 