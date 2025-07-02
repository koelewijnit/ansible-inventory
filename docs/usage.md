# Usage

The CLI provides several commands. The most common are shown below.

## Generate Inventories

```bash
python scripts/ansible_inventory_cli.py generate
```

Use `--environments` to limit output or `--dry-run` to preview changes.

## Health Check

```bash
python scripts/ansible_inventory_cli.py health
```

## Validate Data

```bash
python scripts/ansible_inventory_cli.py validate
```

Run `python scripts/ansible_inventory_cli.py --help` for all options.
