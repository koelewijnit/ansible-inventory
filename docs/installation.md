# Installation Guide

Complete installation guide for the Ansible Inventory Management System across different environments and use cases.

## 🎯 Installation Methods

Choose the installation method that best fits your environment:

| Method | Best For | Python Required |
|--------|----------|-----------------|
| **Direct Script** | Development, testing | ✅ 3.8+ |
| **Virtual Environment** | Production, isolation | ✅ 3.8+ |
| **System-wide** | Server deployment | ✅ 3.8+ |

## 📋 Prerequisites

### System Requirements

#### Minimum Requirements
- **OS**: Linux, macOS, Windows
- **Python**: 3.8 or higher (recommended: 3.10+)
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
- `pathlib2>=2.3.0` - Path handling compatibility

#### Optional Dependencies
- `ansible>=4.0.0` - For Ansible integration testing
- `pytest>=7.0.0` - For running tests
- `black>=23.0.0` - For code formatting
- `ruff>=0.1.0` - For linting

## 🚀 Quick Installation

### Method 1: Direct Script Execution (Recommended for Development)

```bash
# Clone repository
git clone <repository-url>
cd inventory-structure-new

# Install dependencies
pip install -r requirements.txt

# Verify installation
python scripts/ansible_inventory_cli.py --version
python scripts/ansible_inventory_cli.py health
```

### Method 2: Virtual Environment (Recommended for Production)

```bash
# Clone repository
git clone <repository-url>
cd inventory-structure-new

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
python scripts/ansible_inventory_cli.py --version
python scripts/ansible_inventory_cli.py health
```

### Method 3: System-wide Installation

```bash
# Clone repository
git clone <repository-url>
cd inventory-structure-new

# Install system-wide (requires sudo/admin)
sudo pip install -r requirements.txt

# Verify installation
python scripts/ansible_inventory_cli.py --version
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
mkdir -p ~/ansible-inventory
cd ~/ansible-inventory

# Clone repository
git clone <repository-url> .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install application
pip install -r requirements.txt

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
git clone <repository-url>
cd inventory-structure-new
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Using pyenv (Recommended for Multiple Python Versions)
```bash
# Install pyenv
curl https://pyenv.run | bash

# Install Python
pyenv install 3.10.12
pyenv local 3.10.12

# Continue with standard installation
git clone <repository-url>
cd inventory-structure-new
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows Installation

#### Using PowerShell
```powershell
# Install Python from Microsoft Store or python.org
# Ensure Python is in PATH

# Clone repository
git clone <repository-url>
cd inventory-structure-new

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Test installation
python scripts/ansible_inventory_cli.py --version
```

#### Using Windows Subsystem for Linux (WSL)
```bash
# Install WSL Ubuntu
wsl --install -d Ubuntu

# Follow Linux installation instructions within WSL
```

## ✅ Post-Installation Setup

### 1. Configuration
```bash
# Copy configuration template
cp inventory-config.yml.example inventory-config.yml

# Edit configuration for your environment
nano inventory-config.yml
```

### 2. Create Directory Structure
```bash
# Create required directories
mkdir -p inventory_source
mkdir -p inventory/group_vars
mkdir -p inventory/host_vars
mkdir -p logs
```

### 3. Initial CSV Setup
```bash
# Create CSV template
python scripts/ansible_inventory_cli.py validate --create-csv inventory_source/hosts.csv

# Edit CSV with your host data
nano inventory_source/hosts.csv
```

### 4. Environment Variables (Optional)
```bash
# Create .env file (not committed to git)
cat > .env << EOF
LOG_LEVEL=INFO
ANSIBLE_HOST_KEY_CHECKING=False
EOF

# Load environment variables
source .env
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
python scripts/ansible_inventory_cli.py generate --dry-run
```

### Integration Testing
```bash
# Test Ansible integration (if Ansible is installed)
ansible-inventory --inventory inventory/production.yml --list

# Test Makefile commands
make help
make validate
make generate
```

### Performance Testing
```bash
# Time health check
time python scripts/ansible_inventory_cli.py health

# Memory usage test
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

## 🚨 Troubleshooting Installation

### Common Issues

#### 1. **Python Version Issues**
```bash
# Check Python version
python --version
python3 --version

# If version is too old, install newer Python
# Ubuntu/Debian:
sudo apt install python3.10
# macOS:
brew install python@3.10
```

#### 2. **Permission Errors**
```bash
# Use virtual environment instead of system-wide
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or use user installation
pip install --user -r requirements.txt
```

#### 3. **Module Not Found Errors**
```bash
# Ensure you're in the project directory
cd inventory-structure-new

# Check Python path
python -c "import sys; print(sys.path)"

# Add project to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### 4. **Git Clone Issues**
```bash
# If using SSH and having issues, try HTTPS
git clone https://github.com/your-org/inventory-structure-new.git

# Or download ZIP if git is not available
curl -L https://github.com/your-org/inventory-structure-new/archive/main.zip -o inventory.zip
unzip inventory.zip
cd inventory-structure-new-main
```

#### 5. **Dependency Installation Issues**
```bash
# Clear pip cache
pip cache purge

# Upgrade pip
pip install --upgrade pip

# Install dependencies one by one
pip install PyYAML
pip install pathlib2

# Check for conflicting packages
pip check
```

### Environment-Specific Issues

#### Linux Issues
```bash
# Install additional packages if needed
sudo apt install python3-dev python3-distutils

# Fix locale issues
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
```

#### macOS Issues
```bash
# Install Xcode command line tools
xcode-select --install

# Fix OpenSSL issues
brew install openssl
export LDFLAGS="-L$(brew --prefix openssl)/lib"
export CPPFLAGS="-I$(brew --prefix openssl)/include"
```

#### Windows Issues
```powershell
# Install Visual C++ Build Tools if needed
# Download from Microsoft website

# Use Windows-specific paths
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"
```

## 📞 Getting Help

### Documentation
- **Getting Started**: [Getting Started Guide](getting-started.md)
- **Usage Guide**: [Usage Guide](usage.md)
- **FAQ**: [FAQ](faq.md)

### System Commands
```bash
# Get help for any command
python scripts/ansible_inventory_cli.py --help

# Show specific command help
python scripts/ansible_inventory_cli.py generate --help
python scripts/ansible_inventory_cli.py validate --help
python scripts/ansible_inventory_cli.py health --help
python scripts/ansible_inventory_cli.py lifecycle --help

# Show all Makefile commands
make help
```

### Support
- Check existing issues in the repository
- Create new issues with detailed error messages
- Include system information (OS, Python version, etc.)

---

**Ready to start using the system? Continue with the [Getting Started Guide](getting-started.md)! 🚀**
