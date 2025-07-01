#!/usr/bin/env python3
"""
Import Command - Inventory Import Operations

This command handles importing existing Ansible inventories and converting them
to the standardized CSV format with enhanced metadata.
"""

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

from commands import BaseCommand, CommandResult
from core import ENVIRONMENTS, PROJECT_ROOT, get_logger

SCRIPT_DIR = Path(__file__).parent.parent.absolute()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


class ImportCommand(BaseCommand):
    """Command to import existing Ansible inventories into CSV format."""

    def __init__(self, csv_file: Optional[Path] = None, logger=None):
        super().__init__(csv_file, logger)
        self.logger = logger or get_logger(__name__)
        self.hosts_data = {}
        self.warnings = []
        self.stats = {"hosts_processed": 0, "groups_found": 0, "host_vars_found": 0}

    def add_parser_arguments(self, parser):
        """Add import-specific arguments to parser."""
        parser.add_argument(
            "--inventory-file",
            "-i",
            type=Path,
            required=True,
            help="Path to existing inventory file to import",
        )
        parser.add_argument(
            "--host-vars-dir",
            type=Path,
            help="Path to existing host_vars directory to import",
        )
        parser.add_argument(
            "--output-csv",
            type=Path,
            help="Output CSV file path (default: inventory_source/imported_hosts.csv)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be imported without creating files",
        )
        parser.add_argument(
            "--report-file",
            type=Path,
            help="Generate detailed import report (default: auto-generated name)",
        )

    def execute(self, args) -> Dict[str, Any]:
        """Execute the import command."""
        try:
            self.logger.info(
                "📥 Starting inventory import from {}".format(args.inventory_file)
            )

            # Validate input file exists
            if not args.inventory_file.exists():
                return CommandResult(
                    success=False,
                    error=f"Inventory file not found: {args.inventory_file}",
                ).to_dict()

            # Set default output paths
            output_csv = args.output_csv or (
                PROJECT_ROOT / "inventory_source" / "imported_hosts.csv"
            )
            report_file = args.report_file or (
                PROJECT_ROOT
                / "inventory_source"
                / f'import_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            )

            # Parse the inventory file
            inventory_data = self._parse_inventory_file(args.inventory_file)
            if not inventory_data:
                return CommandResult(
                    success=False,
                    error=f"Failed to parse inventory file: {args.inventory_file}",
                ).to_dict()

            # Extract hosts from inventory
            self._extract_hosts_from_inventory(inventory_data)

            # Process host_vars if directory provided
            if args.host_vars_dir and args.host_vars_dir.exists():
                self._process_host_vars_directory(args.host_vars_dir)

            # Enhance host data with intelligent mapping
            self._enhance_host_data()

            # Convert to CSV format
            csv_data = self._convert_to_csv_format()

            if args.dry_run:
                return self._dry_run_import(csv_data, output_csv, report_file)

            # Write CSV file
            self._write_csv_file(csv_data, output_csv)

            # Generate report
            self._generate_import_report(report_file, output_csv, args.inventory_file)

            result_data = {
                "command": "import",
                "source_file": str(args.inventory_file),
                "output_csv": str(output_csv),
                "report_file": str(report_file),
                "statistics": self.stats,
                "warnings": self.warnings,
            }

            message = "✅ Imported {} hosts to {}".format(
                self.stats["hosts_processed"], output_csv
            )

            return CommandResult(
                success=True, data=result_data, message=message
            ).to_dict()

        except Exception as e:
            error_msg = f"Import failed: {e}"
            self.logger.error(error_msg)
            return CommandResult(success=False, error=error_msg).to_dict()

    def _parse_inventory_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a single inventory file (YAML or JSON)."""
        self.logger.info(f"📄 Parsing inventory file: {file_path}")

        try:
            with file_path.open("r", encoding="utf-8") as f:
                if file_path.suffix.lower() in [".yml", ".yaml"]:
                    data = yaml.safe_load(f) or {}
                elif file_path.suffix.lower() == ".json":
                    data = json.load(f)
                else:
                    # Try YAML first, then JSON
                    content = f.read()
                    try:
                        data = yaml.safe_load(content) or {}
                    except yaml.YAMLError:
                        data = json.loads(content)

                self.logger.info(
                    f"Successfully parsed inventory with {len(data)} top-level groups"
                )
                return data

        except Exception as e:
            self.logger.error(f"Error parsing {file_path}: {e}")
            return {}

    def _extract_hosts_from_inventory(self, inventory_data: Dict[str, Any]) -> None:
        """Extract all hosts and their group memberships."""
        self.logger.info("🔍 Extracting hosts from inventory structure")

        def extract_hosts_recursive(
            group_name: str, group_data: Any, depth: int = 0
        ) -> None:
            if depth > 10:  # Prevent infinite recursion
                return

            if isinstance(group_data, dict):
                # Process hosts in this group
                if "hosts" in group_data:
                    hosts = group_data["hosts"]
                    if isinstance(hosts, dict):
                        for hostname, host_vars in hosts.items():
                            if hostname not in self.hosts_data:
                                self.hosts_data[hostname] = {
                                    "hostname": hostname,
                                    "groups": set(),
                                    "vars": {},
                                }

                            self.hosts_data[hostname]["groups"].add(group_name)

                            # Collect host variables
                            if isinstance(host_vars, dict):
                                self.hosts_data[hostname]["vars"].update(host_vars)
                    elif isinstance(hosts, list):
                        for hostname in hosts:
                            if isinstance(hostname, str):
                                if hostname not in self.hosts_data:
                                    self.hosts_data[hostname] = {
                                        "hostname": hostname,
                                        "groups": set(),
                                        "vars": {},
                                    }
                                self.hosts_data[hostname]["groups"].add(group_name)

                # Process child groups
                if "children" in group_data:
                    children = group_data["children"]
                    if isinstance(children, dict):
                        for child_name, child_data in children.items():
                            extract_hosts_recursive(child_name, child_data, depth + 1)
                    elif isinstance(children, list):
                        for child_name in children:
                            extract_hosts_recursive(child_name, {}, depth + 1)

        # Start extraction from root
        for group_name, group_data in inventory_data.items():
            extract_hosts_recursive(group_name, group_data)

        self.stats["hosts_processed"] = len(self.hosts_data)
        self.stats["groups_found"] = len(inventory_data)
        self.logger.info(f"Found {len(self.hosts_data)} hosts")

    def _process_host_vars_directory(self, host_vars_dir: Path) -> None:
        """Process host_vars directory to extract additional variables."""
        self.logger.info(f"📁 Processing host_vars directory: {host_vars_dir}")

        for host_var_file in host_vars_dir.glob("*.yml"):
            hostname = host_var_file.stem

            try:
                with host_var_file.open("r", encoding="utf-8") as f:
                    host_vars = yaml.safe_load(f) or {}

                if hostname in self.hosts_data:
                    self.hosts_data[hostname]["vars"].update(host_vars)
                    self.stats["host_vars_found"] += 1
                else:
                    # Create new entry for host not found in inventory
                    self.hosts_data[hostname] = {
                        "hostname": hostname,
                        "groups": set(),
                        "vars": host_vars,
                    }
                    self.warnings.append(
                        f"Host {hostname} found in host_vars but not in inventory"
                    )

            except Exception as e:
                self.warnings.append(f"Error reading host_vars for {hostname}: {e}")

        self.logger.info(f"Processed {self.stats['host_vars_found']} host_vars files")

    def _enhance_host_data(self) -> None:
        """Enhance host data with intelligent mapping."""
        self.logger.info("✨ Enhancing host data with intelligent mapping")

        # Application service patterns
        app_service_patterns = {
            r"web|apache|nginx|httpd": "web_server",
            r"db|database|mysql|postgres|mongodb": "database",
            r"bastion|jump": "bastion_host",
            r"gitlab.*runner|ci.*runner|runner": "cicd_runner",
            r"monitoring|nagios|prometheus|grafana": "monitoring_system",
            r"backend|api": "backend_app",
            r"frontend": "frontend_app",
            r"loadbalancer|lb|haproxy": "load_balancer",
            r"vault|secret": "vault",
            r"kafka|message|broker": "message_broker",
            r"identity|idm|ldap|ad": "identity_management",
            r"mail|email|smtp": "mail_server",
            r"k8s|kubernetes": "k8s_cluster",
        }

        # Product patterns
        product_patterns = {
            r"apache|httpd": "apache_httpd",
            r"nginx": "nginx",
            r"postgresql|postgres": "postgresql",
            r"mysql": "mysql",
            r"mongodb|mongo": "mongodb",
            r"redis": "redis",
            r"gitlab": "gitlab_runner",
            r"jenkins": "jenkins",
            r"prometheus": "prometheus",
            r"grafana": "grafana",
            r"vault": "hashicorp_vault",
            r"consul": "consul",
            r"kafka": "apache_kafka",
            r"elasticsearch|elk": "elasticsearch",
            r"kibana": "kibana",
            r"nagios": "nagios_xi",
        }

        for hostname, host_data in self.hosts_data.items():
            vars_data = host_data["vars"]
            groups = host_data["groups"]

            # Determine environment
            host_data["environment"] = self._determine_environment(
                hostname, groups, vars_data
            )

            # Determine application service and product
            groups_str = " ".join(groups).lower() + " " + hostname.lower()
            host_data["application_service"] = self._match_pattern(
                groups_str, app_service_patterns
            )
            host_data["product_id"] = self._match_pattern(groups_str, product_patterns)

            # Extract other fields
            host_data["cname"] = (
                vars_data.get("ansible_fqdn")
                or vars_data.get("fqdn")
                or vars_data.get("cname", "")
            )
            host_data["location"] = self._determine_location(
                hostname, groups, vars_data
            )
            host_data["instance"] = self._extract_instance_number(hostname)
            host_data["status"] = vars_data.get("status", "active")
            host_data["ssl_port"] = vars_data.get("ssl_port") or vars_data.get(
                "https_port", ""
            )
            host_data["batch_number"] = vars_data.get(
                "batch_number"
            ) or self._determine_batch_number(hostname)
            host_data["patch_mode"] = vars_data.get("patch_mode") or (
                "manual" if host_data["environment"] == "production" else "auto"
            )
            host_data["dashboard_group"] = vars_data.get("dashboard_group", "")
            host_data["primary_application"] = vars_data.get("primary_application", "")
            host_data["function"] = vars_data.get("function") or vars_data.get(
                "description", ""
            )
            host_data["decommission_date"] = vars_data.get("decommission_date", "")

    def _determine_environment(
        self, hostname: str, groups: Set[str], vars_data: Dict
    ) -> str:
        """Determine environment from hostname, groups, or variables."""
        # Check variables first
        if "environment" in vars_data:
            env = vars_data["environment"].lower()
            if env in ENVIRONMENTS:
                return env

        hostname_lower = hostname.lower()

        # Check hostname prefix
        for env in ENVIRONMENTS:
            env_code = env[:3]  # prd, dev, tst, acc
            if hostname_lower.startswith(env_code + "-"):
                return env

        # Check groups
        for group in groups:
            group_lower = group.lower()
            for env in ENVIRONMENTS:
                if env in group_lower:
                    return env

        # Default patterns
        if any(x in hostname_lower for x in ["prod", "prd"]):
            return "production"
        elif any(x in hostname_lower for x in ["dev"]):
            return "development"
        elif any(x in hostname_lower for x in ["test", "tst"]):
            return "test"
        elif any(x in hostname_lower for x in ["acc", "accept"]):
            return "acceptance"

        return "production"  # Default to production for safety

    def _determine_location(
        self, hostname: str, groups: Set[str], vars_data: Dict
    ) -> str:
        """Determine location from various sources."""
        # Check variables first
        location = (
            vars_data.get("location")
            or vars_data.get("datacenter")
            or vars_data.get("region", "")
        )
        if location:
            return location

        hostname_lower = hostname.lower()

        # Common region patterns
        region_patterns = [
            (r"us-?east-?(\d+)?|use(\d+)?", "use1"),
            (r"us-?west-?(\d+)?|usw(\d+)?", "usw1"),
            (r"eu-?west-?(\d+)?|euw(\d+)?", "euw1"),
            (r"ap-?southeast-?(\d+)?|apse(\d+)?", "apse1"),
            (r"norwalk|nrw", "norwalk"),
            (r"las.?vegas|lvg", "lasvegas"),
            (r"taipei|tpe", "taipei"),
            (r"shanwei|shh", "shanwei"),
            (r"eindhoven.*eid|eid", "eindhoven-eid"),
            (r"eindhoven.*htc|htc", "eindhoven-htc"),
        ]

        for pattern, location_code in region_patterns:
            if re.search(pattern, hostname_lower):
                return location_code

            # Check groups too
            for group in groups:
                if re.search(pattern, group.lower()):
                    return location_code

        return ""

    def _match_pattern(self, text: str, patterns: Dict[str, str]) -> str:
        """Match text against patterns to determine mapping."""
        for pattern, mapping in patterns.items():
            if re.search(pattern, text):
                return mapping
        return ""

    def _extract_instance_number(self, hostname: str) -> str:
        """Extract instance number from hostname."""
        patterns = [r"-(\d+)$", r"_(\d+)$", r"(\d+)$"]

        for pattern in patterns:
            match = re.search(pattern, hostname)
            if match:
                return match.group(1).zfill(2)  # Pad with zero

        return "01"  # Default

    def _determine_batch_number(self, hostname: str) -> str:
        """Determine batch number from hostname."""
        digits = re.findall(r"\d", hostname)
        if digits:
            last_digit = int(digits[-1])
            return str((last_digit % 3) + 1)  # Distribute across batches 1-3
        return "1"

    def _convert_to_csv_format(self) -> List[Dict]:
        """Convert enhanced host data to CSV format."""
        csv_data = []

        for hostname, host_data in self.hosts_data.items():
            csv_row = {
                "hostname": hostname,
                "environment": host_data.get("environment", "production"),
                "status": host_data.get("status", "active"),
                "application_service": host_data.get("application_service", ""),
                "product_id": host_data.get("product_id", ""),
                "location": host_data.get("location", ""),
                "instance": host_data.get("instance", "01"),
                "batch_number": host_data.get("batch_number", "1"),
                "patch_mode": host_data.get("patch_mode", "auto"),
                "dashboard_group": host_data.get("dashboard_group", ""),
                "primary_application": host_data.get("primary_application", ""),
                "function": host_data.get("function", ""),
                "ssl_port": host_data.get("ssl_port", ""),
                "decommission_date": host_data.get("decommission_date", ""),
                "cname": host_data.get("cname", ""),
            }
            csv_data.append(csv_row)

        return csv_data

    def _write_csv_file(self, csv_data: List[Dict], output_path: Path) -> None:
        """Write CSV data to file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
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
        ]

        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)

        self.logger.info(f"✅ Wrote {len(csv_data)} hosts to {output_path}")

    def _generate_import_report(
        self, report_path: Path, csv_path: Path, source_path: Path
    ) -> None:
        """Generate detailed import report."""
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with report_path.open("w", encoding="utf-8") as f:
            f.write("# Ansible Inventory Import Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Source File: {source_path}\n")
            f.write(f"Output CSV: {csv_path}\n\n")
            f.write("## Statistics\n")
            f.write(f"- Hosts processed: {self.stats['hosts_processed']}\n")
            f.write(f"- Groups found: {self.stats['groups_found']}\n")
            f.write(f"- Host vars processed: {self.stats['host_vars_found']}\n\n")

            if self.warnings:
                f.write("## Warnings\n")
                for warning in self.warnings:
                    f.write(f"- {warning}\n")

        self.logger.info(f"📄 Generated import report: {report_path}")

    def _dry_run_import(
        self, csv_data: List[Dict], output_csv: Path, report_file: Path
    ) -> Dict[str, Any]:
        """Perform dry run showing what would be imported."""
        result_data = {
            "command": "import",
            "dry_run": True,
            "would_create": {
                "csv_file": str(output_csv),
                "report_file": str(report_file),
                "hosts_count": len(csv_data),
            },
            "statistics": self.stats,
            "warnings": self.warnings,
            "sample_hosts": csv_data[:5],  # Show first 5 hosts as sample
        }

        message = f"[DRY RUN] Would import {len(csv_data)} hosts"

        return CommandResult(success=True, data=result_data, message=message).to_dict()

    def format_text_output(self, result: Dict[str, Any]) -> str:
        """Format import result for text output."""
        if not result.get("success", False):
            return f"❌ Import failed: {result.get('error', 'Unknown error')}"

        data = result.get("data", {})

        if data.get("dry_run"):
            would_create = data.get("would_create", {})
            stats = data.get("statistics", {})

            lines = [
                "🔍 DRY RUN - Ansible Inventory Import Preview",
                "Would import: {} hosts".format(would_create.get("hosts_count", 0)),
                "Would create CSV: {}".format(would_create.get("csv_file", "unknown")),
                "Would create report: {}".format(
                    would_create.get("report_file", "unknown")
                ),
                "",
                "Statistics:",
                "  Hosts processed: {}".format(stats.get("hosts_processed", 0)),
                "  Groups found: {}".format(stats.get("groups_found", 0)),
                "  Host vars processed: {}".format(stats.get("host_vars_found", 0)),
            ]

            sample_hosts = data.get("sample_hosts", [])
            if sample_hosts:
                lines.append("\nSample hosts (first 5):")
                for host in sample_hosts:
                    lines.append(
                        f"  • {host.get('hostname', 'unknown')} ({host.get('environment', 'unknown')})"
                    )

            return "\n".join(lines)

        else:
            stats = data.get("statistics", {})
            lines = [
                "✅ ANSIBLE INVENTORY IMPORT COMPLETED",
                f"📊 Statistics:",
                f"   Hosts imported: {stats.get('hosts_processed', 0)}",
                f"   Groups processed: {stats.get('groups_found', 0)}",
                f"   Host vars processed: {stats.get('host_vars_found', 0)}",
                "",
                f"📄 Output CSV: {data.get('output_csv', 'unknown')}",
                f"📋 Report file: {data.get('report_file', 'unknown')}",
            ]

            warnings = data.get("warnings", [])
            if warnings:
                lines.append(f"\n⚠️  Warnings ({len(warnings)}):")
                for warning in warnings[:5]:  # Show first 5
                    lines.append(f"   • {warning}")
                if len(warnings) > 5:
                    lines.append(
                        f"   ... and {len(warnings) - 5} more (see report file)"
                    )

            return "\n".join(lines)
