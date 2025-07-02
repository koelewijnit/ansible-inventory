#!/usr/bin/env python3
"""Utility functions for Ansible Inventory Management scripts.

This module contains shared functionality used across multiple inventory
management scripts to eliminate code duplication and ensure consistency.
"""

import csv
import logging
import os
import subprocess
import sys
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

from .models import ValidationResult

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent.absolute()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    from .config import (
        CSV_FILE,
        DATE_FORMAT,
        DEFAULT_STATUS,
        ENVIRONMENTS,
        GROUP_VARS_DIR,
        HOST_VARS_DIR,
        INVENTORY_DIR,
        PROJECT_ROOT,
        TIMESTAMP_FORMAT,
        VALID_STATUS_VALUES,
    )
except ImportError:
    # Fallback to direct configuration if config.py not available
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    CSV_FILE = PROJECT_ROOT / "inventory_source" / "hosts.csv"
    HOST_VARS_DIR = PROJECT_ROOT / "inventory" / "host_vars"
    INVENTORY_DIR = PROJECT_ROOT / "inventory"
    GROUP_VARS_DIR = INVENTORY_DIR / "group_vars"
    ENVIRONMENTS = ["production", "development", "test", "acceptance"]
    VALID_STATUS_VALUES = ["active", "decommissioned"]
    DEFAULT_STATUS = "active"
    DATE_FORMAT = "%Y-%m-%d"
    TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"


def get_logger(name: str) -> logging.Logger:
    """Get standardized logger for consistent output."""
    logger = logging.getLogger(name)
    if not logger.handlers:  # Avoid duplicate handlers
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def setup_logging(log_level: str = "INFO") -> None:
    """Set up logging configuration with specified level."""
    level = getattr(logging, log_level.upper(), logging.INFO)

    # Configure root logger
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
        force=True,  # Override existing configuration
    )


def load_csv_data(
    csv_file: Optional[Path] = None,
    required_fields: Optional[List[str]] = None,
    inventory_key: str = "hostname"
) -> List[Dict[str, str]]:
    """Load and validate CSV data with comprehensive error handling.

    Args:
        csv_file: Path to CSV file. Uses default if None.
        required_fields: Required field names to validate.
        inventory_key: Primary key to use for inventory ("hostname" or "cname").

    Returns:
        List of dictionaries representing CSV rows.

    Raises:
        FileNotFoundError: If CSV file doesn't exist.
        ValueError: If required fields are missing.
    """
    if csv_file is None:
        csv_file = CSV_FILE
    elif isinstance(csv_file, str):
        csv_file = Path(csv_file)

    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    try:
        with csv_file.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # Validate required fields
            if required_fields:
                missing_fields = set(required_fields) - set(reader.fieldnames or [])
                if missing_fields:
                    raise ValueError(f"Missing required CSV fields: {missing_fields}")

            # Load and filter data
            hosts: List[Dict[str, str]] = []
            for row_num, row in enumerate(
                reader, start=2
            ):  # Start at 2 (header is row 1)

                # Get the primary identifier based on inventory key
                hostname = row.get("hostname", "").strip()
                cname = row.get("cname", "").strip()

                # Skip comments and empty rows based on inventory key
                if inventory_key == "cname":
                    # When using cname as primary key, skip if neither cname nor hostname is provided
                    primary_id = cname or hostname
                    if not primary_id or primary_id.startswith("#"):
                        continue
                else:
                    # When using hostname as primary key, skip if hostname is empty
                    # but allow fallback to cname if hostname is not available
                    primary_id = hostname or cname
                    if not primary_id or primary_id.startswith("#"):
                        continue

                # Clean up all string values
                cleaned_row = {k: v.strip() if v else "" for k, v in row.items()}
                hosts.append(cleaned_row)

            return hosts

    except csv.Error as e:
        raise ValueError(f"CSV parsing error: {e}")


def validate_hostname_decorator(func: Any) -> Any:
    """Validate the hostname parameter before calling ``func``."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        hostname = kwargs.get("hostname") or (args[0] if args else None)
        if not hostname or not hostname.strip():
            raise ValueError("Hostname is required and cannot be empty")

        # Basic hostname validation
        hostname = hostname.strip()
        if len(hostname) > 63:
            raise ValueError("Hostname too long (max 63 characters)")

        if not hostname.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Hostname contains invalid characters")

        return func(*args, **kwargs)

    return wrapper


def validate_environment_decorator(func: Any) -> Any:
    """Validate the environment parameter before calling ``func``."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        environment = kwargs.get("environment")
        if environment and environment not in ENVIRONMENTS:
            raise ValueError(
                f"Invalid environment '{environment}'. "
                f"Must be one of: {', '.join(ENVIRONMENTS)}"
            )
        return func(*args, **kwargs)

    return wrapper


