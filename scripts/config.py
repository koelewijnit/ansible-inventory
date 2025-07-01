#!/usr/bin/env python3
"""
Centralized Configuration for Ansible Inventory Management Scripts

This module contains all configurable values used across the inventory management
scripts. Modify values here to change behavior across all scripts.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Version information
VERSION: str = "2.0.0"

# Logging configuration
LOG_LEVEL: str = "INFO"

# Project structure
PROJECT_ROOT: Path = Path(__file__).parent.parent
SCRIPT_DIR: Path = Path(__file__).parent

# Core paths
INVENTORY_SOURCE_DIR: Path = PROJECT_ROOT / "inventory_source"
INVENTORY_DIR: Path = PROJECT_ROOT / "inventory"
HOST_VARS_DIR: Path = INVENTORY_DIR / "host_vars"
GROUP_VARS_DIR: Path = INVENTORY_DIR / "group_vars"
BACKUP_DIR: Path = PROJECT_ROOT / "backups"

# Primary data file
CSV_FILE: Path = INVENTORY_SOURCE_DIR / "hosts.csv"

# File patterns and extensions
YAML_EXTENSION: str = ".yml"
BACKUP_EXTENSION: str = ".backup"
CSV_EXTENSION: str = ".csv"

# Environment configuration
ENVIRONMENTS: List[str] = ["production", "development", "test", "acceptance"]
ENVIRONMENT_CODES: Dict[str, str] = {
    "production": "prd",
    "development": "dev",
    "test": "tst",
    "acceptance": "acc",
}

# Host status values
VALID_STATUS_VALUES: List[str] = ["active", "decommissioned"]
DEFAULT_STATUS: str = "active"
DECOMMISSIONED_STATUS: str = "decommissioned"

# Group naming patterns
GROUP_PREFIXES: Dict[str, str] = {
    "application": "app_",
    "product": "product_",
    "environment": "env_",
}

# File naming patterns
INVENTORY_FILE_PATTERN: str = "{environment}.yml"
ENVIRONMENT_GROUP_VAR_PATTERN: str = "env_{environment}.yml"
HOST_VAR_FILE_PATTERN: str = "{hostname}.yml"

# Grace periods for host cleanup (days)
GRACE_PERIODS: Dict[str, int] = {
    "production": 90,
    "acceptance": 30,
    "test": 14,
    "development": 7,
}


# Patch management
PATCH_WINDOWS: Dict[str, str] = {
    "batch_1": "Saturday 02:00-04:00 UTC",
    "batch_2": "Saturday 04:00-06:00 UTC",
    "batch_3": "Saturday 06:00-08:00 UTC",
    "dev_batch": "Friday 18:00-20:00 UTC",
    "test_batch": "Friday 20:00-22:00 UTC",
    "acc_batch": "Friday 22:00-24:00 UTC",
}


# CMDB settings
DEFAULT_SUPPORT_GROUP: str = "TCS Compute Support Group"
DATE_FORMAT: str = "%Y-%m-%d"
TIMESTAMP_FORMAT: str = "%Y%m%d_%H%M%S"


# Display settings
CONSOLE_WIDTH: int = 60
TREE_MAX_DEPTH: int = 3


# File headers and comments
AUTO_GENERATED_HEADER: str = "AUTO-GENERATED FILE - DO NOT EDIT MANUALLY"
HOST_VARS_HEADER: str = (
    "Generated from enhanced CSV with CMDB and patch management fields"
)


# Required directories for validation
REQUIRED_DIRECTORIES: List[Path] = [INVENTORY_DIR, GROUP_VARS_DIR, HOST_VARS_DIR]


# Expected environment files
EXPECTED_ENV_FILES: List[str] = [f"env_{env}.yml" for env in ENVIRONMENTS]


# Inventory files to check for auto-generated headers
INVENTORY_FILES_TO_VALIDATE: List[str] = [f"{env}.yml" for env in ENVIRONMENTS] + [
    "decommissioned.yml"
]


# Command examples (for display purposes)
EXAMPLE_COMMANDS = {
    "list_hosts": "ansible-inventory --list",
    "show_structure": "ansible-inventory --graph",
    "regenerate": "python3 scripts/generate_inventory.py",
    "validate": "python3 scripts/validate_inventory_structure.py",
    "show_overview": "python3 scripts/show_inventory_structure.py",
}


def get_csv_file_path() -> Path:
    """Get the CSV file path."""
    return CSV_FILE


def get_available_csv_files() -> List[Path]:
    """Get list of available CSV files in inventory_source directory."""
    csv_files = []
    if INVENTORY_SOURCE_DIR.exists():
        for file in INVENTORY_SOURCE_DIR.glob("*.csv"):
            csv_files.append(file)
    return sorted(csv_files)


def validate_csv_file(csv_path: str) -> Tuple[bool, str]:
    """Validate that a CSV file exists and is readable."""
    path = Path(csv_path)
    if not path.exists():
        return False, f"File not found: {csv_path}"
    if not path.is_file():
        return False, f"Not a file: {csv_path}"
    if not csv_path.endswith(".csv"):
        return False, f"Not a CSV file: {csv_path}"
    try:
        with path.open("r", encoding="utf-8") as f:
            # Try to read first line to ensure it's readable
            f.readline()
        return True, "Valid CSV file"
    except Exception as e:
        return False, f"Cannot read file: {e}"


def get_inventory_file_path(environment: str) -> Path:
    """Get inventory file path for a specific environment."""
    return INVENTORY_DIR / INVENTORY_FILE_PATTERN.format(environment=environment)


def get_host_vars_file_path(hostname: str) -> Path:
    """Get host_vars file path for a specific hostname."""
    return HOST_VARS_DIR / HOST_VAR_FILE_PATTERN.format(hostname=hostname)


def get_backup_file_path(base_name: str, timestamp: Optional[str] = None) -> Path:
    """Get backup file path with timestamp."""
    if timestamp is None:
        from datetime import datetime

        timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)

    backup_name = f"{base_name}_backup_{timestamp}{CSV_EXTENSION}"
    return BACKUP_DIR / backup_name


def get_environment_group_var_path(environment: str) -> Path:
    """Get group_vars file path for environment."""
    filename = ENVIRONMENT_GROUP_VAR_PATTERN.format(environment=environment)
    return GROUP_VARS_DIR / filename


def validate_environment(environment: str) -> bool:
    """Validate if environment is in the allowed list."""
    return environment in ENVIRONMENTS


def get_patching_window(batch_number: str) -> str:
    """Get patching window for batch number."""
    return PATCH_WINDOWS.get(batch_number, "TBD")


def get_grace_period(environment: str) -> int:
    """Get grace period for environment."""
    return GRACE_PERIODS.get(environment, 30)


class ErrorMessages:
    """Centralized error messages for consistency."""

    CSV_NOT_FOUND = "❌ CSV file not found: {path}"
    INVALID_HOSTNAME = "❌ Invalid hostname: '{hostname}'"
    ENVIRONMENT_INVALID = (
        "❌ Invalid environment: '{env}'. Must be one of: {valid_envs}"
    )
    HOST_NOT_FOUND = "❌ Host '{hostname}' not found"
    PERMISSION_DENIED = "❌ Permission denied accessing: {path}"
    YAML_PARSE_ERROR = "❌ YAML parsing error in {file}: {error}"
    CONFIG_ERROR = "❌ Configuration error: {error}"
    VALIDATION_FAILED = "❌ Validation failed: {error}"

    @classmethod
    def format_error(cls, template: str, **kwargs) -> str:
        """Format error message with parameters."""
        return template.format(**kwargs)
