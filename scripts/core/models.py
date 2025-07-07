#!/usr/bin/env python3
"""Data models for Ansible Inventory Management.

This module contains structured data models using dataclasses for type
safety, validation, and cleaner code organization.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Host:
    """Structured host data model with automatic validation.

    Supports dynamic product columns (product_1, product_2, etc.) for flexible
    product definitions. Each host can have 1 to N products as needed.
    """

    environment: str
    status: str = "active"
    hostname: Optional[str] = None
    application_service: Optional[str] = None
    site_code: Optional[str] = None
    instance: Optional[str] = None
    batch_number: Optional[str] = None
    patch_mode: Optional[str] = None
    dashboard_group: Optional[str] = None
    primary_application: Optional[str] = None
    function: Optional[str] = None
    ssl_port: Optional[str] = None
    decommission_date: Optional[str] = None
    cname: Optional[str] = None
    ansible_tags: Optional[str] = None
    # Dynamic product storage - supports product_1, product_2, etc.
    products: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate data after initialization."""
        self._validate_required_fields()
        self._validate_environment_and_status()
        self._validate_numeric_fields()
        self._validate_date_fields()
        self._validate_instance_field()
        self._clean_string_fields()
        self._clean_product_fields()

    def _validate_required_fields(self) -> None:
        """Validate that required fields are provided."""
        # Validate that at least hostname or cname is provided
        if not self.hostname and not self.cname:
            raise ValueError("Either hostname or cname is required")

        # If hostname is provided, validate it
        if self.hostname and not self.hostname.strip():
            raise ValueError("Hostname cannot be empty when provided")

        # If cname is provided, validate it
        if self.cname and not self.cname.strip():
            raise ValueError("CNAME cannot be empty when provided")

    def _validate_environment_and_status(self) -> None:
        """Validate environment and status fields."""
        from .config import (
            ENVIRONMENTS,
            VALID_PATCH_MODES,
            VALID_STATUS_VALUES,
            ErrorMessages,
        )

        if self.environment not in ENVIRONMENTS:
            raise ValueError(
                ErrorMessages.ENVIRONMENT_INVALID.format(
                    env=self.environment, valid_envs=", ".join(ENVIRONMENTS)
                )
            )

        if self.status not in VALID_STATUS_VALUES:
            raise ValueError(
                f"Invalid status: {self.status}. Must be one of: {VALID_STATUS_VALUES}"
            )

        if self.patch_mode and self.patch_mode not in VALID_PATCH_MODES:
            raise ValueError(
                f"Invalid patch_mode: {self.patch_mode}. "
                f"Must be one of: {VALID_PATCH_MODES}"
            )

    def _validate_numeric_fields(self) -> None:
        """Validate numeric fields."""
        if self.ssl_port:
            try:
                int(self.ssl_port)
            except ValueError:
                raise ValueError(
                    f"Invalid ssl_port: {self.ssl_port}. Must be an integer."
                )

        if self.batch_number:
            try:
                int(self.batch_number)
            except ValueError:
                raise ValueError(
                    f"Invalid batch_number: {self.batch_number}. Must be an integer."
                )

    def _validate_date_fields(self) -> None:
        """Validate date fields."""
        if self.decommission_date:
            try:
                datetime.strptime(self.decommission_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    f"Invalid decommission_date: {self.decommission_date}. "
                    f"Must be in YYYY-MM-DD format."
                )

    def _validate_instance_field(self) -> None:
        """Validate instance field."""
        if self.instance:
            # Allow 0 and positive integers without leading zeros
            if self.instance == "0" or re.fullmatch(r"[1-9]\d*", self.instance):
                pass  # Valid instance
            else:
                raise ValueError(
                    f"Invalid instance: {self.instance}. Must be a positive integer without leading zeros."
                )

    def _clean_string_fields(self) -> None:
        """Clean up string fields."""
        # Clean up required string fields
        if self.hostname:
            self.hostname = self.hostname.strip()
        self.environment = self.environment.strip()
        self.status = self.status.strip()

        # Clean up optional string fields
        optional_fields = [
            "application_service",
            "site_code",
            "instance",
            "batch_number",
            "patch_mode",
            "dashboard_group",
            "primary_application",
            "function",
            "decommission_date",
            "cname",
            "ansible_tags",
        ]

        for field_name in optional_fields:
            value = getattr(self, field_name)
            if value and isinstance(value, str):
                setattr(self, field_name, value.strip())

    def _clean_product_fields(self) -> None:
        """Clean up product fields."""
        cleaned_products = {}
        for key, value in self.products.items():
            if value and isinstance(value, str) and value.strip():
                cleaned_products[key] = value.strip()
        self.products = cleaned_products

    @property
    def ansible_tags_list(self) -> List[str]:
        """Get a list of Ansible tags for this host."""
        if not self.ansible_tags:
            return []
        return [tag.strip() for tag in self.ansible_tags.split(",") if tag.strip()]

    @property
    def is_decommissioned(self) -> bool:
        """Check if host is decommissioned."""
        return self.status == "decommissioned"

    @property
    def is_production(self) -> bool:
        """Check if host is in production environment."""
        return self.environment == "production"

    @property
    def is_active(self) -> bool:
        """Check if host is active."""
        return self.status == "active"

    def get_app_group_name(self) -> Optional[str]:
        """Get application group name for inventory."""
        if self.application_service:
            return f"app_{self.application_service}"
        return None

    def get_product_ids(self) -> List[str]:
        """Return a list of product IDs for this host.

        Returns all non-empty product values from dynamic product columns.
        Supports flexible product definitions using product_1, product_2, etc.

        Returns:
            List of product IDs (e.g., ["web", "analytics", "monitoring"])
        """
        return list(self.products.values())

    def get_product_group_names(self) -> List[str]:
        """Return all product group names for inventory.

        Creates group names in the format 'product_{product_id}' for each
        product associated with this host.

        Returns:
            List of product group names (e.g., ["product_web", "product_analytics"])
        """
        product_ids = self.get_product_ids()
        return [f"product_{product_id}" for product_id in product_ids]

    def has_product(self, product_id: str) -> bool:
        """Check if host has a specific product installed.

        Args:
            product_id: The product ID to check for

        Returns:
            True if the host has the specified product, False otherwise
        """
        return product_id.strip() in self.get_product_ids()

    def get_primary_product_id(self) -> Optional[str]:
        """Get the primary (first) product ID for this host.

        Returns the first product in the list, which is typically considered
        the primary product for the host.

        Returns:
            The primary product ID, or None if no products are defined
        """
        product_ids = self.get_product_ids()
        return product_ids[0] if product_ids else None

    def validate_products(self) -> List[str]:
        """Validate product configuration and return any issues.

        Checks for:
        - At least one product is defined
        - No duplicate products
        - Product column naming follows expected pattern

        Returns:
            List of validation error messages (empty if valid)
        """
        issues = []

        # Check if host has at least one product
        if not self.get_product_ids():
            issues.append(f"Host {self.hostname} has no products defined")

        # Check for duplicate products
        products = self.get_product_ids()
        if len(products) != len(set(products)):
            issues.append(f"Host {self.hostname} has duplicate products: {products}")

        # Check for gaps in product column numbering
        product_keys = sorted(self.products.keys())
        if product_keys:
            # Extract numbers from product_1, product_2, etc.
            numbers = []
            for key in product_keys:
                if key.startswith("product_"):
                    try:
                        num = int(key[8:])  # Remove "product_" prefix
                        numbers.append(num)
                    except ValueError:
                        issues.append(f"Invalid product column name: {key}")

            # Check for gaps in numbering
            if numbers and numbers != list(range(1, len(numbers) + 1)):
                issues.append(f"Product columns should be sequential: {product_keys}")

        return issues

    def get_inventory_key_value(self, key_type: str = "hostname") -> str:
        """Get the value to use as inventory key based on the key type."""
        if key_type == "cname":
            if self.cname:
                return self.cname
            elif self.hostname:
                return self.hostname
            else:
                raise ValueError(
                    "No valid inventory key found: neither cname nor hostname is available"
                )
        else:  # key_type == "hostname"
            if self.hostname:
                return self.hostname
            elif self.cname:
                return self.cname
            else:
                raise ValueError(
                    "No valid inventory key found: neither hostname nor cname is available"
                )

    def get_host_vars_filename(self, key_type: str = "hostname") -> str:
        """Return the host_vars filename based on the inventory key type."""
        return f"{self.get_inventory_key_value(key_type)}.yml"

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for CSV/YAML output.

        Includes all dynamic product columns in the output.
        """
        result = {
            "hostname": self.hostname or "",
            "environment": self.environment,
            "status": self.status,
            "application_service": self.application_service or "",
            "site_code": self.site_code or "",
            "instance": self.instance or "",
            "batch_number": self.batch_number or "",
            "patch_mode": self.patch_mode or "",
            "dashboard_group": self.dashboard_group or "",
            "primary_application": self.primary_application or "",
            "function": self.function or "",
            "ssl_port": self.ssl_port or "",
            "decommission_date": self.decommission_date or "",
            "cname": self.cname or "",
            "ansible_tags": self.ansible_tags or "",
        }

        # Add dynamic product columns
        result.update(self.products)

        # Add metadata
        result.update(self.metadata)

        return result

    @classmethod
    def from_csv_row(cls, row: Dict[str, str]) -> "Host":
        """Create Host from CSV row data with dynamic product column detection.

        Automatically detects any column starting with "product" and treats it
        as a product definition. Supports flexible CSV structures where hosts
        can have 1 to N products as needed.

        Args:
            row: Dictionary representing a CSV row

        Returns:
            Host object with all fields populated

        Example:
            CSV with single product:
                {"hostname": "host1", "environment": "production", "product_1": "web"}

            CSV with multiple products:
                {"hostname": "host1", "environment": "production",
                 "product_1": "web", "product_2": "analytics", "product_3": "monitoring"}
        """
        # Extract known fields
        known_fields = {
            "hostname",
            "environment",
            "status",
            "application_service",
            "site_code",
            "instance",
            "batch_number",
            "patch_mode",
            "dashboard_group",
            "primary_application",
            "function",
            "ssl_port",
            "decommission_date",
            "cname",
            "ansible_tags",
        }

        host_data: Dict[str, Any] = {}
        metadata: Dict[str, Any] = {}
        products: Dict[str, str] = {}

        for k, v in row.items():
            # Skip None keys (can happen with malformed CSV)
            if k is None:
                continue

            if isinstance(v, str):
                clean_value = v.strip() if v is not None else None
            else:
                clean_value = v

            # Handle dynamic product columns
            if k.startswith("product"):
                if clean_value:
                    products[k] = clean_value
            # Handle known fields
            elif k in known_fields:
                if k in ["hostname", "cname"] and not clean_value:
                    host_data[k] = None
                else:
                    host_data[k] = clean_value if clean_value is not None else ""
            else:
                metadata[k] = clean_value if clean_value is not None else ""

        # Add products to host_data
        host_data["products"] = products
        host_data["metadata"] = metadata

        return cls(**host_data)  # type: ignore[unreachable]


@dataclass
class ValidationResult:
    """Standardized validation result."""

    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add validation error."""
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str) -> None:
        """Add validation warning."""
        self.warnings.append(message)

    def has_issues(self) -> bool:
        """Check if there are any errors or warnings."""
        return bool(self.errors or self.warnings)

    def get_summary(self) -> str:
        """Get a summary of validation results."""
        if not self.has_issues():
            return "✅ Validation passed - no issues found"

        summary = []
        if self.errors:
            summary.append(f"❌ {len(self.errors)} error(s)")
        if self.warnings:
            summary.append(f"⚠️ {len(self.warnings)} warning(s)")

        return " | ".join(summary)


