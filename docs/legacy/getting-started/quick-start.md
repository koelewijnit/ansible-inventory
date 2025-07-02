# Quick Start Guide

Get up and running with Ansible Inventory Management in under 5 minutes.

## 🚀 Prerequisites

- Python 3.7 or higher
- Git
- Basic knowledge of Ansible (optional)

## ⚡ 5-Minute Setup

### 1. Clone the Repository

```bash
git clone https://gitlab.com/company/ansible-inventory-cli.git
cd ansible-inventory-cli
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 3. Verify Installation

```bash
# Check version
python scripts/ansible_inventory_cli.py --version

# Run health check
python scripts/ansible_inventory_cli.py health
```

### 4. Generate Your First Inventory

```bash
# Generate inventory files
python scripts/ansible_inventory_cli.py generate

# Check what was created
ls -la inventory/
```

### 5. Validate Everything Works

```bash
# Validate the generated inventory
python scripts/ansible_inventory_cli.py validate

# Check health again
python scripts/ansible_inventory_cli.py health
```

## 🎯 What Just Happened?

1. **Repository Setup**: You now have a local copy of the inventory management system
2. **Environment Setup**: Python virtual environment with all dependencies
3. **Inventory Generation**: Created Ansible inventory files from CSV data
4. **Validation**: Confirmed everything is working correctly

## 📁 Generated Files

After running the generate command, you'll have:

```
inventory/
├── production.yml      # Production environment inventory
├── development.yml     # Development environment inventory
├── test.yml           # Test environment inventory
├── acceptance.yml     # Acceptance environment inventory
├── group_vars/        # Group variables
└── host_vars/         # Host-specific variables
```

## 🔧 Next Steps

### Add Your First System

1. **Edit the CSV file**:
   ```bash
   nano inventory_source/hosts.csv
   ```

2. **Add a new system** (example):
   ```csv
   my-new-server,production,active,,1,us-east-1,443,web,webapp,WebApp,frontend,1,auto,Web,
   ```

3. **Generate updated inventory**:
   ```bash
   python scripts/ansible_inventory_cli.py generate
   ```

4. **Commit your changes**:
   ```bash
   git add inventory_source/hosts.csv inventory/
   git commit -m "Add new system: my-new-server"
   git push origin main
   ```

### Learn More

- **[Adding New Systems](adding-systems.md)** - Complete guide for adding systems
- **[CLI Commands](../user-guide/cli-commands.md)** - All available commands
- **[CSV Management](../user-guide/csv-management.md)** - Working with CSV data
- **[Health Monitoring](../user-guide/health-monitoring.md)** - Monitoring system health

## 🛠️ Using Makefile (Alternative)

If you prefer using the Makefile:

```bash
# Install development dependencies
make install-dev

# Generate inventory
make generate

# Validate
make validate

# Check health
make health-check

# Run all quality checks
make check
```

## 🔍 Troubleshooting

### Common Issues

**"Command not found" error:**
- Ensure you're in the virtual environment: `source venv/bin/activate`
- Check Python installation: `python --version`

**"Module not found" error:**
- Install dependencies: `pip install -e .`
- Check requirements: `pip list`

**"CSV file not found" error:**
- Ensure you're in the project root directory
- Check if `inventory_source/hosts.csv` exists

### Get Help

```bash
# Show all commands
python scripts/ansible_inventory_cli.py --help

# Show specific command help
python scripts/ansible_inventory_cli.py generate --help
python scripts/ansible_inventory_cli.py health --help
```

## 🎉 Congratulations!

You've successfully set up Ansible Inventory Management! 

- ✅ Repository cloned and configured
- ✅ Python environment ready
- ✅ Inventory files generated
- ✅ System validated and healthy

You're now ready to start managing your Ansible inventory efficiently!

---

**Need help?** Check the [Troubleshooting Guide](../operations/troubleshooting.md) or [User Guide](../user-guide/overview.md). 