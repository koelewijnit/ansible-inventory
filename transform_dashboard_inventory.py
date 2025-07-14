#!/usr/bin/env python3
"""
Transform Ansible inventory to use cnames as hosts and group by dashboard_group only.

This script:
1. Reads the existing inventory from constructed.yml
2. Uses cname as the hostname (falls back to hostname if cname is missing)
3. Groups hosts by dashboard_group only
4. Outputs the transformed inventory as JSON

Usage:
    python transform_dashboard_inventory.py > dashboard_inventory.json
    
Then use with Ansible:
    ansible-inventory -i dashboard_inventory.json --list
    ansible-playbook -i dashboard_inventory.json playbook.yml --limit group_name
"""

import json
import subprocess
import sys
from pathlib import Path

def get_inventory_data():
    """Get inventory data from ansible-inventory command"""
    try:
        # Run ansible-inventory to get the full inventory
        result = subprocess.run([
            'ansible-inventory', 
            '-i', 'inventory/constructed.yml', 
            '--list'
        ], capture_output=True, text=True, check=True)
        
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running ansible-inventory: {e}", file=sys.stderr)
        print(f"Make sure Ansible is installed and inventory/constructed.yml exists", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output: {e}", file=sys.stderr)
        sys.exit(1)

def transform_inventory(original_inventory):
    """Transform inventory to use cnames and group by dashboard_group"""
    
    # Get hostvars from original inventory
    hostvars = original_inventory.get('_meta', {}).get('hostvars', {})
    
    if not hostvars:
        print("No hostvars found in inventory", file=sys.stderr)
        return {}
    
    # Create mapping of hostname -> cname and collect dashboard groups
    host_mapping = {}
    dashboard_groups = {}
    
    for hostname, host_vars in hostvars.items():
        # Use cname if available, otherwise use hostname
        cname = host_vars.get('cname', hostname)
        dashboard_group = host_vars.get('dashboard_group')
        
        # Store mapping
        host_mapping[hostname] = {
            'cname': cname,
            'dashboard_group': dashboard_group,
            'hostvars': host_vars
        }
        
        # Group by dashboard_group
        if dashboard_group:
            if dashboard_group not in dashboard_groups:
                dashboard_groups[dashboard_group] = []
            dashboard_groups[dashboard_group].append(cname)
    
    # Build new inventory structure
    new_inventory = {
        'all': {
            'hosts': list(set(data['cname'] for data in host_mapping.values()))
        },
        '_meta': {
            'hostvars': {}
        }
    }
    
    # Add dashboard groups
    for group_name, hosts in dashboard_groups.items():
        if group_name:  # Only add non-empty group names
            new_inventory[group_name] = {
                'hosts': hosts
            }
    
    # Add hostvars with cnames as keys
    for hostname, data in host_mapping.items():
        cname = data['cname']
        new_inventory['_meta']['hostvars'][cname] = data['hostvars']
    
    return new_inventory

def main():
    """Main function"""
    # Check if inventory file exists
    if not Path('inventory/constructed.yml').exists():
        print("Error: inventory/constructed.yml not found", file=sys.stderr)
        print("Please run from the project root directory", file=sys.stderr)
        sys.exit(1)
    
    # Get original inventory
    print("Reading inventory from ansible-inventory...", file=sys.stderr)
    original_inventory = get_inventory_data()
    
    # Transform inventory
    print("Transforming inventory...", file=sys.stderr)
    transformed_inventory = transform_inventory(original_inventory)
    
    # Output transformed inventory as JSON
    print(json.dumps(transformed_inventory, indent=2, sort_keys=True))
    
    # Print summary to stderr
    dashboard_groups = [k for k in transformed_inventory.keys() 
                       if k not in ['all', '_meta']]
    total_hosts = len(transformed_inventory['all']['hosts'])
    
    print(f"\nTransformation complete:", file=sys.stderr)
    print(f"  Total hosts: {total_hosts}", file=sys.stderr)
    print(f"  Dashboard groups: {len(dashboard_groups)}", file=sys.stderr)
    if dashboard_groups:
        print(f"  Groups created: {', '.join(sorted(dashboard_groups))}", file=sys.stderr)

if __name__ == '__main__':
    main()