def load_hosts_from_csv(csv_file: Optional[str] = None) -> List[Dict[str, str]]:
    """Load all hosts from the CSV file.

    Args:
        csv_file: Path to CSV file. If None, uses default from config.

    Returns:
        List of host dictionaries
    """
    if csv_file is None:
        csv_file = str(CSV_FILE)

    hosts: List[Dict[str, str]] = []
    if not os.path.exists(csv_file):
        return hosts

    try:
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                hostname = row.get("hostname", "").strip()
                if hostname and not hostname.startswith("#"):
                    hosts.append(row)
    except Exception as e:
        print(f"Error reading CSV file {csv_file}: {e}")

    return hosts


def get_hosts_by_environment(
    environment: str, csv_file: Optional[str] = None
) -> List[Dict[str, str]]:
    """Get all hosts for a specific environment.

    Args:
        environment: Environment to filter by
        csv_file: Path to CSV file. If None, uses default from config.

    Returns:
        List of host dictionaries for the environment
    """
    all_hosts = load_hosts_from_csv(csv_file)
    return [
        host for host in all_hosts if host.get("environment", "").strip() == environment
    ]


def get_hosts_by_status(
    status: str, csv_file: Optional[str] = None
) -> List[Dict[str, str]]:
    """Get all hosts with a specific status.

    Args:
        status: Status to filter by (active, decommissioned)
        csv_file: Path to CSV file. If None, uses default from config.

    Returns:
        List of host dictionaries with the status
    """
    all_hosts = load_hosts_from_csv(csv_file)
    return [
        host
        for host in all_hosts
        if host.get("status", "").strip().lower() == status.lower()
    ]


def get_hostnames_from_csv(csv_file: Optional[str] = None) -> Set[str]:
    """Extract all hostnames from the CSV file.

    Args:
        csv_file: Path to CSV file. If None, uses default from config.

    Returns:
        Set of hostnames
    """
    hosts = load_hosts_from_csv(csv_file)
    return {host["hostname"] for host in hosts if host.get("hostname", "").strip()}


def get_host_vars_files() -> Set[str]:
    """Get all host_vars files (hostnames without .yml extension).

    Returns:
        Set of hostnames that have host_vars files
    """
    host_vars_files = set()

    if HOST_VARS_DIR.exists():
        for file_path in HOST_VARS_DIR.glob("*.yml"):
            hostname = file_path.stem
            host_vars_files.add(hostname)

    return host_vars_files


def find_orphaned_host_vars(csv_file: Optional[str] = None) -> Set[str]:
    """Find host_vars files that don't have corresponding entries in CSV.

    Args:
        csv_file: Path to CSV file. If None, uses default from config.

    Returns:
        Set of orphaned hostnames
    """
    csv_hosts = get_hostnames_from_csv(csv_file)
    host_vars_files = get_host_vars_files()
    return host_vars_files - csv_hosts


def validate_hostname(hostname: str) -> Optional[str]:
    """Validate hostname format.

    Args:
        hostname: Hostname to validate

    Returns:
        Error message if invalid, None if valid
    """
    if not hostname:
        return "Hostname cannot be empty"

    if len(hostname) > 63:
        return "Hostname too long (max 63 characters)"

    if not hostname.replace("-", "").replace("_", "").isalnum():
        return "Hostname contains invalid characters"

    return None


def validate_environment(environment: str) -> Optional[str]:
    """Validate environment value.

    Args:
        environment: Environment to validate

    Returns:
        Error message if invalid, None if valid
    """
    if environment not in ENVIRONMENTS:
        valid_envs = ", ".join(ENVIRONMENTS)
        return f"Invalid environment '{environment}'. Must be one of: {valid_envs}"

    return None


def validate_status(status: str) -> Optional[str]:
    """Validate status value.

    Args:
        status: Status to validate

    Returns:
        Error message if invalid, None if valid
    """
    if status not in VALID_STATUS_VALUES:
        valid_statuses = ", ".join(VALID_STATUS_VALUES)
        return f"Invalid status '{status}'. Must be one of: {valid_statuses}"

    return None


def validate_date_format(date_str: str) -> Optional[str]:
    """Validate date format.

    Args:
        date_str: Date string to validate

    Returns:
        Error message if invalid, None if valid
    """
    if not date_str:
        return None  # Empty dates are allowed

    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return None
    except ValueError:
        return f"Invalid date format '{date_str}'. Use {DATE_FORMAT}"


