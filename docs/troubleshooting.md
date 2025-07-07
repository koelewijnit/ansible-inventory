# Troubleshooting Guide

Comprehensive troubleshooting guide for common issues with the Ansible Inventory Management System.

## 🔍 Quick Diagnostics

### Health Check Commands
```bash
# Basic health check
python scripts/ansible_inventory_cli.py health

# Detailed health check
python scripts/ansible_inventory_cli.py health --detailed

# Health check with custom threshold
python scripts/ansible_inventory_cli.py health --threshold 85
```

### System Information
```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(ansible|yaml|pathlib)"

# Check project structure
find . -name "*.py" -o -name "*.yml" -o -name "*.csv" | head -20

# Check current configuration
python scripts/ansible_inventory_cli.py validate --template
```

## 🚨 Common Issues & Solutions

### 1. Installation & Setup Issues

#### **Issue**: `ModuleNotFoundError: No module named 'scripts'`
```bash
# Problem: Python can't find the scripts module
# Solution 1: Run from project root
cd /path/to/inventory-structure-new
python scripts/ansible_inventory_cli.py health

# Solution 2: Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Solution 3: Use virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### **Issue**: `FileNotFoundError: inventory_source/hosts.csv`
```bash
# Problem: CSV file missing
# Solution: Create the file or use custom path
python scripts/ansible_inventory_cli.py --csv-file /path/to/your/hosts.csv health

# Or create default file
mkdir -p inventory_source
python scripts/ansible_inventory_cli.py validate --create-csv inventory_source/hosts.csv
```

#### **Issue**: `Permission denied` errors
```bash
# Problem: Insufficient permissions
# Solution 1: Use virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Solution 2: Use user install
pip install --user -r requirements.txt

# Solution 3: Fix ownership (Linux/macOS)
sudo chown -R $USER:$USER ~/.local/lib/python*
```

### 2. CSV File Issues

#### **Issue**: CSV parsing errors
```bash
# Problem: Invalid CSV format
# Diagnosis: Check CSV structure
python -c "
import csv
with open('inventory_source/hosts.csv') as f:
    reader = csv.DictReader(f)
    print('Headers:', reader.fieldnames)
    try:
        first_row = next(reader)
        print('First row:', first_row)
    except Exception as e:
        print('Error reading first row:', e)
"

# Solution: Fix CSV format
# Ensure proper headers match configuration
python scripts/ansible_inventory_cli.py validate --template
```

#### **Issue**: Encoding problems (special characters)
```bash
# Problem: Non-UTF-8 encoding
# Diagnosis: Check file encoding
file -bi inventory_source/hosts.csv

# Solution: Convert to UTF-8
iconv -f windows-1252 -t utf-8 hosts.csv > hosts_utf8.csv
mv hosts_utf8.csv inventory_source/hosts.csv

# Or specify encoding in Python
python -c "
import pandas as pd
df = pd.read_csv('inventory_source/hosts.csv', encoding='latin-1')
df.to_csv('inventory_source/hosts.csv', encoding='utf-8', index=False)
"
```

#### **Issue**: Missing required columns
```bash
# Problem: CSV missing required columns
# Solution: Check required fields
python scripts/ansible_inventory_cli.py validate --comprehensive

# Show template with all fields
python scripts/ansible_inventory_cli.py validate --template

# Required fields: hostname, environment, status
# Optional fields: cname, product_1, product_2, etc.
```

#### **Issue**: Product column validation errors
```bash
# Problem: Invalid product column format
# Solution: Use product_1, product_2, product_3, etc.
# Example CSV:
# hostname,environment,status,product_1,product_2,product_3
# web01,production,active,web,monitoring,
# api01,production,active,api,logging,cache

# Check product column validation
python scripts/ansible_inventory_cli.py validate --csv-only
```

### 3. Ansible Integration Issues

#### **Issue**: `ansible-inventory` command not found
```bash
# Problem: Ansible not installed
# Solution: Install Ansible
pip install ansible>=4.0.0

# Verify installation
ansible --version
which ansible-inventory
```

#### **Issue**: Ansible inventory validation fails
```bash
# Problem: Invalid inventory YAML
# Diagnosis: Check syntax
ansible-inventory --inventory inventory/production.yml --list

# Solution: Validate YAML syntax
python -c "
import yaml
with open('inventory/production.yml') as f:
    try:
        yaml.safe_load(f)
        print('✅ YAML syntax is valid')
    except yaml.YAMLError as e:
        print(f'❌ YAML syntax error: {e}')
"

