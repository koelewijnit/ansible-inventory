#!/usr/bin/env python3
"""
Geographic Location Core Module
Provides the GeographicManager class for location code management and validation.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class GeographicManager:
    """Manages geographic location codes and configurations"""

    def __init__(self, config_path: Optional[str] = None) -> None:
        """Initialize with optional custom config path"""
        if config_path is None:
            # Default to inventory/group_vars/all/geographic_locations.yml
            base_dir = Path(__file__).parent.parent.parent
            config_path = str(
                base_dir
                / "inventory"
                / "group_vars"
                / "all"
                / "geographic_locations.yml"
            )

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load the geographic locations configuration"""
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f) or {}
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
        value = legacy_mappings.get(location_identifier)
        return str(value) if value is not None else None

    def get_legacy_identifier(self, standard_code: str) -> Optional[str]:
        """Get the legacy identifier for a standard code"""
        location_codes = self.config.get("location_codes", {})
        if standard_code in location_codes:
            value = location_codes[standard_code].get("current_identifier")
            return str(value) if value is not None else None
        return None

    def get_location_info(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get full location information for any identifier (standard or legacy)"""
        standard_code = self.get_standard_code(identifier)
        if standard_code:
            locations = self.config.get("locations", {})
            location_codes = self.config.get("location_codes", {})

            info = dict(locations.get(standard_code, {}))
            if standard_code in location_codes:
                info.update(location_codes[standard_code])
            info["standard_code"] = standard_code
            return info if info else None
        return None

    def list_all_locations(self) -> List[Dict[str, Any]]:
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

    def get_regional_defaults(
        self, location_identifier: str
    ) -> Optional[Dict[str, Any]]:
        """Get regional defaults for a location"""
        location_info = self.get_location_info(location_identifier)
        if location_info and "region" in location_info:
            region = location_info["region"]
            defaults = self.config.get("regional_defaults", {})
            region_defaults = defaults.get(region)
            return dict(region_defaults) if region_defaults else None
        return None
