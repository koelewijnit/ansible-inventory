"""Test cases for HostManager functionality."""
import os
import sys
import unittest
from unittest.mock import patch
from pathlib import Path
import csv
from datetime import datetime, timedelta
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.managers.host_manager import HostManager  # noqa: E402


class TestHostManager(unittest.TestCase):
    """Test cases for HostManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.csv_file = Path(tempfile.NamedTemporaryFile().name)
        self._create_default_csv()
        self.logger_patch = patch("scripts.managers.host_manager.get_logger")
        self.mock_logger = self.logger_patch.start()
        self.host_manager = HostManager(csv_file=self.csv_file)

    def tearDown(self):
        """Clean up test fixtures."""
        self.logger_patch.stop()
        if self.csv_file.exists():
            self.csv_file.unlink()

    def _create_default_csv(self):
        """Create default test CSV data."""
        data = [
            ["hostname", "environment", "status", "decommission_date"],
            ["test-host-01", "production", "active", ""],
            ["test-host-02", "development", "decommissioned", "2025-01-01"],
            ["test-host-03", "production", "decommissioned", 
             (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")],
        ]
        self._write_csv_data(data)

    def _write_csv_data(self, data):
        """Write CSV data to test file."""
        with self.csv_file.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def test_load_hosts_from_csv_raw(self):
        """Test loading hosts from CSV returns correct data."""
        hosts = self.host_manager.load_hosts_from_csv_raw()
        self.assertEqual(len(hosts), 3)
        self.assertEqual(hosts[0]["hostname"], "test-host-01")

    def test_decommission_host_success(self):
        """Test successful host decommissioning."""
        with patch("scripts.managers.host_manager.HostManager.save_hosts_to_csv") as mock_save:
            result = self.host_manager.decommission_host("test-host-01", "2025-01-01")
            self.assertTrue(result)
            mock_save.assert_called_once()

    def test_decommission_host_not_found(self):
        """Test decommissioning non-existent host returns False."""
        with patch("scripts.managers.host_manager.HostManager.save_hosts_to_csv") as mock_save:
            result = self.host_manager.decommission_host("non-existent-host", "2025-01-01")
            self.assertFalse(result)
            mock_save.assert_not_called()

    def test_decommission_host_already_decommissioned(self):
        """Test decommissioning already decommissioned host returns False."""
        with patch("scripts.managers.host_manager.HostManager.save_hosts_to_csv") as mock_save:
            result = self.host_manager.decommission_host("test-host-02", "2025-01-01")
            self.assertFalse(result)
            mock_save.assert_not_called()

    def test_list_expired_hosts(self):
        """Test listing expired hosts returns correct results."""
        expired_data = [
            ["hostname", "environment", "status", "decommission_date"],
            ["test-host-03", "production", "decommissioned", 
             (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")],
        ]
        self._write_csv_data(expired_data)
        expired_hosts = self.host_manager.list_expired_hosts()
        self.assertEqual(len(expired_hosts), 1)
        self.assertEqual(expired_hosts[0]["hostname"], "test-host-03")

    def test_cleanup_expired_hosts(self):
        """Test cleanup of expired hosts removes files and updates CSV."""
        expired_data = [
            ["hostname", "environment", "status", "decommission_date"],
            ["test-host-03", "production", "decommissioned", 
             (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")],
        ]
        self._write_csv_data(expired_data)
        
        with patch("pathlib.Path.exists") as mock_exists, \
             patch("pathlib.Path.unlink") as mock_unlink, \
             patch("scripts.managers.host_manager.HostManager.save_hosts_to_csv") as mock_save, \
             patch("builtins.input", return_value="y"):
            mock_exists.return_value = True
            cleaned_count = self.host_manager.cleanup_expired_hosts()
            self.assertEqual(cleaned_count, 1)
            mock_unlink.assert_called_once()
            mock_save.assert_called_once()


if __name__ == "__main__":
    unittest.main()