def run_ansible_command(
    args: List[str], cwd: Optional[str] = None
) -> Tuple[bool, str, str]:
    """Run an Ansible command and capture output.

    Args:
        args: List of command arguments (must be trusted input)
        cwd: Working directory

    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        # Only trusted input should be passed to subprocess.run
        result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def ensure_directory_exists(directory_path: str) -> None:
    """Ensure directory exists, creating it if necessary."""
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)


def test_ansible_inventory() -> Tuple[bool, str]:
    """Test if ansible-inventory command works.

    Returns:
        Tuple of (success, error_message)
    """
    success, stdout, stderr = run_ansible_command(["ansible-inventory", "--list"])

    if not success:
        return False, f"ansible-inventory failed: {stderr}"

    # Check if output is valid JSON
    try:
        import json

        json.loads(stdout)
        return True, ""
    except json.JSONDecodeError:
        return False, "ansible-inventory output is not valid JSON"


def create_backup_file(source_file: str, backup_dir: Optional[str] = None) -> str:
    """Create a timestamped backup of a file.

    Args:
        source_file: Path to file to backup
        backup_dir: Directory for backup. If None, uses source directory.

    Returns:
        Path to backup file
    """
    import shutil

    source_path = Path(source_file)

    if backup_dir is None:
        backup_dir_path = source_path.parent
    else:
        backup_dir_path = Path(backup_dir)
        backup_dir_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    backup_name = f"{source_path.stem}_backup_{timestamp}{source_path.suffix}"
    backup_path = backup_dir_path / backup_name

    shutil.copy2(source_file, backup_path)
    return str(backup_path)


def save_yaml_file(
    data: Dict, file_path: str, header_comment: Optional[str] = None
) -> None:
    """Save data to a YAML file with optional header comment.

    Args:
        data: Data to save
        file_path: Path to save file
        header_comment: Optional header comment
    """
    path_obj = Path(file_path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    with open(path_obj, "w") as f:
        f.write("---\n")
        if header_comment:
            f.write(f"# {header_comment}\n")
            f.write("\n")
        yaml.dump(data, f, default_flow_style=False, sort_keys=True)


def load_yaml_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Load data from a YAML file.

    Args:
        file_path: Path to YAML file

    Returns:
        Loaded data or None if file doesn't exist or can't be read
    """
    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else None
    except (FileNotFoundError, yaml.YAMLError):
        return None


def format_console_output(title: str, content: List[str], width: int = 60) -> str:
    """Format console output with title and content.

    Args:
        title: Title to display
        content: List of content lines
        width: Console width for separator

    Returns:
        Formatted output string
    """
    output = [title, "=" * width]
    output.extend(content)
    return "\n".join(output)


def print_summary_table(headers: List[str], rows: List[List[str]]) -> None:
    """Print a formatted table with headers and rows.

    Args:
        headers: Column headers
        rows: Data rows
    """
    if not rows:
        return

    # Calculate column widths
    col_widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    # Print header
    header_row = " | ".join(
        header.ljust(col_widths[i]) for i, header in enumerate(headers)
    )
    print(header_row)
    print("-" * len(header_row))

    # Print rows
    for row in rows:
        data_row = " | ".join(
            str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)
        )
        print(data_row)


def get_file_age_days(file_path: str) -> Optional[int]:
    """Get the age of a file in days.

    Args:
        file_path: Path to file

    Returns:
        Age in days or None if file doesn't exist
    """
    try:
        file_stat = os.stat(file_path)
        file_time = datetime.fromtimestamp(file_stat.st_mtime)
        age = datetime.now() - file_time
        return age.days
    except (OSError, FileNotFoundError):
        return None


def validate_csv_headers(
    csv_file: Path, expected_headers: List[str]
) -> ValidationResult:
    """Validate CSV headers against expected fields.

    Args:
        csv_file: Path to CSV file
        expected_headers: List of expected header names

    Returns:
        ValidationResult with any issues found
    """
    result = ValidationResult()

    try:
        with csv_file.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            actual_headers = reader.fieldnames or []

            # Check for missing required headers
            missing_headers = set(expected_headers) - set(actual_headers)
            if missing_headers:
                result.add_error(
                    f"Missing required headers: {', '.join(sorted(missing_headers))}"
                )

            # Check for unexpected headers (warnings)
            unexpected_headers = set(actual_headers) - set(expected_headers)
            if unexpected_headers:
                unexpected_list = ", ".join(sorted(unexpected_headers))
                result.add_warning(
                    f"Unexpected headers (will be ignored): {unexpected_list}"
                )

            # Check for case-insensitive matches
            actual_lower = {h.lower(): h for h in actual_headers}

            case_mismatches = []
            for expected in expected_headers:
                if (
                    expected.lower() in actual_lower
                    and expected != actual_lower[expected.lower()]
                ):
                    case_mismatches.append(
                        f"'{expected}' vs '{actual_lower[expected.lower()]}'"
                    )

            if case_mismatches:
                result.add_warning(
                    f"Case mismatches found: {', '.join(case_mismatches)}"
                )

    except Exception as e:
        result.add_error(f"Error reading CSV file: {e}")

    return result


