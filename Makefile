# Makefile for Ansible Inventory CLI
# =================================

.PHONY: help install install-dev test test-cov lint format security clean build docs pre-commit check health-check

# Default target
help: ## Show this help message
	@echo "Ansible Inventory CLI - Development Commands"
	@echo "==========================================="
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# Installation
install: ## Install the package
	pip install -e .

install-dev: ## Install development dependencies
	pip install -e ".[dev,test,docs]"
	pre-commit install

# Testing
test: ## Run tests
	pytest -v

test-cov: ## Run tests with coverage
	pytest --cov=scripts --cov-report=html --cov-report=term-missing -v

test-unit: ## Run unit tests only
	pytest tests/ -m "unit" -v

test-integration: ## Run integration tests only
	pytest tests/ -m "integration" -v

test-e2e: ## Run end-to-end tests only
	pytest tests/ -m "e2e" -v

# Code Quality
lint: ## Run all linting tools
	@echo "Running flake8..."
	flake8 scripts/
	@echo "Running mypy..."
	mypy scripts/
	@echo "Running bandit..."
	bandit -r scripts/
	@echo "Running yamllint..."
	yamllint inventory/ ansible.cfg

format: ## Format code with black and isort
	@echo "Running black..."
	black scripts/
	@echo "Running isort..."
	isort scripts/

format-check: ## Check if code is properly formatted
	@echo "Checking black formatting..."
	black --check scripts/
	@echo "Checking isort formatting..."
	isort --check-only scripts/

security: ## Run security checks
	@echo "Running bandit security scan..."
	bandit -r scripts/ -f json -o security-report.json
	@echo "Running safety check..."
	safety check
	@echo "Security scan complete!"

# Pre-commit
pre-commit: ## Run pre-commit hooks
	pre-commit run --all-files

pre-commit-update: ## Update pre-commit hooks
	pre-commit autoupdate

# Project Health
check: format-check lint test ## Run all quality checks
	@echo "All checks passed! ✅"

health-check: ## Run inventory health check
	@echo "Running inventory health check..."
	python scripts/ansible_inventory_cli.py health
	@echo ""
	@echo "📍 Geographic Locations Summary:"
	@python scripts/geographic_utils.py list | head -n 8

validate: ## Validate inventory structure
	@echo "Validating inventory structure..."
	ansible-inventory --inventory inventory/production.yml --list > /dev/null
	ansible-inventory --inventory inventory/development.yml --list > /dev/null
	ansible-inventory --inventory inventory/test.yml --list > /dev/null
	ansible-inventory --inventory inventory/acceptance.yml --list > /dev/null
	@echo "Inventory validation complete! ✅"

# Documentation
docs: ## Build documentation
	@echo "Building documentation..."
	@if [ -d "docs" ]; then \
		cd docs && mkdocs build; \
	else \
		echo "Documentation directory not found. Run 'mkdocs new docs' first."; \
	fi

docs-serve: ## Serve documentation locally
	@if [ -d "docs" ]; then \
		cd docs && mkdocs serve; \
	else \
		echo "Documentation directory not found. Run 'mkdocs new docs' first."; \
	fi

# Build and Distribution
clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf security-report.json
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

build: clean ## Build distribution packages
	python -m build

build-wheel: clean ## Build wheel package only
	python -m build --wheel

# Development Environment
setup-dev: ## Set up development environment
	@echo "Setting up development environment..."
	python -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"
	@echo "Then run: make install-dev"

# Ansible specific commands
ansible-check: ## Check Ansible playbook syntax
	@echo "Checking Ansible configuration..."
	ansible --version
	ansible-config dump --only-changed
	@echo "Ansible check complete! ✅"

inventory-stats: ## Show inventory statistics
	@echo "Inventory Statistics:"
	@echo "===================="
	python scripts/ansible_inventory_cli.py health --verbose

csv-backup: ## Create CSV backup
	python scripts/ansible_inventory_cli.py create-backup

