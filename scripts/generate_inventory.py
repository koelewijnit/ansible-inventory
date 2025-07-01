#!/usr/bin/env python3
"""
Comprehensive Inventory Generator

Generates complete Ansible inventories from CSV data sources with enterprise features:
- Environment-specific inventory files
- CMDB integration with metadata structures
- Patch management with batching and scheduling
- Application and product group hierarchies
- Host variables with comprehensive configuration
- Type-safe data models and validation
- Standardized logging and error handling

Author: Ansible Inventory Management System
Version: 3.0.0 (Senior Developer Enhanced)
"""

import argparse
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent.absolute()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from datetime import datetime

from config import (
    DEFAULT_SUPPORT_GROUP,
    ENVIRONMENTS,
    HOST_VARS_HEADER,
    INVENTORY_SOURCE_DIR,
)
from models import Host, InventoryConfig, InventoryStats, ValidationResult
from utils import (
    ensure_directory_exists,
    get_logger,
    load_csv_data,
    validate_environment_decorator,
)


class InventoryGenerator:
    """Enterprise inventory generator with type safety and comprehensive features."""

    def __init__(self, config: InventoryConfig):
        """Initialize the inventory generator."""
        self.config = config
        self.logger = get_logger(__name__)
        self.stats = InventoryStats()

    @validate_environment_decorator
    def load_hosts_by_environment(
        self, csv_file: Path, environment: Optional[str] = None
    ) -> List[Host]:
        """Load hosts from CSV, optionally filtered by environment."""
        try:
            csv_data = load_csv_data(
                csv_file, required_fields=["hostname", "environment"]
            )
            hosts = []

            for row_data in csv_data:
                try:
                    host = Host.from_csv_row(row_data)

                    # Filter by environment if specified
                    if environment and host.environment != environment:
                        continue

                    hosts.append(host)
                    self.stats.add_host(host)

                except ValueError as e:
                    self.logger.warning(f"Skipping invalid host data: {e}")
                    continue

            self.logger.info(f"Loaded {len(hosts)} hosts from {csv_file}")
            return hosts

        except Exception as e:
            self.logger.error(f"Failed to load CSV data: {e}")
            raise

    def create_host_vars(self, host: Host, host_vars_dir: Path) -> None:
        """Create host_vars file with CMDB and patch management fields."""
        try:
            # Ensure directory exists
            ensure_directory_exists(str(host_vars_dir))

            # Build comprehensive host variables
            host_vars = {
                "hostname": host.hostname,
                "cname": host.cname or "",
                "environment": host.environment,
                "application_service": host.application_service or "",
                "product_id": host.product_id or "",
                "location": host.location or "",
                "instance": host.instance or "",
                "status": host.status,
                # CMDB discovery metadata
                "cmdb_discovery": {
                    "support_group": DEFAULT_SUPPORT_GROUP,
                    "primary_application": host.primary_application or "",
                    "function": host.function or "",
                    "classification": host.environment.title(),
                    "dashboard_group": host.dashboard_group or "",
                },
                # Patch management metadata
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

            # Add SSL port if present
            if host.ssl_port:
                try:
                    host_vars["ssl_port"] = int(host.ssl_port)
                except ValueError:
                    host_vars["ssl_port"] = host.ssl_port

            # Add decommission date if present
            if host.decommission_date:
                host_vars["decommission_date"] = host.decommission_date

            # Add any metadata fields
            host_vars.update(host.metadata)

            # Write host_vars file
            host_vars_file = host_vars_dir / f"{host.hostname}.yml"
            with host_vars_file.open("w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"# Host variables for {host.hostname}\n")
                f.write(f"# {HOST_VARS_HEADER}\n")
                f.write("\n")
                yaml.dump(host_vars, f, default_flow_style=False, sort_keys=True)

        except Exception as e:
            self.logger.error(f"Failed to create host_vars for {host.hostname}: {e}")
            raise

    def generate_environment_inventory(
        self, hosts: List[Host], environment: str
    ) -> Dict[str, Any]:
        """Generate inventory for a specific environment."""
        inventory = defaultdict(lambda: {"hosts": {}})

        env_hosts = [h for h in hosts if h.environment == environment and h.is_active]

        if not env_hosts:
            self.logger.warning(f"No active hosts found for environment: {environment}")
            return {}

        for host in env_hosts:
            # Environment group
            inventory[environment]["hosts"][host.hostname] = None

            # Application service group
            if host.application_service:
                app_group = host.get_app_group_name()
                if app_group:
                    inventory[app_group]["hosts"][host.hostname] = None

            # Product group
            if host.product_id:
                prod_group = host.get_product_group_name()
                if prod_group:
                    inventory[prod_group]["hosts"][host.hostname] = None

        # Count groups for stats
        app_groups = len([g for g in inventory.keys() if g.startswith("app_")])
        prod_groups = len([g for g in inventory.keys() if g.startswith("product_")])
        self.stats.application_groups += app_groups
        self.stats.product_groups += prod_groups

        return dict(inventory)

    def generate_comprehensive_inventory(self, hosts: List[Host]) -> Dict[str, Any]:
        """Generate comprehensive inventory with all environments."""
        inventory = defaultdict(lambda: {"hosts": {}})

        for host in hosts:
            # Determine target group
            if host.is_decommissioned:
                target_group = "decommissioned"
            else:
                target_group = host.environment

            inventory[target_group]["hosts"][host.hostname] = None

            # Skip service groups for decommissioned hosts
            if host.is_decommissioned:
                continue

            # Application service group
            if host.application_service:
                app_group = host.get_app_group_name()
                if app_group:
                    inventory[app_group]["hosts"][host.hostname] = None

            # Product group
            if host.product_id:
                prod_group = host.get_product_group_name()
                if prod_group:
                    inventory[prod_group]["hosts"][host.hostname] = None

        return dict(inventory)

    def write_inventory_file(
        self,
        inventory: Dict[str, Any],
        output_file: Path,
        title: str = "Ansible Inventory",
    ) -> None:
        """Write inventory to YAML file with proper headers."""
        try:
            ensure_directory_exists(str(output_file.parent))

            with output_file.open("w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"# {title}\n")
                f.write(
                    "# Generated from enhanced CSV with CMDB and patch management integration\n"
                )
                f.write(
                    "# Enterprise features: environment groups, application services, product hierarchies\n"
                )
                f.write(
                    f"# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                f.write("\n")
                yaml.dump(inventory, f, default_flow_style=False, sort_keys=True)

            self.logger.info(f"Written inventory to {output_file}")

        except Exception as e:
            self.logger.error(f"Failed to write inventory file {output_file}: {e}")
            raise

    def generate_inventories(
        self,
        csv_file: Path,
        output_dir: Path,
        host_vars_dir: Path,
        environments: Optional[List[str]] = None,
    ) -> InventoryStats:
        """Generate all inventory files."""
        start_time = time.time()

        try:
            # Load all hosts
            all_hosts = self.load_hosts_by_environment(csv_file)

            if not all_hosts:
                self.logger.error("No hosts loaded from CSV file")
                return self.stats

            # Filter environments if specified
            target_environments = environments or self.config.environments

            # Generate environment-specific inventories
            for env in target_environments:
                env_hosts = [h for h in all_hosts if h.environment == env]

                if not env_hosts:
                    self.logger.warning(f"No hosts found for environment: {env}")
                    continue

                # Generate host_vars for active hosts
                active_hosts = [h for h in env_hosts if h.is_active]
                for host in active_hosts:
                    self.create_host_vars(host, host_vars_dir)

                # Generate environment inventory
                inventory = self.generate_environment_inventory(all_hosts, env)
                if inventory:
                    output_file = output_dir / f"{env}_simple.yml"
                    title = f"{env.title()} Environment Inventory"
                    self.write_inventory_file(inventory, output_file, title)

                    # Log summary
                    env_host_count = len(inventory.get(env, {}).get("hosts", {}))
                    app_groups = len(
                        [g for g in inventory.keys() if g.startswith("app_")]
                    )
                    prod_groups = len(
                        [g for g in inventory.keys() if g.startswith("product_")]
                    )

                    self.logger.info(
                        f"✅ {env}: {env_host_count} hosts, {app_groups} app groups, {prod_groups} product groups"
                    )

            # Record generation time
            self.stats.generation_time = time.time() - start_time

            return self.stats

        except Exception as e:
            self.logger.error(f"Failed to generate inventories: {e}")
            raise


def validate_arguments(args: argparse.Namespace) -> ValidationResult:
    """Validate command-line arguments."""
    result = ValidationResult()

    # Validate CSV file
    if args.csv_file:
        csv_path = Path(args.csv_file)
        if not csv_path.exists():
            result.add_error(f"CSV file not found: {csv_path}")
        elif not csv_path.is_file():
            result.add_error(f"Not a file: {csv_path}")
        elif not str(csv_path).endswith(".csv"):
            result.add_error(f"Not a CSV file: {csv_path}")

    # Validate environments
    if args.environments:
        for env in args.environments:
            if env not in ENVIRONMENTS:
                result.add_error(
                    f"Invalid environment: {env}. Valid options: {', '.join(ENVIRONMENTS)}"
                )

    return result


def print_usage_examples(output_dir: str) -> None:
    """Print comprehensive usage examples."""
    print(f"\n🎯 **Test the comprehensive inventory:**")
    print(f"   ansible-inventory -i {output_dir}/production_simple.yml --list")
    print(f"   ansible-inventory -i {output_dir}/production_simple.yml --graph")
    print(
        f"   ansible app_identity_management -i {output_dir}/production_simple.yml --list-hosts"
    )
    print(
        f"   ansible product_netiq_idm -i {output_dir}/production_simple.yml --list-hosts"
    )
    print(f"\n🔧 **Enterprise Features - CMDB & Patch Management:**")
    print(
        f"   ansible-inventory -i {output_dir}/production_simple.yml --host prd-idm-use1-01"
    )
    print(
        f"   ansible production -i {output_dir}/production_simple.yml -m debug -a 'var=batch_number'"
    )
    print(
        f"   ansible production -i {output_dir}/production_simple.yml -m debug -a 'var=cmdb_discovery'"
    )
    print("\n💡 **Advanced Usage:**")
    print("   # Use custom CSV file")
    print(
        f"   python scripts/generate_inventory.py --csv-file inventory_source/hosts_production.csv"
    )
    print("   # Generate specific environments only")
    print("   python scripts/generate_inventory.py --environments production test")
    print("   # Custom output directory")
    print("   python scripts/generate_inventory.py --output-dir custom_inventory")


def main() -> int:
    """Main function with comprehensive error handling and type safety."""
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Comprehensive Inventory Generator - Generate enterprise Ansible inventories with CMDB integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default CSV from centralized config
  python scripts/generate_inventory.py
  
  # Use specific CSV file
  python scripts/generate_inventory.py --csv-file /path/to/custom_hosts.csv
  
  # Use alternative CSV in inventory_source
  python scripts/generate_inventory.py --csv-file inventory_source/hosts_production.csv
        """,
    )

    parser.add_argument(
        "--csv-file",
        "--csv",
        "-c",
        type=str,
        help="Path to CSV file containing host data (overrides centralized config)",
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="inventory",
        help="Output directory for generated inventory files (default: inventory)",
    )

    parser.add_argument(
        "--host-vars-dir",
        type=str,
        default="inventory/host_vars",
        help="Directory for host_vars files (default: inventory/host_vars)",
    )

    parser.add_argument(
        "--environments",
        "-e",
        nargs="+",
        help="Specific environments to generate (default: all environments)",
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="Comprehensive Inventory Generator v3.0.0",
    )

    args = parser.parse_args()

    # Set up logging
    logger = get_logger(__name__)

    # Validate arguments
    validation = validate_arguments(args)
    if not validation.is_valid:
        logger.error("Validation failed:")
        for error in validation.errors:
            logger.error(f"  {error}")
        return 1

    try:
        # Create configuration
        config = InventoryConfig.create_default()

        # Determine CSV file to use
        if args.csv_file:
            csv_file = Path(args.csv_file)
            logger.info("🚀 **Comprehensive Inventory Generator (Custom CSV)**")
            logger.info(f"📊 Using custom CSV source: {csv_file}")
        else:
            csv_file = config.csv_file
            logger.info(
                "🚀 **Comprehensive Inventory Generator (Using Centralized Config)**"
            )
            logger.info(f"📊 Using configured CSV source: {csv_file}")

        # Validate CSV file exists
        if not csv_file.exists():
            logger.error(f"CSV file not found: {csv_file}")
            available_files = list(INVENTORY_SOURCE_DIR.glob("*.csv"))
            if available_files:
                logger.info("💡 Available CSV files:")
                for file in available_files:
                    logger.info(f"   📄 {file.name}")
            return 1

        # Set up paths
        output_dir = Path(args.output_dir)
        host_vars_dir = Path(args.host_vars_dir)
        environments = args.environments

        if environments:
            logger.info(
                f"🎯 Processing specific environments: {', '.join(environments)}"
            )

        logger.info(
            "Generating enterprise Ansible inventories with CMDB integration and patch management"
        )

        # Create inventory generator
        generator = InventoryGenerator(config)

        # Generate inventories
        stats = generator.generate_inventories(
            csv_file=csv_file,
            output_dir=output_dir,
            host_vars_dir=host_vars_dir,
            environments=environments,
        )

        # Print statistics
        print("\n" + stats.get_summary())

        # Print usage examples
        print_usage_examples(str(output_dir))

        return 0

    except Exception as e:
        logger.error(f"Failed to generate inventory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
