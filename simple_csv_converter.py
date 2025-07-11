#!/usr/bin/env python3
"""
Simple CSV to Ansible inventory converter
Converts any CSV file to hosts.yml format with embedded host variables
Only requirement: CSV must contain a 'hostname' column
"""

import csv
import yaml
import sys
from pathlib import Path


def read_csv_data(csv_file):
    """Read CSV data and return host information"""
    
    print(f"Reading CSV data from {csv_file}...")
    
    hosts_data = {}
    
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Check if hostname column exists
        if 'hostname' not in reader.fieldnames:
            print("❌ CSV must contain a 'hostname' column")
            sys.exit(1)
        
        print(f"✓ Detected CSV headers: {list(reader.fieldnames)}")
        
        for row in reader:
            hostname = row.get('hostname')
            if hostname:
                # Include all fields, keeping empty values as empty strings
                hosts_data[hostname] = dict(row)
    
    print(f"✓ Read {len(hosts_data)} hosts from CSV")
    return hosts_data


def create_simple_inventory(hosts_data):
    """Create a base inventory file with all hosts and variables embedded"""
    
    inventory_file = Path('inventory/hosts.yml')
    inventory_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create inventory with all hosts and variables
    simple_inventory = {
        'all': {
            'hosts': hosts_data
        }
    }
    
    with open(inventory_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("# Base inventory file with all hosts and variables\n")
        f.write("# Generated from CSV data\n\n")
        yaml.dump(simple_inventory, f, default_flow_style=False, sort_keys=True)
    
    print(f"✓ Created base inventory with {len(hosts_data)} hosts: {inventory_file}")
    return inventory_file


def main():
    """Main function to create simplified inventory system"""
    
    print("CSV to Ansible Inventory Converter")
    print("=" * 40)
    
    # Check if CSV file exists
    csv_file = 'inventory_source/sample_hosts.csv'
    if not Path(csv_file).exists():
        print(f"❌ CSV file not found: {csv_file}")
        print("Please ensure your CSV file exists in inventory_source/")
        sys.exit(1)
    
    try:
        # Read CSV data
        hosts_data = read_csv_data(csv_file)
        
        # Create simple inventory with hosts
        create_simple_inventory(hosts_data)
        
        print("\n" + "=" * 40)
        print("✅ Inventory created successfully!")
        print(f"✅ Converted {len(hosts_data)} hosts from CSV")
        print("\nOutput file: inventory/hosts.yml")
        print("\nNext steps:")
        print("1. Use with ansible-inventory command:")
        print("   ansible-inventory -i inventory/hosts.yml --list")
        print("2. Use with ansible-playbook:")
        print("   ansible-playbook -i inventory/hosts.yml playbook.yml")
        
    except Exception as e:
        print(f"❌ Error creating inventory: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
