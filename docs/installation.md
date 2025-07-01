# Installation Guide

Complete installation guide for the Ansible Inventory Management CLI across different environments and use cases.

## 🎯 Installation Methods

Choose the installation method that best fits your environment:

| Method | Best For | Python Required |
|--------|----------|-----------------|
| **Direct Script** | Development, testing | ✅ 3.7+ |
| **Package Install** | Production, system-wide | ✅ 3.7+ |
| **Docker** | Containerized environments | ❌ |
| **From Source** | Contributing, customization | ✅ 3.7+ |

## 📋 Prerequisites

### System Requirements

#### Minimum Requirements
- **OS**: Linux, macOS, Windows
- **Python**: 3.7 or higher (recommended: 3.10+)
- **Memory**: 512MB RAM
- **Disk**: 100MB free space
- **Network**: Internet access for initial setup

#### Recommended Requirements
- **Python**: 3.10+ for best performance
- **Memory**: 1GB+ RAM for large inventories
- **Disk**: 1GB+ for logs and backups

### Software Dependencies

#### Core Dependencies (Automatically Installed)
- `PyYAML>=6.0` - YAML processing
- `pathlib2>=2.3.0` - Path handling (Python <3.4)

#### Optional Dependencies
- `ansible>=4.0.0` - For Ansible integration
- `pytest>=7.0.0` - For running tests
- `black>=23.0.0` - For code formatting

## 🚀 Quick Installation

### Method 1: Direct Script Execution (Recommended for Development)

```bash
# Clone repository
git clone https://gitlab.com/company/ansible-inventory-cli.git
cd ansible-inventory-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python scripts/ansible_inventory_cli.py --version
python scripts/ansible_inventory_cli.py health
```

### Method 2: Package Installation

```bash
# Install from PyPI (when available)
pip install ansible-inventory-cli

# Or install from local package
pip install -e .

# Verify installation
ansible-inventory-cli --version
ansible-inventory-cli health
```

### Method 3: Docker Installation

```bash
# Build Docker image
docker build -t ansible-inventory-cli .

# Run container
docker run -it \
  -v $(pwd)/inventory:/app/inventory \
  -v $(pwd)/inventory_source:/app/inventory_source \
  ansible-inventory-cli health
```

## 🔧 Detailed Installation Instructions

### Linux/Ubuntu Installation

#### System Packages
```bash
# Update package manager
sudo apt update

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv git

# Install Ansible (optional)
sudo apt install -y ansible

# For development (optional)
sudo apt install -y make build-essential
```

#### Python Environment
```bash
# Create project directory
mkdir -p ~/ansible-inventory-cli
cd ~/ansible-inventory-cli

# Clone repository
git clone https://gitlab.com/company/ansible-inventory-cli.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install application
pip install -e ".[dev,test]"

# Verify installation
python scripts/ansible_inventory_cli.py health
```

### macOS Installation

#### Using Homebrew
```bash
# Install Python (if not already installed)
brew install python@3.10

# Install Git (if not already installed)
brew install git

# Install Ansible (optional)
brew install ansible

# Clone and set up
git clone https://gitlab.com/company/ansible-inventory-cli.git
cd ansible-inventory-cli
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

#### Using pyenv (Recommended for Multiple Python Versions)
```bash
# Install pyenv
curl https://pyenv.run | bash

# Install Python
pyenv install 3.10.12
pyenv local 3.10.12

# Continue with standard installation
git clone https://gitlab.com/company/ansible-inventory-cli.git
cd ansible-inventory-cli
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Windows Installation

#### Using PowerShell
```powershell
# Install Python from Microsoft Store or python.org
# Ensure Python is in PATH

# Clone repository
git clone https://gitlab.com/company/ansible-inventory-cli.git
cd ansible-inventory-cli

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -e .

# Test installation
python scripts/ansible_inventory_cli.py --version
```

#### Using Windows Subsystem for Linux (WSL)
```bash
# Install WSL Ubuntu
wsl --install -d Ubuntu

# Follow Linux installation instructions within WSL
```

### Docker Installation

#### Using Docker Hub (When Available)
```bash
# Pull image
docker pull company/ansible-inventory-cli:latest

# Run with volume mounts
docker run -it \
  -v $(pwd)/inventory:/app/inventory \
  -v $(pwd)/inventory_source:/app/inventory_source \
  -v $(pwd)/logs:/app/logs \
  company/ansible-inventory-cli:latest health
```

#### Building from Source
```bash
# Build image
docker build -t ansible-inventory-cli .

# Create docker-compose.yml for easier management
cat > docker-compose.yml << EOF
version: '3.8'
services:
  ansible-inventory-cli:
    build: .
    volumes:
      - ./inventory:/app/inventory
      - ./inventory_source:/app/inventory_source
      - ./logs:/app/logs
    environment:
      - LOG_LEVEL=INFO
EOF

# Run with docker-compose
docker-compose run ansible-inventory-cli health
```

## ⚙️ Configuration

### Initial Configuration

#### 1. Create Required Directories
```bash
mkdir -p inventory inventory/host_vars inventory/group_vars
mkdir -p inventory_source logs
```

#### 2. Configure CSV Source
```bash
# Copy sample CSV or create your own
cp inventory_source/hosts.csv.example inventory_source/hosts.csv

# Edit CSV with your infrastructure
nano inventory_source/hosts.csv
```

#### 3. Configure Ansible (Optional)
```bash
# Create ansible.cfg
cat > ansible.cfg << EOF
[defaults]
inventory = inventory
host_key_checking = False
stdout_callback = yaml

[inventory]
enable_plugins = yaml
EOF
```

