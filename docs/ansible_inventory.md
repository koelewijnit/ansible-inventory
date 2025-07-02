# Ansible Inventory

Generated inventories reside in the `inventory/` directory. Each environment is written to a separate YAML file.
Inspect any file with `ansible-inventory`.

```text
inventory/
├── production.yml
├── development.yml
├── test.yml
└── group_vars/
    └── env_production.yml
```

Host-specific variables live in `inventory/host_vars/` when generated. Adjust naming patterns in `inventory-config.yml`.
