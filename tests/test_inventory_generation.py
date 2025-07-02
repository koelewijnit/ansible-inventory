from pathlib import Path
import subprocess

import yaml

from scripts.managers.inventory_manager import InventoryManager
from scripts.managers.validation_manager import ValidationManager
from scripts.core.utils import load_csv_data


def create_csv(tmp_path: Path, rows: list[str]) -> Path:
    csv_file = tmp_path / "hosts.csv"
    csv_file.write_text("\n".join(rows))
    return csv_file


def test_generate_inventory(tmp_path: Path):
    rows = [
        "hostname,environment,status,cname",
        "web01,production,active,",
        "db01,production,active,",
    ]
    csv_file = create_csv(tmp_path, rows)
    out_dir = tmp_path / "inventory"
    host_vars_dir = out_dir / "host_vars"
    manager = InventoryManager(csv_file=csv_file)
    stats = manager.generate_inventories(out_dir, host_vars_dir, ["production"])
    inv_file = out_dir / "production.yml"
    assert inv_file.exists()
    data = yaml.safe_load(inv_file.read_text())
    assert data["production"]["hosts"] == {"web01": None, "db01": None}
    result = subprocess.run(
        ["ansible-inventory", "-i", str(inv_file), "--list"], capture_output=True
    )
    assert result.returncode == 0
    assert stats.total_hosts == 2


def test_validate_csv_duplicates(tmp_path: Path):
    rows = [
        "hostname,environment,status,cname",
        "dup,production,active,",
        "dup,production,active,",
    ]
    csv_file = create_csv(tmp_path, rows)
    validator = ValidationManager(csv_file=csv_file)
    result = validator.validate_csv_data()
    assert not result.is_valid
    assert any("Duplicate hostnames" in e for e in result.errors)


def test_load_csv_data_malformed(tmp_path: Path):
    rows = [
        "hostname,environment,status",
        "badrow",  # malformed row
    ]
    csv_file = create_csv(tmp_path, rows)
    data = load_csv_data(csv_file)
    assert len(data) == 1
    assert data[0]["hostname"] == "badrow"
