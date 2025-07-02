# Quick Reference - Ansible Inventory Management

## 🚀 **Add New System (Complete Workflow)**

```bash
# 1. Edit CSV file
nano inventory_source/hosts.csv

# 2. Generate inventory
python scripts/ansible_inventory_cli.py generate

# 3. Validate changes
python scripts/ansible_inventory_cli.py validate

# 4. Add to git
git add inventory_source/hosts.csv inventory/
git commit -m "Add new system: server-name"
git push origin main
```

## 📝 **CSV Format (Required Fields)**

```csv
hostname,environment,status,cname,instance,site_code,ssl_port,application_service,product_id,primary_application,function,batch_number,patch_mode,dashboard_group,decommission_date
prod-web-01,production,active,,1,us-east-1,443,web,webapp,WebApp,frontend,1,auto,Web,
```

**Required:** `hostname`, `environment`, `status`

## 🔧 **Essential Commands**

| Command | Purpose |
|---------|---------|
| `python scripts/ansible_inventory_cli.py generate` | Generate inventory files |
| `python scripts/ansible_inventory_cli.py health` | Check system health |
| `python scripts/ansible_inventory_cli.py validate` | Validate configuration |
| `python scripts/ansible_inventory_cli.py --help` | Show all commands |

## 🛠️ **Makefile Shortcuts**

| Command | Purpose |
|---------|---------|
| `make generate` | Generate inventory |
| `make validate` | Validate structure |
| `make health-check` | Check health |
| `make help` | Show all commands |

## 📋 **Common Values**

### Environments
- `production`
- `development` 
- `test`
- `acceptance`

### Status
- `active`
- `decommissioned`

### Patch Modes
- `auto`
- `manual`

## 🔍 **Troubleshooting**

```bash
# Check CSV format
python scripts/ansible_inventory_cli.py validate --csv-only

# Create CSV template
python scripts/ansible_inventory_cli.py validate --create-csv template.csv

# Show CSV template format
python scripts/ansible_inventory_cli.py validate --template
```

## 📚 **More Information**

- **[Complete Guide: Adding New Systems](docs/ADDING_SYSTEMS.md)**
- **[User Guide](USER_GUIDE.md)**
- **[Troubleshooting](docs/troubleshooting.md)**

---

**Need help?** Run `python scripts/ansible_inventory_cli.py --help`