# Usage

The CLI exposes several subcommands. Examples below assume the virtual environment is active.

## Generate inventories

```bash
python scripts/ansible_inventory_cli.py generate
```

Limit to specific environments:

```bash
python scripts/ansible_inventory_cli.py generate --environments production test
```

## Health check

```bash
python scripts/ansible_inventory_cli.py health
```

## Validate data

```bash
python scripts/ansible_inventory_cli.py validate
```

Use `--help` on any command to see additional options.
