# Troubleshooting Guide

Comprehensive troubleshooting guide for common issues with the Ansible Inventory Management CLI.

## 🔍 Quick Diagnostics

### Health Check Commands
```bash
# Basic health check
python scripts/ansible_inventory_cli.py health

# Verbose health check
python scripts/ansible_inventory_cli.py health --verbose

# JSON output for automation
python scripts/ansible_inventory_cli.py health --output-format json
```

### System Information
```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(ansible|yaml|pathlib)"

# Check project structure
find . -name "*.py" -o -name "*.yml" -o -name "*.csv" | head -20
```

## 🚨 Common Issues & Solutions

### 1. Installation & Setup Issues

#### **Issue**: `ModuleNotFoundError: No module named 'scripts'`
```bash
# Problem: Python can't find the scripts module
# Solution 1: Install in development mode
pip install -e .

# Solution 2: Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Solution 3: Run from project root
cd /path/to/ansible-inventory-cli
python scripts/ansible_inventory_cli.py health
```

#### **Issue**: `FileNotFoundError: inventory_source/hosts.csv`
```bash
# Problem: CSV file missing
# Solution: Create the file or use custom path
python scripts/ansible_inventory_cli.py --csv-file /path/to/your/hosts.csv health

# Or create default file
mkdir -p inventory_source
touch inventory_source/hosts.csv
echo "hostname,environment,location,role,status" > inventory_source/hosts.csv
```

#### **Issue**: `Permission denied` errors
```bash
# Problem: Insufficient permissions
# Solution 1: Use user install
pip install --user -e .

# Solution 2: Fix ownership (Linux/macOS)
sudo chown -R $USER:$USER ~/.local/lib/python*

# Solution 3: Use virtual environment
python -m venv venv
source venv/bin/activate
pip install -e .
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
# Ensure proper headers: hostname,environment,location,role,status
# Check for missing quotes, extra commas, encoding issues
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
# Solution: Add missing columns
python -c "
import csv
required_cols = ['hostname', 'environment', 'location', 'role', 'status']
with open('inventory_source/hosts.csv') as f:
    reader = csv.DictReader(f)
    missing = [col for col in required_cols if col not in reader.fieldnames]
    if missing:
        print(f'Missing columns: {missing}')
    else:
        print('All required columns present')
"
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

# Fix common YAML issues:
# - Inconsistent indentation
# - Missing quotes around special values
# - Invalid characters in keys
```

#### **Issue**: Ansible configuration conflicts
```bash
# Problem: Conflicting ansible.cfg settings
# Diagnosis: Check configuration
ansible-config dump --only-changed

# Solution: Create project-specific config
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
import scripts.ansible_inventory_cli as cli
manager = cli.UnifiedInventoryManager()
hosts = manager.load_hosts()
current, peak = tracemalloc.get_traced_memory()
print(f'Memory usage: {current / 1024 / 1024:.1f}MB')
tracemalloc.stop()
"
```

#### **Issue**: High memory usage
```bash
# Problem: Large host_vars files or memory leaks
# Solution: Check file sizes
find inventory/host_vars -name "*.yml" -exec wc -l {} + | sort -n | tail -10

# Optimize large files
# Remove unnecessary variables
# Use group_vars for common settings
```

### 5. Logging & Debug Issues

#### **Issue**: Missing log files
```bash
# Problem: Log directory not created
# Solution: Create log directory
mkdir -p logs

# Check log configuration
python -c "
import scripts.config as config
print(f'Log directory: {config.LOG_DIR}')
print(f'Log file: {config.LOG_FILE}')
"
```

#### **Issue**: Insufficient logging detail
```bash
# Problem: Log level too high
# Solution: Enable debug logging
export LOG_LEVEL=DEBUG
python scripts/ansible_inventory_cli.py --log-level DEBUG health

# Or permanently in environment
echo "LOG_LEVEL=DEBUG" >> .env
```

#### **Issue**: Log rotation problems
```bash
# Problem: Log files growing too large
# Solution: Set up log rotation
sudo tee /etc/logrotate.d/ansible-inventory << EOF
/path/to/ansible-inventory-cli/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 $USER $USER
}
EOF
```

### 6. GitLab CI/CD Issues

#### **Issue**: Pipeline fails at validation stage
```bash
# Problem: Code quality issues
# Solution: Run checks locally
make pre-commit  # Run all pre-commit hooks
make lint       # Run linting
make format     # Auto-format code

# Fix specific issues
black scripts/                    # Format Python code
isort scripts/                   # Sort imports
flake8 scripts/                  # Check linting
mypy scripts/                    # Type checking
```

#### **Issue**: Test failures in CI
```bash
# Problem: Environment differences
# Solution: Run tests locally with same Python version
python3.10 -m venv test-env
source test-env/bin/activate
pip install -e ".[test]"
pytest tests/ -v

# Check for missing test dependencies
pip install pytest pytest-cov pytest-mock
```