def validate_csv_structure(csv_file: Path) -> ValidationResult:
    """Perform comprehensive CSV validation.

    Args:
        csv_file: Path to the CSV file to validate.

    Returns:
        ValidationResult with detailed validation results.
    """
    from .models import Host
    from .config import get_csv_template_headers

    result = ValidationResult()

    # Expected headers from configuration
    expected_headers = get_csv_template_headers()

    # Validate headers first
    header_validation = validate_csv_headers(csv_file, expected_headers)
    result.errors.extend(header_validation.errors)
    result.warnings.extend(header_validation.warnings)

    if not result.is_valid:
        return result

    # Validate data rows
    try:
        with csv_file.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            row_errors = []
            valid_rows = 0
            total_rows = 0

            for row_num, row in enumerate(reader, start=2):
                total_rows += 1
                hostname = row.get("hostname", "").strip()

                # Skip empty rows and comments
                if not hostname or hostname.startswith("#"):
                    continue

                try:
                    # Try to create Host object (this validates all fields)
                    Host.from_csv_row(row)
                    valid_rows += 1
                except ValueError as e:
                    row_errors.append(f"Row {row_num} ({hostname}): {e}")
                except Exception as e:
                    row_errors.append(
                        f"Row {row_num} ({hostname}): Unexpected error - {e}"
                    )

            # Add summary
            if row_errors:
                result.errors.extend(row_errors)
                result.add_error(
                    f"CSV validation failed: {len(row_errors)} invalid rows "
                    f"out of {total_rows} total rows"
                )
            else:
                result.add_warning(
                    f"CSV validation passed: {valid_rows} valid rows processed"
                )

    except Exception as e:
        result.add_error(f"Error reading CSV file: {e}")

    return result


def get_csv_template() -> str:
    """Get a CSV template with all required headers and example data.

    Headers are loaded from configuration and organized logically:
    - Required fields first (hostname, environment, status)
    - Identity fields (cname, instance)
    - Infrastructure fields (site_code, ssl_port)
    - Application fields (application_service, product_id, primary_application, function)
    - Operational fields (batch_number, patch_mode, dashboard_group)
    - Lifecycle fields (decommission_date)

    Returns:
        String containing CSV template
    """
    from .config import get_csv_template_headers, ENVIRONMENTS, VALID_STATUS_VALUES, VALID_PATCH_MODES

    headers = get_csv_template_headers()
    header_line = ",".join(headers)

    return (
        f"{header_line}\n"
        "# Example hosts (remove # to activate):\n"
        "# prd-web-use1-01,production,active,,1,us-east-1,443,"
        "web,webapp,WebApp,frontend,1,auto,Web,\n"
        "# dev-db-use1-01,development,active,,2,us-east-1,5432,"
        "db,postgres,Database,backend,2,manual,DB,\n"
        "# tst-app-use1-01,test,active,,3,us-east-1,8080,"
        "app,appsvc,AppService,api,3,auto,API,\n"
        "# acc-mon-use1-01,acceptance,active,,4,us-east-1,9090,"
        "monitoring,mon,Monitoring,infra,4,manual,Monitoring,\n\n"
        "# Required fields: hostname, environment, status\n"
        "# Optional fields: all others\n"
        "# Data types: instance, batch_number, and ssl_port must be integers\n"
        f"# Status values: {', '.join(VALID_STATUS_VALUES)}\n"
        f"# Environment values: {', '.join(ENVIRONMENTS)}\n"
        f"# Patch modes: {', '.join(VALID_PATCH_MODES)}\n"
    )


def create_csv_file(file_path: Path, overwrite: bool = False) -> bool:
    """Create a new CSV file with template content.

    Args:
        file_path: Path where to create the CSV file
        overwrite: Whether to overwrite existing file

    Returns:
        True if file was created successfully, False otherwise
    """
    try:
        # Check if file exists and handle overwrite
        if file_path.exists() and not overwrite:
            raise FileExistsError(
                f"File {file_path} already exists. Use --overwrite to replace it."
            )

        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Get template content
        template_content = get_csv_template()

        # Write the file
        with file_path.open("w", encoding="utf-8") as f:
            f.write(template_content)

        return True

    except Exception as e:
        raise ValueError(f"Failed to create CSV file: {e}")
