#!/usr/bin/env python3
"""Base classes for CLI commands.

This module contains the base classes that all commands inherit from.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional
import logging


class BaseCommand(ABC):
    """Base interface for all CLI commands."""

    def __init__(
        self, csv_file: Optional[Path] = None, logger: Optional[logging.Logger] = None
    ) -> None:
        """Store common options for commands."""
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
    """Standard result structure for command execution.

    This class provides a consistent format for command results with
    success status, data payload, error messages, and optional metadata.
    """

    def __init__(
        self,
        success: bool,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        message: Optional[str] = None,
    ) -> None:
        """Initialize a command result.

        Args:
            success: Whether the command succeeded
            data: Optional data payload with command output
            error: Optional error message if command failed
            message: Optional human-readable message
        """
        self.success = success
        self.data = data or {}
        self.error = error
        self.message = message

    def to_dict(self) -> Dict[str, Any]:
        """Convert the result to a dictionary format.

        Returns:
            Dictionary containing result fields
        """
        result = {"success": self.success, "data": self.data}
        if self.error:
            result["error"] = self.error
        if self.message:
            result["message"] = self.message
        return result
