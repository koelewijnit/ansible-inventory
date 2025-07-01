# Development Setup & Workflow

Complete guide for setting up and working with the Ansible Inventory Management CLI in a development environment.

## 🚀 Quick Setup

### Prerequisites
- **Python 3.7+** (recommended: 3.10+)
- **Git** for version control
- **Ansible** (will be installed automatically)
- **Docker** (optional, for containerized workflows)

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://gitlab.com/company/ansible-inventory-cli.git
cd ansible-inventory-cli

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
make install-dev
```

### 2. Configure Pre-commit Hooks

```bash
# Install pre-commit hooks (automatically runs on commits)
pre-commit install

# Run hooks manually on all files
make pre-commit
```

### 3. Verify Installation

```bash
# Run health check to verify everything works
make health-check

# Run all quality checks
make check
```

## 🛠️ Development Workflow

### Daily Development Commands

```bash
# Format code
make format

# Run linting
make lint

# Run tests with coverage
make test-cov

# Validate Ansible configurations
make validate

# Run complete quality check
make check
```

### Development Environment Variables

Create `.env` file for local development:

```bash
# .env (not committed to repository)
ANSIBLE_HOST_KEY_CHECKING=False
ANSIBLE_STDOUT_CALLBACK=yaml
LOG_LEVEL=DEBUG
COVERAGE_THRESHOLD=80
```

## 📁 Project Structure

```
ansible-inventory-cli/
├── .github/
│   └── workflows/          # GitHub Actions (legacy)
├── docs/                   # Documentation
│   ├── README.md          # Documentation index
│   ├── gitlab-cicd.md     # CI/CD implementation guide
│   └── development.md     # This file
├── inventory/             # Ansible inventory files
│   ├── production.yml     # Production inventory
│   ├── development.yml    # Development inventory
│   ├── test.yml          # Test inventory
│   ├── acceptance.yml    # Acceptance inventory
│   ├── group_vars/       # Group variables
│   └── host_vars/        # Host-specific variables
├── inventory_source/      # Source data
│   └── hosts.csv         # Master host data (CSV format)
├── scripts/              # Main application code
│   ├── ansible_inventory_cli.py  # Main CLI application
│   ├── config.py         # Configuration settings
│   ├── models.py         # Data models
│   └── utils.py          # Utility functions
├── logs/                 # Application logs
├── tests/                # Test suite (to be created)
├── .gitlab-ci.yml        # GitLab CI/CD pipeline
├── .gitignore           # Git ignore patterns
├── .editorconfig        # Editor configuration
├── .pre-commit-config.yaml  # Pre-commit hooks
├── .yamllint.yml        # YAML linting rules
├── pyproject.toml       # Modern Python project config
├── setup.cfg            # Legacy Python project config
├── Makefile            # Development automation
├── LICENSE             # MIT license
├── README.md           # Project overview
├── USER_GUIDE.md       # User documentation
├── MIGRATION.md        # Legacy migration guide
└── requirements.txt    # Python dependencies
```

## 🧪 Testing Strategy

### Test Organization

```bash
tests/
├── unit/                # Unit tests
│   ├── test_models.py
│   ├── test_utils.py
│   └── test_cli.py
├── integration/         # Integration tests
│   ├── test_ansible_integration.py
│   └── test_end_to_end.py
├── performance/         # Performance tests
│   └── test_benchmarks.py
└── fixtures/           # Test data
    ├── sample_hosts.csv
    └── sample_inventory.yml
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test types
make test-unit
make test-integration

# Run performance tests
make perf-test
```

### Writing Tests

#### Unit Test Example

```python
# tests/unit/test_models.py
import pytest
from scripts.models import Host, InventoryStats

def test_host_creation():
    """Test Host model creation and validation."""
    host = Host(
        hostname='test-server-01',
        environment='test',
        location='us-east-1',
        role='web',
        status='active'
    )
    
    assert host.hostname == 'test-server-01'
    assert host.is_active()
    assert host.get_group_name() == 'test_web'

def test_inventory_stats():
    """Test InventoryStats calculation."""
    stats = InventoryStats(total_hosts=10, active_hosts=8)
    assert stats.get_summary() == "Generated 8/10 hosts"
```

#### Integration Test Example

```python
# tests/integration/test_cli.py
import subprocess
import json