# Regenerate inventory files
python scripts/ansible_inventory_cli.py generate
```

#### **Issue**: Ansible configuration conflicts
```bash
# Problem: Conflicting ansible.cfg settings
# Diagnosis: Check configuration
ansible-config dump --only-changed

# Solution: Use project ansible.cfg
cat > ansible.cfg << EOF
[defaults]
inventory = inventory
host_key_checking = False
stdout_callback = yaml

[inventory]
enable_plugins = yaml
EOF
```

### 4. Performance Issues

#### **Issue**: Slow health check performance
```bash
# Problem: Large inventory or slow I/O
# Diagnosis: Profile execution
time python scripts/ansible_inventory_cli.py health

# Solution 1: Use SSD storage for better I/O
# Solution 2: Optimize CSV size (remove unnecessary columns)
# Solution 3: Increase system resources

# Monitor memory usage
python -c "
import tracemalloc
tracemalloc.start()
from scripts.managers.inventory_manager import InventoryManager
manager = InventoryManager()
hosts = manager.load_hosts()
current, peak = tracemalloc.get_traced_memory()
print(f'Memory usage: {current / 1024 / 1024:.1f}MB')
tracemalloc.stop()
"
```

#### **Issue**: Large inventory generation slowdown
```bash
# Problem: Slow inventory generation
# Diagnosis: Time the operation
time python scripts/ansible_inventory_cli.py generate

# Solution: Use dry-run to test
python scripts/ansible_inventory_cli.py generate --dry-run

# Generate specific environments only
python scripts/ansible_inventory_cli.py generate --environments production
```

### 5. Configuration Issues

#### **Issue**: `Configuration file not found`
```bash
# Problem: Missing inventory-config.yml
# Solution: Copy template
cp inventory-config.yml.example inventory-config.yml

# Edit configuration
nano inventory-config.yml

# Validate configuration
python scripts/ansible_inventory_cli.py validate --structure-only
```

#### **Issue**: Invalid environment names
```bash
# Problem: Using unsupported environment names
# Solution: Check supported environments
python -c "
from scripts.core.config import get_supported_environments
print('Supported environments:', get_supported_environments())
"

# Use only: production, development, test, acceptance
# Update inventory-config.yml if needed
```

#### **Issue**: Group variables not loading
```bash
# Problem: Missing group_vars files
# Solution: Create group_vars structure
mkdir -p inventory/group_vars

# Create environment group variables
touch inventory/group_vars/env_production.yml
touch inventory/group_vars/env_development.yml

# Create application group variables
touch inventory/group_vars/app_web_server.yml
touch inventory/group_vars/app_api_server.yml

# Validate structure
python scripts/ansible_inventory_cli.py validate --structure-only
```

### 6. Host Lifecycle Issues

#### **Issue**: Decommissioning fails
```bash
# Problem: Cannot decommission host
# Diagnosis: Check host exists
python scripts/ansible_inventory_cli.py lifecycle list-expired

# Solution: Use correct hostname
python scripts/ansible_inventory_cli.py lifecycle decommission \
  --hostname correct-hostname \
  --date 2025-12-31 \
  --dry-run

# Check CSV for exact hostname
grep "hostname" inventory_source/hosts.csv
```

#### **Issue**: Cleanup removes wrong hosts
```bash
# Problem: Cleanup affecting wrong hosts
# Solution: Always use dry-run first
python scripts/ansible_inventory_cli.py lifecycle cleanup --dry-run

# Check grace periods
python scripts/ansible_inventory_cli.py lifecycle cleanup \
  --grace-days 30 \
  --dry-run

# Limit cleanup scope
python scripts/ansible_inventory_cli.py lifecycle cleanup \
  --max-hosts 5 \
  --dry-run
```

### 7. Validation Issues

#### **Issue**: Health score always low
```bash
# Problem: Poor health score
# Diagnosis: Check detailed health
python scripts/ansible_inventory_cli.py health --detailed

# Common causes:
# 1. Orphaned host_vars files
# 2. Missing host_vars files
# 3. Decommissioned hosts not cleaned up

# Solution: Clean up orphaned files
python scripts/ansible_inventory_cli.py lifecycle cleanup --dry-run
```

#### **Issue**: Validation always fails
```bash
# Problem: Validation errors
# Diagnosis: Run comprehensive validation
python scripts/ansible_inventory_cli.py validate --comprehensive

# Check specific issues:
# 1. CSV structure
python scripts/ansible_inventory_cli.py validate --csv-only

# 2. Directory structure
python scripts/ansible_inventory_cli.py validate --structure-only