@dataclass
class InventoryStats:
    """Statistics about inventory generation."""

    total_hosts: int = 0
    active_hosts: int = 0
    decommissioned_hosts: int = 0
    environment_counts: Dict[str, int] = field(default_factory=dict)
    application_groups: int = 0
    product_groups: int = 0
    generation_time: float = 0.0
    orphaned_files_removed: int = 0

    def add_host(self, host: Host) -> None:
        """Add a host to the statistics."""
        self.total_hosts += 1

        if host.is_decommissioned:
            self.decommissioned_hosts += 1
        else:
            self.active_hosts += 1

        # Count by environment
        if host.environment not in self.environment_counts:
            self.environment_counts[host.environment] = 0
        self.environment_counts[host.environment] += 1

    def get_summary(self) -> str:
        """Get a summary of the statistics."""
        lines = [
            "📊 Inventory Statistics:",
            f"   Total hosts: {self.total_hosts}",
            f"   Active: {self.active_hosts}",
            f"   Decommissioned: {self.decommissioned_hosts}",
            f"   Application groups: {self.application_groups}",
            f"   Product groups: {self.product_groups}",
            f"   Generation time: {self.generation_time:.2f}s",
        ]

        if self.environment_counts:
            lines.append("   Environment breakdown:")
            for env, count in sorted(self.environment_counts.items()):
                lines.append(f"     {env}: {count}")

        return "\n".join(lines)


