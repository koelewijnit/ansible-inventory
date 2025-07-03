# Makefile Reference

This document provides a comprehensive reference for all available Makefile commands in the Ansible Inventory Management System.

## Overview

The Makefile provides convenient shortcuts for common operations, development tasks, and CI/CD processes. All commands are designed to be safe and provide clear feedback about what they do.

## Quick Start

```bash
# Show all available commands
make help

# Generate inventory from CSV
make generate

# Validate inventory structure
make validate

# Run health check
make health-check
```

## Inventory Management Commands

### Basic Generation

#### `make generate`
Generate inventory from CSV with automatic cleanup of orphaned host_vars files.

```bash
make generate
```

**What it does:**
- Reads `inventory_source/hosts.csv`
- Generates inventory files for all environments
- Creates host_vars files for active hosts
- Automatically removes orphaned host_vars files
- Provides progress feedback

**Use when:**
- Regular inventory updates
- After CSV changes
- Before Ansible playbook runs

#### `make generate-dry-run`
Show what would be generated without making changes.

```bash
make generate-dry-run
```

**What it does:**
- Simulates inventory generation
- Shows what files would be created/modified
- No actual changes are made
- Safe for testing

**Use when:**
- Testing CSV changes
- Verifying configuration
- Before making actual changes

#### `make generate-fresh`
**⚠️ DESTRUCTIVE** - Remove ALL host_vars and regenerate from CSV.

```bash
make generate-fresh
```

**What it does:**
- Prompts for confirmation
- Removes ALL host_vars files
- Regenerates everything from CSV
- Complete fresh start

**Use when:**
- Major CSV restructuring
- Cleaning up corrupted host_vars
- Troubleshooting inventory issues
- **Use with caution!**

### Validation and Health

#### `make validate`
Validate inventory structure and Ansible compatibility.

```bash
make validate
```

**What it does:**
- Tests all inventory files with `ansible-inventory`
- Validates YAML syntax
- Checks group structure
- Verifies host_vars accessibility

**Use when:**
- After inventory generation
- Before Ansible playbook runs
- Troubleshooting inventory issues

#### `make health-check`
Run comprehensive inventory health check.

```bash
make health-check
```

**What it does:**
- Analyzes inventory statistics
- Checks for orphaned files
- Validates CSV structure
- Reports inventory health metrics

**Use when:**
- Regular maintenance
- Troubleshooting
- Performance monitoring

#### `make inventory-stats`
Show detailed inventory statistics.

```bash
make inventory-stats
```

**What it does:**
- Displays host counts by environment
- Shows group statistics
- Reports generation metrics
- Provides inventory overview

## Development Commands

### Installation

#### `make install`
Install the package in development mode.

```bash
make install
```

**What it does:**
- Installs package with `pip install -e .`
- Makes scripts available system-wide
- Enables development mode

#### `make install-dev`
Install with development dependencies.

```bash
make install-dev
```

**What it does:**
- Installs package with dev/test dependencies
- Sets up pre-commit hooks
- Configures development environment

#### `make setup-dev`
Set up complete development environment.

```bash
make setup-dev
```

**What it does:**
- Creates virtual environment
- Provides activation instructions
- Prepares for development

### Code Quality

#### `make lint`
Run all linting tools.

```bash
make lint
```

**What it does:**
- Runs flake8 for style checking
- Runs mypy for type checking
- Runs bandit for security scanning
- Runs yamllint for YAML validation

#### `make format`
Format code with black and isort.

```bash
make format
```

**What it does:**
- Formats Python code with black
- Sorts imports with isort
- Applies consistent style

#### `make format-check`
Check if code is properly formatted.

```bash
make format-check
```

**What it does:**
- Verifies black formatting
- Checks import sorting
- Fails if formatting is incorrect

#### `make security`
Run security checks.

```bash
make security
```

**What it does:**
- Runs bandit security scan
- Runs safety check for vulnerabilities
- Generates security report
- Provides security summary

