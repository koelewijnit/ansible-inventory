#!/usr/bin/env python3
"""
Geographic Location Utilities
Provides functions for location code management and validation
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

import yaml


class GeographicManager:
    """Manages geographic location codes and configurations"""

    def __init__(self, config_path: str = None):
        """Initialize with optional custom config path"""
        if config_path is None:
            # Default to inventory/group_vars/all/geographic_locations.yml
            base_dir = Path(__file__).parent.parent
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
        """Load the geographic locations configuration"""
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Geographic config not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in geographic config: {e}")

    def get_standard_code(self, location_identifier: str) -> Optional[str]:
        """Convert legacy location identifier to standard code"""
        # Check if it's already a standard code
        if location_identifier in self.config.get("locations", {}):
            return location_identifier

        # Check legacy mappings
        legacy_mappings = self.config.get("legacy_mappings", {})
        return legacy_mappings.get(location_identifier)

    def get_legacy_identifier(self, standard_code: str) -> Optional[str]:
        """Get the legacy identifier for a standard code"""
        location_codes = self.config.get("location_codes", {})
        if standard_code in location_codes:
            return location_codes[standard_code].get("current_identifier")
        return None

    def get_location_info(self, identifier: str) -> Optional[Dict]:
        """Get full location information for any identifier (standard or legacy)"""
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
        """List all configured locations with their codes"""
        locations = []
        for code, info in self.config.get("location_codes", {}).items():
            location_info = self.get_location_info(code)
            if location_info:
                locations.append(location_info)
        return locations

    def validate_location(self, identifier: str) -> bool:
        """Validate if a location identifier is known"""
        return self.get_standard_code(identifier) is not None

    def get_regional_defaults(self, location_identifier: str) -> Optional[Dict]:
        """Get regional defaults for a location"""
        location_info = self.get_location_info(location_identifier)
        if location_info and "region" in location_info:
            region = location_info["region"]
            return self.config.get("regional_defaults", {}).get(region)
        return None


def main():
    """CLI interface for geographic utilities"""
    import argparse

    parser = argparse.ArgumentParser(description="Geographic Location Utilities")
    parser.add_argument(
        "action",
        choices=["list", "lookup", "validate", "convert"],
        help="Action to perform",
    )
    parser.add_argument(
        "location", nargs="?", help="Location identifier (for lookup/validate/convert)"
    )
    parser.add_argument(
        "--format",
        choices=["table", "json", "yaml"],
        default="table",
        help="Output format",
    )

    args = parser.parse_args()

    try:
        geo_mgr = GeographicManager()

        if args.action == "list":
            locations = geo_mgr.list_all_locations()
            if args.format == "table":
                print(
                    f"{'Code':<4} {'Name':<12} {'Country':<15} {'Legacy ID':<20} {'Region'}"
                )
                print("-" * 70)
                for loc in locations:
                    print(
                        f"{loc['standard_code']:<4} {loc['name']:<12} {loc['country']:<15} "
                        f"{loc.get('current_identifier', ''):<20} {loc.get('region', '')}"
                    )
            elif args.format == "json":
                import json

                print(json.dumps(locations, indent=2))
            elif args.format == "yaml":
                print(yaml.dump(locations, default_flow_style=False))

        elif args.action == "lookup":
            if not args.location:
                print("Error: location identifier required for lookup")
                return 1

            info = geo_mgr.get_location_info(args.location)
            if info:
                if args.format == "table":
                    print(f"Location Information for '{args.location}':")
                    for key, value in info.items():
                        if isinstance(value, (list, dict)):
                            print(f"  {key}: {value}")
                        else:
                            print(f"  {key}: {value}")
                elif args.format == "json":
                    import json

                    print(json.dumps(info, indent=2))
                elif args.format == "yaml":
                    print(yaml.dump({args.location: info}, default_flow_style=False))
            else:
                print(f"Location '{args.location}' not found")
                return 1

        elif args.action == "validate":
            if not args.location:
                print("Error: location identifier required for validation")
                return 1

            is_valid = geo_mgr.validate_location(args.location)
            if is_valid:
                standard_code = geo_mgr.get_standard_code(args.location)
                print(
                    f"✓ '{args.location}' is valid (maps to standard code: {standard_code})"
                )
            else:
                print(f"✗ '{args.location}' is not a valid location identifier")
                return 1

        elif args.action == "convert":
            if not args.location:
                print("Error: location identifier required for conversion")
                return 1

            standard_code = geo_mgr.get_standard_code(args.location)
            legacy_id = geo_mgr.get_legacy_identifier(args.location)

            if standard_code:
                print(f"Location: {args.location}")
                print(f"  Standard code: {standard_code}")
                if legacy_id and legacy_id != args.location:
                    print(f"  Legacy identifier: {legacy_id}")
            else:
                print(f"Unknown location: {args.location}")
                return 1

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