# 3. Show template
python scripts/ansible_inventory_cli.py validate --template
```

### 8. Makefile Issues

#### **Issue**: `make: command not found`
```bash
# Problem: Make not installed
# Solution: Install make
# Ubuntu/Debian:
sudo apt install make
# macOS:
xcode-select --install
# Windows:
# Use WSL or install make for Windows
```

#### **Issue**: Makefile targets fail
```bash
# Problem: Make targets not working
# Diagnosis: Check available targets
make help

# Common solutions:
# 1. Ensure you're in project root
cd inventory-structure-new

# 2. Check Python path
make validate

# 3. Use direct commands if make fails
python scripts/ansible_inventory_cli.py generate
python scripts/ansible_inventory_cli.py validate
python scripts/ansible_inventory_cli.py health
```

## 🔧 Debug Tools & Commands

### Enable Debug Mode
```bash
# Set debug environment
export DEBUG=1
export LOG_LEVEL=DEBUG

# Run with maximum verbosity
python scripts/ansible_inventory_cli.py --log-level DEBUG health --detailed
```

### Memory & Performance Profiling
```bash
# Profile script execution
python -m cProfile -o profile.stats scripts/ansible_inventory_cli.py health

# Analyze results
python -c "
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('tottime').print_stats(10)
"

# Memory profiling with memory_profiler
pip install memory-profiler
python -m memory_profiler scripts/ansible_inventory_cli.py health
```

### File System Debugging
```bash
# Check file permissions
ls -la inventory_source/hosts.csv
ls -la inventory/
ls -la inventory/group_vars/
ls -la inventory/host_vars/

# Check disk space
df -h

# Check file encoding
file -bi inventory_source/hosts.csv

# Check for hidden characters
cat -A inventory_source/hosts.csv | head -5
```

## 📊 System Health Monitoring

### Automated Health Check Script
```bash
#!/bin/bash
# health_check_system.sh

echo "=== System Health Check ==="

# Check Python version
echo "Python version: $(python --version)"

# Check project structure
echo "Project structure:"
ls -la

# Check CSV file
if [ -f "inventory_source/hosts.csv" ]; then
    echo "CSV file exists: $(wc -l < inventory_source/hosts.csv) lines"
else
    echo "❌ CSV file missing"
fi

# Run health check
echo "Running health check..."
python scripts/ansible_inventory_cli.py health --detailed

# Check recent logs
if [ -d "logs" ]; then
    echo "Recent log files:"
    ls -la logs/ | head -5
fi

echo "=== Health Check Complete ==="
```

### Continuous Monitoring
```bash
# Monitor health score over time
while true; do
    score=$(python scripts/ansible_inventory_cli.py health --json | jq -r '.data.health_score')
    echo "$(date): Health Score: $score%"
    sleep 300  # Check every 5 minutes
done
```

## 📞 Getting Help

### Documentation Resources
1. **Installation Guide**: [Installation Guide](installation.md)
2. **Getting Started**: [Getting Started Guide](getting-started.md)
3. **Usage Guide**: [Usage Guide](usage.md)
4. **FAQ**: [FAQ](faq.md)

### Command Help
```bash
# General help
python scripts/ansible_inventory_cli.py --help

# Command-specific help
python scripts/ansible_inventory_cli.py generate --help
python scripts/ansible_inventory_cli.py health --help
python scripts/ansible_inventory_cli.py validate --help
python scripts/ansible_inventory_cli.py lifecycle --help

# Makefile help
make help
```

### Creating Effective Bug Reports

Include the following information when reporting issues:

```markdown
## Environment
- OS: [e.g., Ubuntu 22.04, macOS 13.0, Windows 11]
- Python Version: [e.g., 3.10.8]
- Installation Method: [e.g., virtual environment, system-wide]

## Expected Behavior
[Describe what you expected to happen]

## Actual Behavior
[Describe what actually happened]

## Steps to Reproduce
1. [First step]
2. [Second step]
3. [Third step]

## Error Messages
```
[Paste any error messages here]
```

## System Information
```
[Include output of health check and system info]
```

## Configuration
```
[Include relevant configuration files]
```
```

### Log Collection
```bash
# Collect system information
python scripts/ansible_inventory_cli.py health --detailed > health_report.txt

# Collect debug logs
python scripts/ansible_inventory_cli.py --log-level DEBUG validate --comprehensive > debug_log.txt

# Collect configuration
cp inventory-config.yml config_backup.yml

# Create support bundle
tar -czf support_bundle.tar.gz \
  health_report.txt \
  debug_log.txt \
  config_backup.yml \
  inventory_source/hosts.csv \
  logs/
```

---

**Still having issues? Check the [FAQ](faq.md) or create an issue with the information above! 🤝** 