#!/usr/bin/env python3
"""
Base classes for CLI commands

This module contains the base classes that all commands inherit from.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional


class BaseCommand(ABC):
    """Base interface for all CLI commands."""

    def __init__(
        self, csv_file: Optional[Path] = None, logger: Optional[Any] = None
    ) -> None:
        self.csv_file = csv_file
        self.logger = logger

    @abstractmethod
    def execute(self, args: Any) -> Dict[str, Any]:
        """Execute the command with the given arguments.

        Args:
            args: Parsed command-line arguments

        Returns:
            Dictionary with command results
        """
        pass

    @abstractmethod
    def add_parser_arguments(self, parser: Any) -> None:
        """Add command-specific arguments to the parser.

        Args:
            parser: ArgumentParser subparser for this command
        """
        pass


class CommandResult:
    """Standardized command result wrapper."""

    def __init__(
        self,
        success: bool = True,
        data: Optional[Dict[str, Any]] = None,
        message: str = "",
        error: str = "",
    ) -> None:
        self.success = success
        self.data = data or {}
        self.message = message
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON output."""
        result = {"success": self.success, "data": self.data}
        if self.message:
            result["message"] = self.message
        if self.error:
            result["error"] = self.error
        return result