#### 4. Set Environment Variables
```bash
# Create .env file (not committed to git)
cat > .env << EOF
LOG_LEVEL=INFO
ANSIBLE_HOST_KEY_CHECKING=False
COVERAGE_THRESHOLD=80
EOF

# Load environment variables
source .env
```

### Advanced Configuration

#### Custom Configuration File
```python
# scripts/local_config.py (optional override)
import os
from pathlib import Path

# Override default paths
CSV_FILE = Path(os.getenv('CUSTOM_CSV_PATH', 'inventory_source/hosts.csv'))
LOG_DIR = Path(os.getenv('CUSTOM_LOG_DIR', 'logs'))

# Override grace periods
GRACE_PERIODS = {
    'development': 7,    # 7 days
    'test': 14,         # 14 days  
    'staging': 21,      # 21 days
    'production': 90    # 90 days
}
```

## ✅ Verification & Testing

### Basic Verification
```bash
# Check version
python scripts/ansible_inventory_cli.py --version

# Test health check
python scripts/ansible_inventory_cli.py health

# Validate configuration
python scripts/ansible_inventory_cli.py validate

# Generate test inventory
python scripts/ansible_inventory_cli.py generate --environments test
```

### Integration Testing
```bash
# Test Ansible integration
ansible-inventory --inventory inventory/production.yml --list

# Test with ansible command
ansible all -i inventory/production.yml -m ping --limit 1

# Test lifecycle operations (dry run)
python scripts/ansible_inventory_cli.py lifecycle list-expired
```

### Performance Testing
```bash
# Time health check
time python scripts/ansible_inventory_cli.py health

# Memory usage test
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

## 🚨 Troubleshooting Installation

### Common Issues

#### 1. **Python Version Conflicts**
```bash
# Check Python version
python --version

# Use specific Python version
python3.10 -m venv venv

# Use pyenv for version management
pyenv install 3.10.12
pyenv local 3.10.12
```

#### 2. **Permission Errors**
```bash
# Use user install instead of system
pip install --user -e .

# Or fix permissions (Linux/macOS)
sudo chown -R $USER:$USER ~/.local/lib/python*
```

#### 3. **Missing System Dependencies**
```bash
# Ubuntu/Debian
sudo apt install -y python3-dev build-essential

# CentOS/RHEL
sudo yum install -y python3-devel gcc

# macOS
xcode-select --install
```

#### 4. **Ansible Integration Issues**
```bash
# Install Ansible separately
pip install ansible>=4.0.0

# Check Ansible configuration
ansible --version
ansible-config dump --only-changed

# Verify Python path
python -c "import ansible; print(ansible.__file__)"
```

#### 5. **CSV File Issues**
```bash
# Check file encoding
file -bi inventory_source/hosts.csv

# Convert encoding if needed
iconv -f windows-1252 -t utf-8 hosts.csv > hosts_utf8.csv

# Validate CSV format
python -c "
import csv
with open('inventory_source/hosts.csv') as f:
    reader = csv.DictReader(f)
    print(f'Headers: {reader.fieldnames}')
    print(f'First row: {next(reader)}')
"
```

### Environment-Specific Issues

#### Windows-Specific
```powershell
# Enable long path support
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

# Fix line ending issues
git config --global core.autocrlf true
```

#### macOS-Specific
```bash
# Install Command Line Tools
xcode-select --install

# Fix SSL issues
/Applications/Python\ 3.10/Install\ Certificates.command
```

## 🔄 Upgrade Instructions

### Upgrading from Git
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -e ".[dev]" --upgrade

# Run migrations if needed
python scripts/ansible_inventory_cli.py validate
```

### Upgrading Package Installation
```bash
# Upgrade from PyPI
pip install --upgrade ansible-inventory-cli

# Or from local source
pip install -e . --upgrade
```

### Data Migration
```bash
# Backup existing data
python scripts/ansible_inventory_cli.py create-backup

# Validate after upgrade
python scripts/ansible_inventory_cli.py validate
python scripts/ansible_inventory_cli.py health
```

## 📦 Development Installation

### Full Development Setup
```bash
# Clone with all branches
git clone --recurse-submodules https://gitlab.com/company/ansible-inventory-cli.git
cd ansible-inventory-cli

# Install development dependencies
make install-dev

# Set up pre-commit hooks
pre-commit install

# Run development checks
make check
```

### IDE Configuration

#### Visual Studio Code
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"]
}
```

#### PyCharm
```
# Configure interpreter: File -> Settings -> Project -> Python Interpreter
# Select: ./venv/bin/python

# Configure code style: File -> Settings -> Editor -> Code Style -> Python
# Set: Black formatter, 88 character line length
```

## 🌐 Network Configuration

### Proxy Configuration
```bash
# Set proxy environment variables
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1,.company.com

# Configure pip
pip config set global.proxy http://proxy.company.com:8080
```

### Firewall Configuration
```bash
# Ensure access to:
# - GitLab: gitlab.com (HTTPS/443)
# - PyPI: pypi.org (HTTPS/443)
# - Ansible Galaxy: galaxy.ansible.com (HTTPS/443)
```

## 📞 Support

If you encounter issues during installation:

1. **Check the [Troubleshooting Guide](troubleshooting.md)**
2. **Review [FAQ](faq.md)**
3. **Search existing [GitLab Issues](https://gitlab.com/company/ansible-inventory-cli/-/issues)**
4. **Create a new issue** with:
   - OS and Python version
   - Installation method attempted
   - Complete error message
   - Steps to reproduce

---

**Ready to start using the CLI? Check out the [User Guide](../USER_GUIDE.md)! 🚀** 