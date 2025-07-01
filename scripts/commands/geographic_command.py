#!/usr/bin/env python3
"""
Geographic Command - Geographic Location Management

This command provides utilities for managing geographic locations,
including location lookup, validation, and legacy identifier conversion.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from commands import BaseCommand, CommandResult
from core import get_logger

SCRIPT_DIR = Path(__file__).parent.parent.absolute()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


class GeographicManager:
    """Manages geographic location codes and configurations."""

    def __init__(self, config_path: str = None):
        """Initialize with optional custom config path."""
        if config_path is None:
            # Default to inventory/group_vars/all/geographic_locations.yml
            base_dir = Path(__file__).parent.parent.parent
            config_path = (
                base_dir
                / "inventory"
                / "group_vars"
                / "all"
                / "geographic_locations.yml"
            )

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load the geographic locations configuration."""
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Geographic config not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in geographic config: {e}")

    def get_standard_code(self, location_identifier: str) -> Optional[str]:
        """Convert legacy location identifier to standard code."""
        # Check if it's already a standard code
        if location_identifier in self.config.get("locations", {}):
            return location_identifier

        # Check legacy mappings
        legacy_mappings = self.config.get("legacy_mappings", {})
        return legacy_mappings.get(location_identifier)

    def get_legacy_identifier(self, standard_code: str) -> Optional[str]:
        """Get the legacy identifier for a standard code."""
        location_codes = self.config.get("location_codes", {})
        if standard_code in location_codes:
            return location_codes[standard_code].get("current_identifier")
        return None

    def get_location_info(self, identifier: str) -> Optional[Dict]:
        """Get full location information for any identifier (standard or legacy)."""
        standard_code = self.get_standard_code(identifier)
        if standard_code:
            locations = self.config.get("locations", {})
            location_codes = self.config.get("location_codes", {})

            info = locations.get(standard_code, {}).copy()
            if standard_code in location_codes:
                info.update(location_codes[standard_code])
            info["standard_code"] = standard_code
            return info
        return None

    def list_all_locations(self) -> List[Dict]:
        """List all configured locations with their codes."""
        locations = []
        for code, info in self.config.get("location_codes", {}).items():
            location_info = self.get_location_info(code)
            if location_info:
                locations.append(location_info)
        return locations

    def validate_location(self, identifier: str) -> bool:
        """Validate if a location identifier is known."""
        return self.get_standard_code(identifier) is not None


