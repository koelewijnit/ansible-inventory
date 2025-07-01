#!/usr/bin/env python3
"""
Commands package for Ansible Inventory Management CLI

This package contains all command implementations following a consistent interface.
"""

from pathlib import Path
from typing import Optional

from .base import BaseCommand, CommandResult
from .generate_command import GenerateCommand
from .geographic_command import GeographicCommand
from .health_command import HealthCommand
from .import_command import ImportCommand
from .lifecycle_command import LifecycleCommand
from .validate_command import ValidateCommand


class CommandRegistry:
    """Registry for all available commands."""

    def __init__(self):
        self.commands = {
            "generate": GenerateCommand,
            "health": HealthCommand,
            "validate": ValidateCommand,
            "lifecycle": LifecycleCommand,
            "import": ImportCommand,
            "geographic": GeographicCommand,
        }

    def get_command_class(self, command_name: str):
        """Get command class by name."""
        return self.commands.get(command_name)

    def get_available_commands(self) -> list:
        """Get list of available command names."""
        return list(self.commands.keys())

    def create_command(
        self, command_name: str, csv_file: Optional[Path] = None, logger=None
    ):
        """Create command instance by name."""
        command_class = self.get_command_class(command_name)
        if command_class:
            return command_class(csv_file, logger)
        raise ValueError(f"Unknown command: {command_name}")


__all__ = [
    "BaseCommand",
    "CommandResult",
    "CommandRegistry",
    "GenerateCommand",
    "HealthCommand",
    "ValidateCommand",
    "LifecycleCommand",
    "ImportCommand",
    "GeographicCommand",
]