def test_health_command():
    """Test CLI health command."""
    result = subprocess.run([
        'python', 'scripts/ansible_inventory_cli.py', 
        'health', '--output-format', 'json'
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    health_data = json.loads(result.stdout)
    assert 'health_score' in health_data
    assert health_data['health_score'] >= 0
```

## 🔧 Code Quality Standards

### Python Code Style

- **Formatter**: Black (88 character line length)
- **Import sorting**: isort (Black-compatible profile)
- **Linting**: flake8 with plugins
- **Type checking**: mypy with strict settings
- **Security**: bandit security linting

### Example Code Style

```python
from typing import List, Optional, Dict, Any
import logging
from pathlib import Path

class InventoryManager:
    """Manages Ansible inventory operations.
    
    Attributes:
        csv_file: Path to CSV source file
        logger: Configured logger instance
    """
    
    def __init__(self, csv_file: Optional[Path] = None) -> None:
        """Initialize inventory manager.
        
        Args:
            csv_file: Optional custom CSV file path
        """
        self.csv_file = csv_file or Path("inventory_source/hosts.csv")
        self.logger = logging.getLogger(__name__)
    
    def load_hosts(self, environment: Optional[str] = None) -> List[Dict[str, Any]]:
        """Load hosts from CSV source.
        
        Args:
            environment: Optional environment filter
            
        Returns:
            List of host dictionaries
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
        """
        if not self.csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
        
        # Implementation...
        return []
```

### YAML Style (Ansible)

```yaml
# inventory/production.yml
all:
  children:
    production:
      hosts:
        prd-web-use1-01:
          ansible_host: 10.1.1.10
          role: web_server
          environment: production
          location: us-east-1
        prd-db-use1-01:
          ansible_host: 10.1.1.20
          role: database
          environment: production
          location: us-east-1
```

## 🔄 Git Workflow

### Branch Strategy

```bash
main           # Production-ready code
├── develop    # Integration branch
├── feature/*  # Feature development
├── hotfix/*   # Production hotfixes
└── release/*  # Release preparation
```

### Commit Convention

```bash
# Format: type(scope): description

feat(cli): add health monitoring command
fix(csv): handle missing hostname gracefully  
docs(readme): update installation instructions
test(unit): add coverage for host validation
refactor(models): simplify host group logic
ci(gitlab): add security scanning stage
```

### Development Flow

```bash
# Create feature branch
git checkout -b feature/new-health-checks

# Make changes and commit
git add .
git commit -m "feat(health): add detailed health scoring"

# Push and create merge request
git push origin feature/new-health-checks
# Create MR in GitLab UI

# After review and approval, merge to develop
# Release process promotes from develop to main
```

## 🐛 Debugging & Troubleshooting

### Enable Debug Logging

```bash
# Set environment variable
export LOG_LEVEL=DEBUG

# Or use CLI flag
python scripts/ansible_inventory_cli.py --log-level DEBUG health
```

### Common Issues

#### 1. **Import Errors**
```bash
# Ensure proper Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or use development install
pip install -e .
```

#### 2. **Ansible Configuration**
```bash
# Check Ansible configuration
ansible-config dump --only-changed

# Verify inventory syntax
ansible-inventory --inventory inventory/production.yml --list
```

#### 3. **CSV File Issues**
```bash
# Validate CSV format
python -c "
import csv
with open('inventory_source/hosts.csv') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if not row.get('hostname'):
            print(f'Missing hostname on line {i+2}')
"
```

### Performance Profiling

```bash
# Profile script execution
python -m cProfile -o profile.stats scripts/ansible_inventory_cli.py health

# Analyze profile results
python -c "
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('tottime').print_stats(10)
"
```

## 📦 Dependency Management

### Adding Dependencies

```bash
# Add to pyproject.toml [project] dependencies
# Then install
pip install -e .

# For development dependencies, add to [project.optional-dependencies] dev
pip install -e ".[dev]"
```

### Updating Dependencies

```bash
# Update requirements.txt if needed
pip freeze > requirements.txt

# Security updates
safety check
pip-audit
```

## 🔒 Security Considerations

### Secrets Management

```bash
# Never commit secrets to repository
echo "*.secret" >> .gitignore
echo ".env" >> .gitignore

# Use environment variables
export ANSIBLE_VAULT_PASSWORD="secure_password"

# Or vault files
ansible-vault create secrets.yml
```

### Code Security

```bash
# Run security scans
make security

# Check for hardcoded secrets
pre-commit run detect-private-key --all-files

# Dependency vulnerabilities
safety check
```

## 🚀 Release Process

### Version Management

```bash
# Update version in pyproject.toml
version = "4.1.0"

# Create git tag
git tag -a v4.1.0 -m "Release version 4.1.0"
git push origin v4.1.0
```

### Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Run full test suite: `make check`
- [ ] Update documentation
- [ ] Create git tag
- [ ] Merge to main branch
- [ ] Monitor CI/CD pipeline
- [ ] Verify deployment

## 📞 Getting Help

### Documentation
- [Main README](../README.md) - Project overview
- [User Guide](../USER_GUIDE.md) - CLI usage
- [GitLab CI/CD](gitlab-cicd.md) - Pipeline documentation

### Community
- GitLab Issues - Bug reports and feature requests
- Merge Requests - Code contributions
- Wiki - Additional documentation

### Development Support
- Run `make help` for available commands
- Check `.pre-commit-config.yaml` for quality standards
- Review `pyproject.toml` for project configuration

---

**Happy coding! 🎉** 