class GeographicCommand(BaseCommand):
    """Command to manage geographic location codes and validation."""

    def __init__(self, csv_file: Optional[Path] = None, logger=None):
        super().__init__(csv_file, logger)
        self.logger = logger or get_logger(__name__)
        self.geo_manager = GeographicManager()

    def add_parser_arguments(self, parser):
        """Add geographic-specific arguments to parser."""
        parser.add_argument(
            "action",
            choices=["list", "lookup", "validate", "convert"],
            help="Geographic action to perform",
        )
        parser.add_argument(
            "location",
            nargs="?",
            help="Location identifier (for lookup/validate/convert)",
        )
        parser.add_argument(
            "--format",
            choices=["table", "json", "yaml"],
            default="table",
            help="Output format (default: table)",
        )
        parser.add_argument(
            "--config-path",
            type=Path,
            help="Custom path to geographic configuration file",
        )

    def execute(self, args) -> Dict[str, Any]:
        """Execute the geographic command."""
        try:
            # Initialize with custom config if provided
            if args.config_path:
                self.geo_manager = GeographicManager(str(args.config_path))
            else:
                self.geo_manager = GeographicManager()

            if args.action == "list":
                return self._handle_list(args)
            elif args.action == "lookup":
                return self._handle_lookup(args)
            elif args.action == "validate":
                return self._handle_validate(args)
            elif args.action == "convert":
                return self._handle_convert(args)
            else:
                return CommandResult(
                    success=False, error=f"Unknown geographic action: {args.action}"
                ).to_dict()

        except FileNotFoundError as e:
            error_msg = f"Geographic operation failed: {e}"
            self.logger.error(error_msg)
            return CommandResult(success=False, error=error_msg).to_dict()
        except Exception as e:
            error_msg = f"Geographic operation failed: {e}"
            self.logger.error(error_msg)
            return CommandResult(success=False, error=error_msg).to_dict()

    def _handle_list(self, args) -> Dict[str, Any]:
        """Handle listing all locations."""
        self.logger.info("📍 Listing all geographic locations")

        locations = self.geo_manager.list_all_locations()

        result_data = {
            "command": "geographic",
            "action": "list",
            "locations": locations,
            "total_locations": len(locations),
            "format": args.format,
        }

        return CommandResult(
            success=True,
            data=result_data,
            message=f"Found {len(locations)} geographic locations",
        ).to_dict()

    def _handle_lookup(self, args) -> Dict[str, Any]:
        """Handle looking up a specific location."""
        if not args.location:
            return CommandResult(
                success=False, error="Location identifier required for lookup"
            ).to_dict()

        self.logger.info(f"🔍 Looking up location: {args.location}")

        location_info = self.geo_manager.get_location_info(args.location)

        if location_info:
            result_data = {
                "command": "geographic",
                "action": "lookup",
                "location_identifier": args.location,
                "location_info": location_info,
                "format": args.format,
            }

            return CommandResult(
                success=True,
                data=result_data,
                message=f"Found location information for '{args.location}'",
            ).to_dict()
        else:
            return CommandResult(
                success=False, error=f"Location '{args.location}' not found"
            ).to_dict()

    def _handle_validate(self, args) -> Dict[str, Any]:
        """Handle validating a location identifier."""
        if not args.location:
            return CommandResult(
                success=False, error="Location identifier required for validation"
            ).to_dict()

        self.logger.info(f"✅ Validating location: {args.location}")

        is_valid = self.geo_manager.validate_location(args.location)
        standard_code = (
            self.geo_manager.get_standard_code(args.location) if is_valid else None
        )

        result_data = {
            "command": "geographic",
            "action": "validate",
            "location_identifier": args.location,
            "is_valid": is_valid,
            "standard_code": standard_code,
        }

        if is_valid:
            message = (
                f"✓ '{args.location}' is valid (maps to standard code: {standard_code})"
            )
        else:
            message = f"✗ '{args.location}' is not a valid location identifier"

        return CommandResult(
            success=is_valid, data=result_data, message=message
        ).to_dict()

    def _handle_convert(self, args) -> Dict[str, Any]:
        """Handle converting between location identifier formats."""
        if not args.location:
            return CommandResult(
                success=False, error="Location identifier required for conversion"
            ).to_dict()

        self.logger.info(f"🔄 Converting location: {args.location}")

        standard_code = self.geo_manager.get_standard_code(args.location)
        legacy_id = self.geo_manager.get_legacy_identifier(args.location)

        if standard_code:
            result_data = {
                "command": "geographic",
                "action": "convert",
                "input_location": args.location,
                "standard_code": standard_code,
                "legacy_identifier": legacy_id,
            }

            return CommandResult(
                success=True,
                data=result_data,
                message=f"Converted '{args.location}' to standard code: {standard_code}",
            ).to_dict()
        else:
            return CommandResult(
                success=False, error=f"Unknown location: {args.location}"
            ).to_dict()

    def format_text_output(self, result: Dict[str, Any]) -> str:
        """Format geographic result for text output."""
        if not result.get("success", False):
            return f"❌ Geographic operation failed: {result.get('error', 'Unknown error')}"

        data = result.get("data", {})
        action = data.get("action", "unknown")
        output_format = data.get("format", "table")

        if action == "list":
            return self._format_list_output(data, output_format)
        elif action == "lookup":
            return self._format_lookup_output(data, output_format)
        elif action == "validate":
            return self._format_validate_output(data)
        elif action == "convert":
            return self._format_convert_output(data)
        else:
            return "❓ Unknown geographic action: {}".format(action)

    def _format_list_output(self, data: Dict[str, Any], output_format: str) -> str:
        locations = data.get("locations", [])
        total = data.get("total_locations", 0)

        if output_format == "json":
            return json.dumps(locations, indent=2)
        elif output_format == "yaml":
            return yaml.dump(locations, default_flow_style=False)
        else:  # table format
            lines = [
                "📍 GEOGRAPHIC LOCATIONS",
                "Total locations: {}".format(total),
                "",
                "{'Code':<4} {'Name':<12} {'Country':<15} {'Legacy ID':<20} {'Region'}",
            ]
            lines.append("-" * 70)

            for loc in locations:
                lines.append(
                    "{:<4} {:<12} {:<15} {:<20} {}".format(
                        loc.get("standard_code", ""),
                        loc.get("name", ""),
                        loc.get("country", ""),
                        loc.get("current_identifier", ""),
                        loc.get("region", ""),
                    )
                )

            return "\n".join(lines)

    def _format_lookup_output(self, data: Dict[str, Any], output_format: str) -> str:
        location_info = data.get("location_info", {})
        location_id = data.get("location_identifier", "unknown")

        if output_format == "json":
            return json.dumps(location_info, indent=2)
        elif output_format == "yaml":
            return yaml.dump({location_id: location_info}, default_flow_style=False)
        else:  # table format
            lines = ["📍 Location Information for '{}':".format(location_id)]
            for key, value in location_info.items():
                if isinstance(value, (list, dict)):
                    lines.append("  {}: {}".format(key, value))
                else:
                    lines.append("  {}: {}".format(key, value))

            return "\n".join(lines)

    def _format_validate_output(self, data: Dict[str, Any]) -> str:
        location_id = data.get("location_identifier", "unknown")
        is_valid = data.get("is_valid", False)
        standard_code = data.get("standard_code")

        if is_valid:
            return "✓ '{}' is valid (maps to standard code: {}) ".format(
                location_id, standard_code
            )
        else:
            return "✗ '{}' is not a valid location identifier".format(location_id)

    def _format_convert_output(self, data: Dict[str, Any]) -> str:
        input_location = data.get("input_location", "unknown")
        standard_code = data.get("standard_code")
        legacy_id = data.get("legacy_identifier")

        lines = [
            "🔄 Location Conversion for: {}".format(input_location),
            "  Standard code: {}".format(standard_code),
        ]

        if legacy_id and legacy_id != input_location:
            lines.append("  Legacy identifier: {}".format(legacy_id))

        return "\n".join(lines)