### Testing

#### `make test`
Run all tests.

```bash
make test
```

**What it does:**
- Runs pytest with verbose output
- Executes all test suites
- Reports test results

#### `make test-cov`
Run tests with coverage reporting.

```bash
make test-cov
```

**What it does:**
- Runs tests with coverage
- Generates HTML coverage report
- Shows missing coverage

#### `make test-unit`
Run unit tests only.

```bash
make test-unit
```

#### `make test-integration`
Run integration tests only.

```bash
make test-integration
```

#### `make test-e2e`
Run end-to-end tests only.

```bash
make test-e2e
```

### Pre-commit

#### `make pre-commit`
Run pre-commit hooks.

```bash
make pre-commit
```

**What it does:**
- Runs all pre-commit hooks
- Checks staged files
- Ensures code quality

#### `make pre-commit-update`
Update pre-commit hooks.

```bash
make pre-commit-update
```

**What it does:**
- Updates hook versions
- Refreshes configurations
- Ensures latest checks

## CI/CD Commands

### CI Environment

#### `make ci-install`
Install for CI environment.

```bash
make ci-install
```

**What it does:**
- Installs with dev/test dependencies
- Optimized for CI environments
- Minimal dependencies

#### `make ci-test`
Run tests in CI environment.

```bash
make ci-test
```

**What it does:**
- Runs tests with coverage
- Generates XML coverage report
- Optimized for CI output

#### `make ci-lint`
Run linting in CI environment.

```bash
make ci-lint
```

**What it does:**
- Runs all linting tools
- Generates report files
- Optimized for CI processing

### Build and Distribution

#### `make build`
Build distribution packages.

```bash
make build
```

**What it does:**
- Cleans build artifacts
- Builds source and wheel distributions
- Creates distributable packages

#### `make build-wheel`
Build wheel package only.

```bash
make build-wheel
```

**What it does:**
- Builds wheel distribution
- Faster than full build
- Optimized for wheel-only needs

#### `make clean`
Clean build artifacts.

```bash
make clean
```

**What it does:**
- Removes build directories
- Cleans cache files
- Removes temporary files
- Resets to clean state

## Utility Commands

### Backup and Recovery

#### `make csv-backup`
Create CSV backup.

```bash
make csv-backup
```

**What it does:**
- Creates timestamped backup
- Preserves original file
- Provides backup confirmation

#### `make backup-all`
Create comprehensive backup.

```bash
make backup-all
```

**What it does:**
- Backs up all important files
- Creates timestamped backups
- Preserves project state

### Ansible Integration

#### `make ansible-check`
Check Ansible configuration.

```bash
make ansible-check
```

**What it does:**
- Verifies Ansible installation
- Shows Ansible version
- Displays configuration
- Validates setup

### Performance and Monitoring

#### `make perf-test`
Run performance tests.

```bash
make perf-test
```

**What it does:**
- Measures execution time
- Tests system performance
- Provides timing metrics

#### `make version`
Show current version.

```bash
make version
```

**What it does:**
- Displays package version
- Shows version information
- Useful for verification

## Import Commands

### External Inventory Import

#### `make import-dry-run`
Test import of external inventory.

```bash
make import-dry-run INVENTORY_FILE=/path/to/inventory.yml
```

**What it does:**
- Tests import process
- Shows what would be imported
- No actual changes made
- Safe for testing

#### `make import-inventory`
Import external inventory.

```bash
make import-inventory INVENTORY_FILE=/path/to/inventory.yml
```

**What it does:**
- Imports external inventory
- Creates new CSV file
- Preserves existing data
- Prompts for confirmation

#### `make import-inventory` (with host_vars)
Import with host_vars directory.

```bash
make import-inventory INVENTORY_FILE=/path/to/inventory.yml HOST_VARS_DIR=/path/to/host_vars/
```

