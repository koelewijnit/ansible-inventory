# Dashboard Inventory Transformation

This document explains how to use the `transform_dashboard_inventory.py` script to create a specialized inventory that uses cnames as hostnames and groups by dashboard_group only.

## Overview

The `transform_dashboard_inventory.py` script transforms your existing Ansible inventory to:
- Use `cname` values as the actual hostnames (fallback to `hostname` if `cname` is missing)
- Group hosts by `dashboard_group` only
- Remove all other grouping (batch, environment, etc.)

## Usage

### 1. Generate Dashboard Inventory

```bash
# Generate dashboard inventory and save to file
python transform_dashboard_inventory.py > dashboard_inventory.json
```

### 2. Use with Ansible

```bash
# List all hosts (will show cnames)
ansible-inventory -i dashboard_inventory.json --list

# Show inventory structure
ansible-inventory -i dashboard_inventory.json --graph

# List hosts in specific dashboard group
ansible-inventory -i dashboard_inventory.json --list-hosts web_dashboard

# Run playbook on specific dashboard group
ansible-playbook -i dashboard_inventory.json playbook.yml --limit web_dashboard
```

## Example Output

If your CSV has hosts with these values:
```csv
hostname,cname,dashboard_group
web-01,web-01.example.com,web_dashboard
web-02,web-02.example.com,web_dashboard
db-01,db-01.example.com,db_dashboard
```

The transformed inventory will look like:
```json
{
  "all": {
    "hosts": [
      "web-01.example.com",
      "web-02.example.com", 
      "db-01.example.com"
    ]
  },
  "web_dashboard": {
    "hosts": [
      "web-01.example.com",
      "web-02.example.com"
    ]
  },
  "db_dashboard": {
    "hosts": [
      "db-01.example.com"
    ]
  },
  "_meta": {
    "hostvars": {
      "web-01.example.com": {
        "hostname": "web-01",
        "cname": "web-01.example.com",
        "dashboard_group": "web_dashboard"
      },
      "web-02.example.com": {
        "hostname": "web-02", 
        "cname": "web-02.example.com",
        "dashboard_group": "web_dashboard"
      },
      "db-01.example.com": {
        "hostname": "db-01",
        "cname": "db-01.example.com", 
        "dashboard_group": "db_dashboard"
      }
    }
  }
}
```

## Prerequisites

- Ansible must be installed
- Your CSV must have `cname` and `dashboard_group` columns
- Run `python simple_csv_converter.py` first to create the base inventory

## Workflow

1. **Prepare CSV**: Ensure your CSV has `cname` and `dashboard_group` columns
2. **Generate base inventory**: `python simple_csv_converter.py`
3. **Transform for dashboard**: `python transform_dashboard_inventory.py > dashboard_inventory.json`
4. **Use with Ansible**: `ansible-playbook -i dashboard_inventory.json playbook.yml`

## Benefits

- **Clean hostnames**: Use fully qualified domain names from cname field
- **Simple grouping**: Only dashboard-relevant groups, no batch/environment complexity
- **Standard format**: Output is standard Ansible JSON inventory format
- **Flexible**: Can be used with any Ansible command or playbook

## Troubleshooting

### Script fails with "ansible-inventory not found"
- Install Ansible: `pip install ansible`
- Or use the system package manager

### Empty inventory output
- Make sure `inventory/constructed.yml` exists
- Run `python simple_csv_converter.py` first
- Check that your CSV has the required columns

### Missing dashboard groups
- Verify your CSV has a `dashboard_group` column
- Check for empty values in the dashboard_group column
- Ensure the base inventory was generated correctly
