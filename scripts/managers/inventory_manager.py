#!/usr/bin/env python3
"""
Inventory Manager - Core Inventory Operations

Handles the generation of Ansible inventory files and host_vars
from CSV data sources.
"""

# Add scripts directory to path for imports
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

SCRIPT_DIR = Path(__file__).parent.parent.absolute()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core import (
    DEFAULT_SUPPORT_GROUP,
    HOST_VARS_HEADER,
    ensure_directory_exists,
    get_logger,
    load_csv_data,
)
from core.models import Host, InventoryConfig, InventoryStats


class InventoryManager:
    """Manages core inventory operations and file generation."""

    def __init__(self, csv_file: Optional[Path] = None, logger=None):
        # Import here to ensure correct path resolution
        from core import CSV_FILE as DEFAULT_CSV_FILE

        self.config = InventoryConfig.create_default()
        self.csv_file = csv_file if csv_file is not None else DEFAULT_CSV_FILE
        self.logger = logger if logger else get_logger(__name__)
        self.stats = InventoryStats()

        # Ensure CSV file exists
        if not Path(self.csv_file).exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")

        self.logger.info("Inventory Manager initialized")
        self.logger.info(f"Using CSV source: {self.csv_file}")

    def load_hosts(self, environment: Optional[str] = None) -> List[Host]:
        """Load hosts from CSV with optional environment filtering."""
        csv_data = load_csv_data(
            self.csv_file, required_fields=["hostname", "environment"]
        )
        hosts = []

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

    def generate_inventories(
        self,
        output_dir: Path,
        host_vars_dir: Path,
        environments: Optional[List[str]] = None,
    ) -> InventoryStats:
        """Generate inventory files and host_vars."""
        start_time = time.time()
        self.logger.info("Starting inventory generation")

        all_hosts = self.load_hosts()
        target_environments = environments or self.config.environments

        for env in target_environments:
            env_hosts = [h for h in all_hosts if h.environment == env and h.is_active]

            if not env_hosts:
                self.logger.warning(f"No active hosts found for environment: {env}")
                continue

            # Generate host_vars
            for host in env_hosts:
                self.create_host_vars(host, host_vars_dir)

            # Generate environment inventory
            inventory = self.build_environment_inventory(env_hosts, env)
            if inventory:
                output_file = output_dir / f"{env}.yml"
                self.write_inventory_file(
                    inventory, output_file, f"{env.title()} Environment"
                )

                host_count = len(inventory.get(env, {}).get("hosts", {}))
                app_groups = len([g for g in inventory.keys() if g.startswith("app_")])
                prod_groups = len(
                    [g for g in inventory.keys() if g.startswith("product_")]
                )

                self.logger.info(
                    f"✅ {env}: {host_count} hosts, {app_groups} app groups, {prod_groups} product groups"
                )

        self.stats.generation_time = time.time() - start_time
        return self.stats

    def create_host_vars(self, host: Host, host_vars_dir: Path) -> None:
        """Create host_vars file for a host."""
        ensure_directory_exists(str(host_vars_dir))

        host_vars = {
            "hostname": host.hostname,
            "cname": host.cname or "",
            "environment": host.environment,
            "application_service": host.application_service or "",
            "product_id": host.product_id or "",
            "location": host.location or "",
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

        host_vars_file = host_vars_dir / f"{host.hostname}.yml"
        with host_vars_file.open("w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"# Host variables for {host.hostname}\n")
            f.write(f"# {HOST_VARS_HEADER}\n")
            f.write("\n")
            yaml.dump(host_vars, f, default_flow_style=False, sort_keys=True)

    def build_environment_inventory(
        self, hosts: List[Host], environment: str
    ) -> Dict[str, Any]:
        """Build inventory dictionary for an environment."""
        inventory = defaultdict(lambda: {"hosts": {}})

        for host in hosts:
            inventory[environment]["hosts"][host.hostname] = None

            if host.application_service:
                app_group = host.get_app_group_name()
                if app_group:
                    inventory[app_group]["hosts"][host.hostname] = None

            if host.product_id:
                prod_group = host.get_product_group_name()
                if prod_group:
                    inventory[prod_group]["hosts"][host.hostname] = None

        return dict(inventory)

    def write_inventory_file(
        self, inventory: Dict[str, Any], output_file: Path, title: str
    ) -> None:
        """Write inventory to YAML file."""
        ensure_directory_exists(str(output_file.parent))

        with output_file.open("w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"# {title} Inventory\n")
            f.write(
                "# Generated from enhanced CSV with CMDB and patch management integration\n"
            )
            f.write(f"# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n")
            yaml.dump(inventory, f, default_flow_style=False, sort_keys=True)

    def get_stats(self) -> InventoryStats:
        """Get current inventory statistics."""
        return self.stats
