#!/usr/bin/env python3
"""
Data Models for Ansible Inventory Management

This module contains structured data models using dataclasses for type safety,
validation, and cleaner code organization.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Host:
    """Structured host data model with automatic validation."""

    hostname: str
    environment: str
    status: str = "active"
    application_service: Optional[str] = None
    product_id: Optional[str] = None
    location: Optional[str] = None
    instance: Optional[str] = None
    batch_number: Optional[str] = None
    patch_mode: Optional[str] = None
    dashboard_group: Optional[str] = None
    primary_application: Optional[str] = None
    function: Optional[str] = None
    ssl_port: Optional[str] = None
    decommission_date: Optional[str] = None
    cname: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate data after initialization."""
        from config import ENVIRONMENTS, VALID_STATUS_VALUES, ErrorMessages

        if not self.hostname or not self.hostname.strip():
            raise ValueError("Hostname is required")

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

        # Clean up string fields
        self.hostname = self.hostname.strip()
        self.environment = self.environment.strip()
        self.status = self.status.strip()

        # Clean up optional string fields
        for field_name in [
            "application_service",
            "product_id",
            "location",
            "instance",
            "batch_number",
            "patch_mode",
            "dashboard_group",
            "primary_application",
            "function",
            "decommission_date",
            "cname",
        ]:
            value = getattr(self, field_name)
            if value:
                setattr(self, field_name, value.strip())

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

    def get_product_group_name(self) -> Optional[str]:
        """Get product group name for inventory."""
        if self.product_id:
            return f"product_{self.product_id}"
        return None

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for CSV/YAML output."""
        return {
            "hostname": self.hostname,
            "environment": self.environment,
            "status": self.status,
            "application_service": self.application_service or "",
            "product_id": self.product_id or "",
            "location": self.location or "",
            "instance": self.instance or "",
            "batch_number": self.batch_number or "",
            "patch_mode": self.patch_mode or "",
            "dashboard_group": self.dashboard_group or "",
            "primary_application": self.primary_application or "",
            "function": self.function or "",
            "ssl_port": self.ssl_port or "",
            "decommission_date": self.decommission_date or "",
            "cname": self.cname or "",
            **self.metadata,
        }

    @classmethod
    def from_csv_row(cls, row: Dict[str, str]) -> "Host":
        """Create Host from CSV row data."""
        # Extract known fields
        known_fields = {
            "hostname",
            "environment",
            "status",
            "application_service",
            "product_id",
            "location",
            "instance",
            "batch_number",
            "patch_mode",
            "dashboard_group",
            "primary_application",
            "function",
            "ssl_port",
            "decommission_date",
            "cname",
        }

        host_data = {}
        metadata = {}

        for k, v in row.items():
            clean_value = v.strip() if v else None
            if k in known_fields:
                host_data[k] = clean_value
            else:
                metadata[k] = clean_value

        return cls(**host_data, metadata=metadata)


@dataclass
class ValidationResult:
    """Standardized validation result."""

    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, message: str):
        """Add validation error."""
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str):
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

    def add_host(self, host: Host):
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
            f"📊 Inventory Statistics:",
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

    @classmethod
    def create_default(cls) -> "InventoryConfig":
        """Create default configuration."""
        project_root = Path(__file__).parent.parent
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
