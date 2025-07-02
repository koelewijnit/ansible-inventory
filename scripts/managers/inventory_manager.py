#!/usr/bin/env python3
"""
Inventory manager - core inventory operations.

Handles the generation of Ansible inventory files and host_vars
from CSV data sources.
"""

import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, NoReturn

import yaml


# Ensure sibling modules are importable when imported outside of the `scripts`
# directory
SCRIPT_DIR = Path(__file__).parent.parent.absolute()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core import (  # noqa: E402
    CSV_FILE as DEFAULT_CSV_FILE,
    DEFAULT_SUPPORT_GROUP,
    HOST_VARS_HEADER,
    ensure_directory_exists,
    get_logger,
    load_csv_data,
)  # noqa: E402
from core.models import Host, InventoryConfig, InventoryStats  # noqa: E402
from core.config import load_config  # noqa: E402


class InventoryManager:
    """Manages core inventory operations and file generation."""

    def __init__(
        self,
        csv_file: Optional[Path] = None,
        logger: Optional[Any] = None,
        inventory_key: str = "hostname",
    ) -> None:
        """Initialise the manager with configuration and logging."""
        self.config = InventoryConfig.create_default(inventory_key=inventory_key)
        self.csv_file: Path = csv_file if csv_file is not None else DEFAULT_CSV_FILE
        self.logger = logger if logger else get_logger(__name__)
        self.stats = InventoryStats()

        # Ensure CSV file exists
        if not Path(self.csv_file).exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")

        self.logger.info("Inventory Manager initialized")
        self.logger.info(f"Using CSV source: {self.csv_file}")

    def load_hosts(self, environment: Optional[str] = None) -> List[Host]:
        """Load hosts from CSV with optional environment filtering."""
        # Determine required fields based on inventory key
        if self.config.inventory_key == "cname":
            # When using cname as primary key, either cname or hostname must be present
            # but we'll let the Host model validation handle this
            required_fields = ["environment"]
        else:
            # When using hostname as primary key, hostname is preferred but cname can be fallback
            required_fields = ["environment"]

        csv_data = load_csv_data(
            self.csv_file,
            required_fields=required_fields,
            inventory_key=self.config.inventory_key,
        )
        hosts: List[Host] = []

        for row_data in csv_data:
            try:
                host = Host.from_csv_row(row_data)
                if environment and host.environment != environment:
                    continue
                hosts.append(host)
                self.stats.add_host(host)
            except ValueError as e:
                self.logger.warning(f"Skipping invalid host data: {e}")
                continue

        self.logger.info(f"Loaded {len(hosts)} hosts from CSV")
        return hosts

    def cleanup_orphaned_host_vars(
        self, hosts: List[Host], dry_run: bool = False
    ) -> int:
        """Clean up orphaned host_vars files that don't exist in the current CSV.

        Args:
            hosts: Current list of hosts from CSV
            dry_run: If True, only report what would be removed

        Returns:
            Number of files removed (or would be removed in dry-run)
        """
        # Check if cleanup is enabled in config
        config = load_config()
        if not config.get("features", {}).get("cleanup_orphaned_on_generate", True):
            self.logger.debug("Orphaned file cleanup is disabled in configuration")
            return 0

        # Collect all valid identifiers (both hostnames and cnames)
        valid_identifiers = set()
        for host in hosts:
            if host.hostname:
                valid_identifiers.add(host.hostname)
            if host.cname:
                valid_identifiers.add(host.cname)

        # Find orphaned files
        orphaned_files = []
        if self.config.host_vars_dir.exists():
            for file_path in self.config.host_vars_dir.glob("*.yml"):
                identifier = file_path.stem
                if identifier not in valid_identifiers:
                    orphaned_files.append(file_path)

        if not orphaned_files:
            return 0

        self.logger.info(f"Found {len(orphaned_files)} orphaned host_vars files")

        if dry_run:
            self.logger.info("[DRY RUN] Would remove orphaned files:")
            for file_path in orphaned_files[:5]:  # Show first 5
                self.logger.info(f"  - {file_path.name}")
            if len(orphaned_files) > 5:
                self.logger.info(f"  ... and {len(orphaned_files) - 5} more")
            return len(orphaned_files)

        # Remove orphaned files
        removed_count = 0
        for file_path in orphaned_files:
            try:
                file_path.unlink()
                self.logger.debug(f"Removed orphaned file: {file_path.name}")
                removed_count += 1
            except Exception as e:
                self.logger.error(f"Failed to remove {file_path}: {e}")

        if removed_count > 0:
            self.logger.info(f"Cleaned up {removed_count} orphaned host_vars files")

        return removed_count

    def generate_inventories(
        self, environments: Optional[List[str]] = None, dry_run: bool = False
    ) -> Dict[str, Any]:
        """Generate inventory files for specified environments.

        Args:
            environments: List of environments to generate (None for all)
            dry_run: If True, only show what would be generated

        Returns:
            Dictionary with generation results and statistics

        Raises:
            FileNotFoundError: If CSV source file doesn't exist
            ValueError: If no valid hosts found
        """
        self.logger.info("Starting inventory generation")
        start_time = time.time()

        # Reset statistics
        self.stats = InventoryStats()

        try:
            # Load and validate hosts
            hosts = self.load_hosts()
            if not hosts:
                raise ValueError("No valid hosts found in CSV file")

            self.logger.info(f"Loaded {len(hosts)} hosts from CSV")

            # Clean up orphaned host_vars files before generating new ones
            orphaned_count = self.cleanup_orphaned_host_vars(hosts, dry_run)

            # Filter environments if specified
            target_environments = environments or self.config.environments

            # Generate inventories for each environment
            generated_files = []

            for env in target_environments:
                try:
                    self.logger.info(f"Processing environment: {env}")
                    env_hosts = [h for h in hosts if h.environment == env]

                    if not env_hosts:
                        self.logger.warning(f"No hosts found for environment: {env}")
                        continue

                    if dry_run:
                        self.logger.info(
                            f"[DRY RUN] Would generate inventory for {env} "
                            f"with {len(env_hosts)} hosts"
                        )
                    else:
                        # Generate the actual inventory file
                        inventory_file = self._generate_inventory_file(env, env_hosts)
                        generated_files.append(str(inventory_file))
                        self.logger.info(f"Generated inventory file: {inventory_file}")

                except Exception as e:
                    self.logger.error(
                        f"Failed to generate inventory for {env}: {e}", exc_info=True
                    )
                    # Continue with other environments
                    continue

            # Calculate generation time
            self.stats.generation_time = time.time() - start_time

            # Add orphaned count to stats
            self.stats.orphaned_files_removed = orphaned_count

            return {
                "generated_files": generated_files,
                "dry_run": dry_run,
                "stats": self.stats.__dict__,
                "environments": target_environments,
                "orphaned_files_removed": orphaned_count,
            }

        except FileNotFoundError as e:
            self.logger.error(f"CSV source file not found: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Inventory generation failed: {e}", exc_info=True)
            raise ValueError(f"Failed to generate inventories: {e}") from e

    def create_host_vars(self, host: Host, host_vars_dir: Path) -> None:
        """Create host_vars file for a host."""
        ensure_directory_exists(str(host_vars_dir))

        # Get the primary identifier for this host based on inventory key
        primary_id = host.get_inventory_key_value(self.config.inventory_key)

        host_vars: Dict[str, Any] = {
            "hostname": host.hostname or "",
            "cname": host.cname or "",
            "environment": host.environment,
            "application_service": host.application_service or "",
            "product_id": host.product_id or "",
            "products": {
                "installed": host.get_product_ids(),
                "primary": host.get_primary_product_id() or "",
                "count": len(host.get_product_ids()),
            },
            "site_code": host.site_code or "",
            "instance": host.instance or "",
            "status": host.status,
            "cmdb_discovery": {
                "support_group": DEFAULT_SUPPORT_GROUP,
                "primary_application": host.primary_application or "",
                "function": host.function or "",
                "classification": host.environment.title(),
                "dashboard_group": host.dashboard_group or "",
            },
            "patch_management": {
                "batch_number": host.batch_number or "",
                "patch_mode": host.patch_mode or "",
                "patching_window": self.config.get_patching_window(
                    host.batch_number or ""
                ),
                "requires_reboot": True,
                "pre_patch_checks": True,
            },
        }

        if host.ssl_port:
            try:
                host_vars["ssl_port"] = int(host.ssl_port)
            except ValueError:
                host_vars["ssl_port"] = host.ssl_port

        if host.decommission_date:
            host_vars["decommission_date"] = host.decommission_date

        host_vars.update(host.metadata)

        # Use the inventory key-based filename
        host_vars_filename = host.get_host_vars_filename(self.config.inventory_key)
        host_vars_file: Path = host_vars_dir / host_vars_filename
        with host_vars_file.open("w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"# Host variables for {primary_id}\n")
            f.write(f"# {HOST_VARS_HEADER}\n")
            f.write("\n")
            yaml.dump(host_vars, f, default_flow_style=False, sort_keys=True)

    def build_environment_inventory(
        self, hosts: List[Host], environment: str
    ) -> Dict[str, Any]:
        """Build inventory dictionary for an environment."""
        inventory: Dict[str, Any] = defaultdict(lambda: {"hosts": {}})

        for host in hosts:
            if host.environment != environment:
                continue
            host_key = host.get_inventory_key_value(self.config.inventory_key)
            inventory[environment]["hosts"][host_key] = {}

            if host.application_service:
                app_group = host.get_app_group_name()
                if app_group:
                    inventory[app_group]["hosts"][host_key] = {}

            # Support multiple products per host
            if host.product_id:
                product_groups = host.get_product_group_names()
                for prod_group in product_groups:
                    inventory[prod_group]["hosts"][host_key] = {}

            # Add site_code group if available
            if host.site_code:
                # Ensure site_code is a string and handle any edge cases
                site_code_str = str(host.site_code).strip()
                if site_code_str:
                    site_group = f"site_{site_code_str.lower().replace('-', '_')}"
                    inventory[site_group]["hosts"][host_key] = {}

        return dict(inventory)

    def write_inventory_file(
        self, inventory: Dict[str, Any], output_file: Path, title: str
    ) -> None:
        """Write inventory to YAML file, omitting empty groups."""
        ensure_directory_exists(str(output_file.parent))

        # Remove groups with no hosts
        filtered_inventory = {}
        for group, data in inventory.items():
            hosts = data.get("hosts", {})
            if hosts and len(hosts) > 0:
                filtered_inventory[group] = data

        with output_file.open("w", encoding="utf-8") as f:
            f.write("# ----------------------------------------------------------------------\n")
            f.write("# AUTO-GENERATED FILE - DO NOT EDIT MANUALLY\n")
            f.write("# This file is generated by the inventory management system.\n")
            f.write("# Any manual changes will be overwritten the next time inventory is generated.\n")
            f.write("# ----------------------------------------------------------------------\n")
            f.write(f"# {title} Inventory\n")
            f.write(
                "# Generated from enhanced CSV with CMDB and patch management integration\n"
            )
            f.write(f"# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n")
            yaml.dump(filtered_inventory, f, default_flow_style=False, sort_keys=True)

    def _generate_inventory_file(self, environment: str, hosts: List[Host]) -> Path:
        """Generate inventory file for a specific environment.

        Args:
            environment: Environment name
            hosts: List of hosts for this environment

        Returns:
            Path to generated inventory file

        Raises:
            OSError: If file cannot be written
        """
        try:
            # Create host_vars for all active hosts
            active_hosts = [h for h in hosts if h.is_active]
            for host in active_hosts:
                self.create_host_vars(host, self.config.host_vars_dir)

            # Build inventory structure
            inventory = self.build_environment_inventory(active_hosts, environment)

            # Update statistics
            self.stats.application_groups = len(
                [g for g in inventory.keys() if g.startswith("app_")]
            )
            self.stats.product_groups = len(
                [g for g in inventory.keys() if g.startswith("product_")]
            )

            # Write inventory file
            output_file = self.config.inventory_dir / f"{environment}.yml"
            self.write_inventory_file(
                inventory, output_file, f"{environment.title()} Environment"
            )

            self.logger.info(
                f"Generated {environment} inventory: "
                f"{len(active_hosts)} hosts, "
                f"{self.stats.application_groups} app groups, "
                f"{self.stats.product_groups} product groups"
            )

            return output_file  # type: ignore[no-any-return]

        except OSError as e:
            self.logger.error(f"Failed to write inventory file for {environment}: {e}")
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error generating inventory for {environment}: {e}",
                exc_info=True,
            )
            raise ValueError(f"Failed to generate {environment} inventory: {e}") from e

    def get_stats(self) -> InventoryStats:
        """Get current inventory statistics."""
        return self.stats