#### **Issue**: Docker build failures
```bash
# Problem: Docker context or dependencies
# Solution: Test Docker build locally
docker build -t test-build .

# Check Docker logs
docker logs <container_id>

# Test with specific base image
docker run -it python:3.10-slim bash
```

### 7. File System & Permissions

#### **Issue**: Cannot write to logs/backups directory
```bash
# Problem: Permission denied
# Solution: Fix permissions
chmod 755 logs backups
chown -R $USER:$USER logs backups

# Or use different location
export LOG_DIR=/tmp/ansible-inventory-logs
mkdir -p $LOG_DIR
```

#### **Issue**: Cross-platform path issues
```bash
# Problem: Windows/Unix path differences
# Solution: Use pathlib (already implemented)
python -c "
from pathlib import Path
print(f'Current path: {Path.cwd()}')
print(f'CSV path: {Path(\"inventory_source/hosts.csv\").resolve()}')
"
```

### 8. Environment & Dependencies

#### **Issue**: Version conflicts
```bash
# Problem: Incompatible package versions
# Solution: Check requirements
pip check

# Create fresh environment
python -m venv fresh-env
source fresh-env/bin/activate
pip install -e .

# Or use specific versions
pip install PyYAML==6.0 pathlib2==2.3.0
```

#### **Issue**: Python version incompatibility
```bash
# Problem: Using unsupported Python version
# Solution: Check compatibility
python -c "
import sys
if sys.version_info < (3, 7):
    print('❌ Python 3.7+ required')
else:
    print(f'✅ Python {sys.version} is compatible')
"

# Install compatible Python version
pyenv install 3.10.12
pyenv local 3.10.12
```

## 🔧 Debug Tools & Commands

### Enable Debug Mode
```bash
# Set debug environment
export DEBUG=1
export LOG_LEVEL=DEBUG

# Run with maximum verbosity
python scripts/ansible_inventory_cli.py --log-level DEBUG health --verbose
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

### Network Debugging
```bash
# Test network connectivity
curl -I https://gitlab.com/company/ansible-inventory-cli
ping gitlab.com

# Check proxy settings
env | grep -i proxy

# Test DNS resolution
nslookup gitlab.com
```

## 📊 Health Monitoring

### System Health Check
```bash
#!/bin/bash
# health_check_system.sh

echo "=== System Health Check ==="

# Check disk space
df -h | grep -E "(/$|inventory|logs)"

# Check memory
free -h

# Check Python environment
python --version
pip list | grep -E "(ansible|yaml)"

# Check file permissions
ls -la inventory_source/hosts.csv
ls -la logs/

# Check process
ps aux | grep python | grep ansible_inventory

echo "=== Application Health Check ==="
python scripts/ansible_inventory_cli.py health --output-format json
```

### Automated Monitoring Script
```python
#!/usr/bin/env python3
# monitor.py

import subprocess
import json
import logging
from datetime import datetime

def check_application_health():
    """Run health check and return results."""
    try:
        result = subprocess.run([
            'python', 'scripts/ansible_inventory_cli.py', 
            'health', '--output-format', 'json'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            logging.error(f"Health check failed: {result.stderr}")
            return None
    except Exception as e:
        logging.error(f"Health check error: {e}")
        return None

if __name__ == "__main__":
    health = check_application_health()
    if health:
        score = health.get('health_score', 0)
        print(f"Health Score: {score}%")
        if score < 80:
            print("⚠️ Health score below threshold")
    else:
        print("❌ Health check failed")
```

## 📞 Getting Additional Help

### Information to Collect Before Asking for Help

```bash
# System information
uname -a
python --version
pip --version

# Application information
python scripts/ansible_inventory_cli.py --version
python scripts/ansible_inventory_cli.py health --output-format json

# Environment information
env | grep -E "(PYTHON|PATH|ANSIBLE)"
ls -la inventory_source/
ls -la logs/

# Error logs
tail -50 logs/audit.log
tail -50 logs/lifecycle_audit.log
```

### Support Channels

1. **Documentation**
   - [Installation Guide](installation.md)
   - [Development Guide](development.md)
   - [GitLab CI/CD Guide](gitlab-cicd.md)

2. **Issue Tracking**
   - Search [existing issues](https://gitlab.com/company/ansible-inventory-cli/-/issues)
   - Create [new issue](https://gitlab.com/company/ansible-inventory-cli/-/issues/new)

3. **Community**
   - GitLab Discussions
   - Internal chat channels
   - Code reviews and merge requests

### Creating Effective Bug Reports

Include the following information:

```markdown
## Environment
- OS: [e.g., Ubuntu 20.04, macOS 12.6, Windows 10]
- Python Version: [e.g., 3.10.8]
- Installation Method: [e.g., pip, source, docker]

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

## Additional Context
[Any other relevant information]
```

---

**Still having issues? Don't hesitate to [create an issue](https://gitlab.com/company/ansible-inventory-cli/-/issues/new) with the information above! 🤝** 