"""Core Infrastructure Package.

This package contains the fundamental infrastructure modules for the
Ansible Inventory Management System:

- config: Configuration constants and settings
- utils: Shared utility functions
- models: Data models and validation
"""

# Export commonly used items for easier importing
from .config import (
    CSV_FILE,
    DEFAULT_SUPPORT_GROUP,
    ENVIRONMENT_CODES,
    ENVIRONMENTS,
    GROUP_VARS_DIR,
    HOST_VARS_DIR,
    HOST_VARS_HEADER,
    INVENTORY_DIR,
    LOG_LEVEL,
    PROJECT_ROOT,
    VALID_PATCH_MODES,
    VALID_STATUS_VALUES,
    VERSION,
    ErrorMessages,
)
from .models import Host, InventoryConfig, InventoryStats, ValidationResult
from .utils import (
    create_backup_file,
    ensure_directory_exists,
    get_csv_template,
    get_hosts_by_environment,
    get_hosts_by_status,
    get_logger,
    load_csv_data,
    load_hosts_from_csv,
    save_yaml_file,
    setup_logging,
    test_ansible_inventory,
    validate_csv_headers,
    validate_csv_structure,
    validate_environment_decorator,
    validate_hostname_decorator,
)

__all__ = [
    # Config exports
    "VERSION",
    "LOG_LEVEL",
    "PROJECT_ROOT",
    "CSV_FILE",
    "DEFAULT_SUPPORT_GROUP",
    "ENVIRONMENTS",
    "ENVIRONMENT_CODES",
    "VALID_STATUS_VALUES",
    "INVENTORY_DIR",
    "HOST_VARS_DIR",
    "GROUP_VARS_DIR",
    "HOST_VARS_HEADER",
    "VALID_PATCH_MODES",
    "ErrorMessages",
    # Utils exports
    "get_logger",
    "setup_logging",
    "load_csv_data",
    "validate_hostname_decorator",
    "validate_environment_decorator",
    "validate_csv_headers",
    "validate_csv_structure",
    "get_csv_template",
    "load_hosts_from_csv",
    "get_hosts_by_environment",
    "get_hosts_by_status",
    "ensure_directory_exists",
    "create_backup_file",
    "save_yaml_file",
    "test_ansible_inventory",
    # Models exports
    "Host",
    "ValidationResult",
    "InventoryStats",
    "InventoryConfig",
]