# Inventory import functionality
import-dry-run: ## Test import of external inventory (requires INVENTORY_FILE)
	@if [ -z "$(INVENTORY_FILE)" ]; then \
		echo "Usage: make import-dry-run INVENTORY_FILE=/path/to/inventory.yml"; \
		exit 1; \
	fi
	python scripts/ansible_inventory_cli.py import --inventory-file "$(INVENTORY_FILE)" --dry-run

import-inventory: ## Import external inventory (requires INVENTORY_FILE)
	@if [ -z "$(INVENTORY_FILE)" ]; then \
		echo "Usage: make import-inventory INVENTORY_FILE=/path/to/inventory.yml"; \
		echo "Optional: make import-inventory INVENTORY_FILE=/path/to/inventory.yml HOST_VARS_DIR=/path/to/host_vars/"; \
		exit 1; \
	fi
	@echo "⚠️  WARNING: This will create a new CSV file with imported inventory data"
	@echo "Make sure to backup your existing CSV first!"
	@read -p "Continue? [y/N]: " confirm && [ "$$confirm" = "y" ] || exit 1
	python scripts/ansible_inventory_cli.py import --inventory-file "$(INVENTORY_FILE)" $(if $(HOST_VARS_DIR),--host-vars-dir "$(HOST_VARS_DIR)")

import-help: ## Show import usage examples
	@echo "🔄 INVENTORY IMPORT COMMANDS"
	@echo "============================"
	@echo ""
	@echo "Test import (dry run):"
	@echo "  make import-dry-run INVENTORY_FILE=/path/to/existing/inventory.yml"
	@echo ""
	@echo "Import with host_vars:"
	@echo "  make import-inventory INVENTORY_FILE=/path/to/inventory.yml HOST_VARS_DIR=/path/to/host_vars/"
	@echo ""
	@echo "Direct command usage:"
	@echo "  python scripts/ansible_inventory_cli.py import --help"
	@echo "  python scripts/inventory_import.py --help"

# Geographic location management
geo-list: ## List all geographic locations
	@echo "📍 Geographic Locations:"
	@python scripts/geographic_utils.py list

geo-lookup: ## Lookup a location (usage: make geo-lookup-<location>)
	@echo "📍 Location Lookup Examples:"
	@echo "  make geo-lookup-shanwei    # Legacy identifier"
	@echo "  make geo-lookup-shh        # Standard code"
	@echo "  make geo-lookup-norwalk    # Location name"

geo-lookup-%: ## Lookup specific location
	@echo "📍 Looking up location: $*"
	@python scripts/geographic_utils.py lookup $*

geo-validate-%: ## Validate specific location
	@echo "📍 Validating location: $*"
	@python scripts/geographic_utils.py validate $*

geo-convert-%: ## Convert location identifier
	@echo "📍 Converting location: $*"
	@python scripts/geographic_utils.py convert $*

# CI/CD helpers
ci-install: ## Install for CI environment
	pip install -e ".[dev,test]"

ci-test: ## Run tests in CI environment
	pytest --cov=scripts --cov-report=xml --cov-report=term-missing -v

ci-lint: ## Run linting in CI environment
	flake8 scripts/ --output-file=flake8-report.txt
	mypy scripts/ --xml-report=mypy-report
	bandit -r scripts/ -f json -o bandit-report.json

# Version management
version: ## Show current version
	@python -c "import scripts.config as config; print(f'Version: {getattr(config, \"VERSION\", \"unknown\")}')"

# Database/CSV operations
backup-all: ## Backup all important files
	@echo "Creating comprehensive backup..."
	python scripts/ansible_inventory_cli.py create-backup
	@echo "Backup complete! 💾"

# Performance testing
perf-test: ## Run performance tests
	@echo "Running performance tests..."
	time python scripts/ansible_inventory_cli.py health
	@echo "Performance test complete! ⚡" 