@dataclass(frozen=True)
class InventoryConfig:
    """Immutable configuration object for inventory management."""

    project_root: Path
    csv_file: Path
    inventory_dir: Path
    host_vars_dir: Path
    group_vars_dir: Path
    environments: List[str]
    valid_status_values: List[str]
    patch_windows: Dict[str, str]
    grace_periods: Dict[str, int]
    inventory_key: str = "hostname"

    @classmethod
    def create_default(cls, inventory_key: str = "hostname") -> "InventoryConfig":
        """Create default configuration."""
        project_root = Path(__file__).parent.parent.parent
        return cls(
            project_root=project_root,
            csv_file=project_root / "inventory_source" / "hosts.csv",
            inventory_dir=project_root / "inventory",
            host_vars_dir=project_root / "inventory" / "host_vars",
            group_vars_dir=project_root / "inventory" / "group_vars",
            environments=["production", "development", "test", "acceptance"],
            valid_status_values=["active", "decommissioned"],
            patch_windows={
                "batch_1": "Saturday 02:00-04:00 UTC",
                "batch_2": "Saturday 04:00-06:00 UTC",
                "batch_3": "Saturday 06:00-08:00 UTC",
                "dev_batch": "Friday 18:00-20:00 UTC",
                "test_batch": "Friday 20:00-22:00 UTC",
                "acc_batch": "Friday 22:00-24:00 UTC",
            },
            grace_periods={
                "production": 90,
                "acceptance": 30,
                "test": 14,
                "development": 7,
            },
            inventory_key=inventory_key,
        )

    def validate(self) -> ValidationResult:
        """Validate configuration."""
        result = ValidationResult()

        if not self.csv_file.exists():
            result.add_error(f"CSV file not found: {self.csv_file}")

        if not self.inventory_dir.exists():
            result.add_warning(f"Inventory directory not found: {self.inventory_dir}")

        if not self.host_vars_dir.exists():
            result.add_warning(f"Host vars directory not found: {self.host_vars_dir}")

        if not self.group_vars_dir.exists():
            result.add_warning(f"Group vars directory not found: {self.group_vars_dir}")

        # Validate environments
        for env in self.environments:
            env_file = self.group_vars_dir / f"env_{env}.yml"
            if not env_file.exists():
                result.add_warning(f"Environment file not found: {env_file}")

        return result

    def get_patching_window(self, batch_number: str) -> str:
        """Get patching window for batch number."""
        return self.patch_windows.get(batch_number, "TBD")

    def get_grace_period(self, environment: str) -> int:
        """Get grace period for environment."""
        return self.grace_periods.get(environment, 30)
