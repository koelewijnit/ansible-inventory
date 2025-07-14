#!/usr/bin/env python3
"""
Filter hosts from Ansible inventory by any field
"""

import yaml
import sys
from pathlib import Path


def load_inventory(inventory_file):
    """Load inventory from YAML file"""
    try:
        with open(inventory_file, 'r', encoding='utf-8') as f:
            inventory = yaml.safe_load(f)
        return inventory
    except FileNotFoundError:
        print(f"❌ Inventory file not found: {inventory_file}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML: {e}")
        sys.exit(1)


def filter_hosts(inventory, field, value):
    """Filter hosts by field value"""
    filtered_hosts = {}
    
    hosts = inventory.get('all', {}).get('hosts', {})
    
    for hostname, host_data in hosts.items():
        if host_data.get(field) == value:
            filtered_hosts[hostname] = host_data
    
    return filtered_hosts


def list_field_values(inventory, field):
    """List all unique values for a field"""
    values = set()
    
    hosts = inventory.get('all', {}).get('hosts', {})
    
    for hostname, host_data in hosts.items():
        field_value = host_data.get(field)
        if field_value:
            values.add(field_value)
    
    return sorted(values)


def main():
    """Main function"""
    inventory_file = 'inventory/hosts.yml'
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python filter_hosts.py <field> [value]")
        print("  python filter_hosts.py --list-fields")
        print("")
        print("Examples:")
        print("  python filter_hosts.py environment production")
        print("  python filter_hosts.py batch_number 1")
        print("  python filter_hosts.py application_service web_server")
        print("  python filter_hosts.py environment  # List all environment values")
        print("  python filter_hosts.py --list-fields  # Show all available fields")
        sys.exit(1)
    
    # Load inventory
    inventory = load_inventory(inventory_file)
    
    if sys.argv[1] == '--list-fields':
        # Show all available fields
        print("Available fields:")
        hosts = inventory.get('all', {}).get('hosts', {})
        all_fields = set()
        
        for hostname, host_data in hosts.items():
            all_fields.update(host_data.keys())
        
        for field in sorted(all_fields):
            print(f"  {field}")
        return
    
    field = sys.argv[1]
    
    if len(sys.argv) == 2:
        # List all values for the field
        values = list_field_values(inventory, field)
        print(f"Available values for '{field}':")
        for value in values:
            print(f"  {value}")
        return
    
    value = sys.argv[2]
    
    # Filter hosts
    filtered_hosts = filter_hosts(inventory, field, value)
    
    if not filtered_hosts:
        print(f"❌ No hosts found with {field} = '{value}'")
        return
    
    print(f"✅ Found {len(filtered_hosts)} hosts with {field} = '{value}':")
    print("")
    
    for hostname, host_data in filtered_hosts.items():
        print(f"Host: {hostname}")
        for key, val in host_data.items():
            print(f"  {key}: {val}")
        print("")


if __name__ == "__main__":
    main()
