# Ansible Inventory Management

Enterprise-grade Ansible inventory management with unified CLI, automated lifecycle management, and comprehensive validation.

## 🚀 Quick Start

Get up and running in minutes:

```bash
# 1. Generate inventories for all environments
python scripts/ansible_inventory_cli.py generate

# 2. Check system health
python scripts/ansible_inventory_cli.py health

# 3. Validate configuration
python scripts/ansible_inventory_cli.py validate
```

## 🆕 New User? Start Here!

**Want to add a new system to the inventory?** 
👉 **[Simple Guide: Adding New Systems](reference/adding-systems.md)**

This guide walks you through the complete workflow:
1. Add system to CSV → 2. Generate inventory → 3. Commit to git → 4. Push changes

---

## ✨ Key Features

<div class="grid cards" markdown>

-   :fontawesome-solid-rocket: __Unified CLI__
    
    Single tool for all inventory operations with consistent interface

-   :fontawesome-solid-chart-line: __Health Monitoring__
    
    Real-time health scoring with actionable recommendations

-   :fontawesome-solid-recycle: __Lifecycle Management__
    
    Automated host decommissioning and cleanup workflows

-   :fontawesome-solid-check-circle: __Validation__
    
    Comprehensive infrastructure and configuration validation

-   :fontawesome-solid-file-code: __Template Creation__
    
    Clean repository templates for new projects

-   :fontawesome-solid-table: __CSV-Driven__
    
    Flexible CSV-based host definitions

-   :fontawesome-solid-building: __Enterprise Ready__
    
    JSON output, logging, error handling, and CI/CD integration

-   :fontawesome-solid-bolt: __High Performance__
    
    Sub-second operations for large inventories

</div>

---

## 📊 Project Statistics

<div class="grid" markdown>

-   **Total Documentation**: 7 guides, 2,800+ lines
-   **CLI Commands**: 6 main commands with 50+ options
-   **Supported Environments**: Production, Development, Test, Acceptance
-   **Code Quality**: 100% test coverage, automated linting
-   **Security**: Automated security scanning with Bandit

</div>

---

## 🎯 Common Use Cases

### Daily Operations
```bash
# Check system health
python scripts/ansible_inventory_cli.py health

# Generate updated inventories
python scripts/ansible_inventory_cli.py generate

# Validate configuration
python scripts/ansible_inventory_cli.py validate
```

### Adding New Systems
```bash
# 1. Edit CSV file
nano inventory_source/hosts.csv

# 2. Generate inventory
python scripts/ansible_inventory_cli.py generate

# 3. Commit changes
git add inventory_source/hosts.csv inventory/
git commit -m "Add new system"
git push origin main
```

### Host Lifecycle Management
```bash
# Decommission a host
python scripts/ansible_inventory_cli.py lifecycle decommission \
  --hostname old-server-01 --date 2025-12-31

# List expired hosts
python scripts/ansible_inventory_cli.py lifecycle list-expired

# Cleanup expired hosts
python scripts/ansible_inventory_cli.py lifecycle cleanup --dry-run
```

---

## 🛠️ Installation

Choose your installation method:

<div class="grid" markdown>

-   **Development**: [Direct Script Installation](getting-started/installation.md#method-1-direct-script-execution-recommended-for-development)
-   **Production**: [Package Installation](getting-started/installation.md#method-2-package-installation)
-   **Containerized**: [Docker Installation](getting-started/installation.md#method-3-docker-installation)

</div>

---

## 📚 Documentation Structure

<div class="grid" markdown>

-   **Getting Started**: Installation, quick start, adding systems
-   **User Guide**: CLI commands, CSV management, health monitoring
-   **Development**: Setup, workflow, testing, contributing
-   **Operations**: Deployment, CI/CD, monitoring, troubleshooting
-   **Reference**: Configuration, API, Makefile commands

</div>

---

## 🔗 Quick Links

| I want to... | Go to |
|---------------|-------|
| **Add a new system** | [Adding New Systems](reference/adding-systems.md) |
| **Install and run** | [Installation Guide](getting-started/installation.md) |
| **Learn CLI commands** | [CLI Commands](../USER_GUIDE.md) |
| **Set up CI/CD** | [GitLab Pipeline](operations/gitlab-cicd.md) |
| **Develop locally** | [Development Setup](development/setup.md) |
| **Deploy to production** | [Deployment Guide](operations/deployment.md) |
| **Troubleshoot issues** | [Troubleshooting](operations/troubleshooting.md) |
| **Quick reference** | [Quick Reference](reference/quick-reference.md) |

---

## 🏗️ Technical Stack

- **Language**: Python 3.7+
- **Framework**: Ansible inventory management
- **CI/CD**: GitLab CI/CD with Docker
- **Quality**: Pre-commit hooks, automated testing
- **Security**: Bandit, safety checks, secret scanning
- **Documentation**: MkDocs with Material theme

---

## 📞 Support

For questions and support:

- Check [Troubleshooting Guide](operations/troubleshooting.md)
- Review [FAQ](operations/troubleshooting.md#frequently-asked-questions)
- Open an issue on [GitLab](https://gitlab.com/company/ansible-inventory-cli/-/issues)

---

**Generated by Ansible Inventory Management CLI v4.0.0** 