**What it does:**
- Imports inventory and host_vars
- Creates complete CSV structure
- Includes all variables
- Comprehensive import

#### `make import-help`
Show import usage examples.

```bash
make import-help
```

**What it does:**
- Displays import examples
- Shows command syntax
- Provides usage guidance

## Quality Assurance

#### `make check`
Run all quality checks.

```bash
make check
```

**What it does:**
- Runs format check
- Runs linting
- Runs tests
- Comprehensive validation

## Command Categories

### Safe Commands (No Data Loss)
- `make help`
- `make generate-dry-run`
- `make validate`
- `make health-check`
- `make inventory-stats`
- `make test` (all variants)
- `make lint`
- `make format-check`
- `make security`
- `make version`
- `make import-dry-run`
- `make import-help`

### Development Commands
- `make install`
- `make install-dev`
- `make setup-dev`
- `make format`
- `make pre-commit`
- `make pre-commit-update`
- `make clean`
- `make build`
- `make build-wheel`

### Data Modification Commands
- `make generate` (safe, auto-cleans orphaned files)
- `make csv-backup`
- `make backup-all`
- `make import-inventory` (with confirmation)

### Destructive Commands (Use with Caution)
- `make generate-fresh` (removes ALL host_vars)
- `make clean` (removes build artifacts)

## Environment Variables

Some commands support environment variable overrides:

```bash
# Override CSV file location
export INVENTORY_CSV_FILE="/path/to/custom/hosts.csv"
make generate

# Override inventory file for import
make import-dry-run INVENTORY_FILE=/path/to/inventory.yml

# Override host_vars directory for import
make import-inventory INVENTORY_FILE=/path/to/inventory.yml HOST_VARS_DIR=/path/to/host_vars/
```

## Best Practices

### Daily Operations
1. **Regular Generation**: Use `make generate` for routine updates
2. **Validation**: Always run `make validate` after generation
3. **Health Checks**: Use `make health-check` for monitoring
4. **Backup**: Use `make csv-backup` before major changes

### Development Workflow
1. **Setup**: Use `make setup-dev` for new environments
2. **Quality**: Run `make check` before commits
3. **Formatting**: Use `make format` for consistent code
4. **Testing**: Use `make test-cov` for comprehensive testing

### Troubleshooting
1. **Dry Run**: Always use `make generate-dry-run` first
2. **Validation**: Use `make validate` to check inventory
3. **Health Check**: Use `make health-check` for diagnostics
4. **Fresh Start**: Use `make generate-fresh` as last resort

### CI/CD Integration
1. **Install**: Use `make ci-install` for CI environments
2. **Test**: Use `make ci-test` for automated testing
3. **Lint**: Use `make ci-lint` for code quality checks
4. **Build**: Use `make build` for distribution packages

## Error Handling

### Common Issues

#### Permission Errors
```bash
# Fix file permissions
chmod 644 inventory_source/hosts.csv
chmod -R 755 inventory/
```

#### Missing Dependencies
```bash
# Install development dependencies
make install-dev
```

#### Format Issues
```bash
# Fix code formatting
make format
```

#### Validation Failures
```bash
# Check inventory structure
make validate
make health-check
```

## Exit Codes

- **0**: Success
- **1**: Command error (validation failed, invalid input)
- **2**: File not found
- **3**: Unexpected error

## Getting Help

```bash
# Show all commands
make help

# Show specific command help
make import-help

# Check command documentation
make --help
```

## Integration with Other Tools

### Git Hooks
```bash
# Install pre-commit hooks
make install-dev

# Run pre-commit manually
make pre-commit
```

### CI/CD Pipelines
```bash
# CI installation
make ci-install

# CI testing
make ci-test

# CI linting
make ci-lint
```

### IDE Integration
```bash
# Format on save (configure in IDE)
make format

# Lint on save (configure in IDE)
make lint
```

---

**Note**: All commands provide clear feedback and are designed to be safe. Destructive commands require explicit confirmation before execution. 