#!/usr/bin/env python3
"""
Create a test inventory file to demonstrate batch_number grouping
"""

import csv
import yaml
from pathlib import Path
from datetime import datetime

def create_test_inventory():
    """Create test inventory files showing batch_number grouping"""
    
    # Read test CSV data
    test_csv_file = 'test_batch_sample.csv'
    
    print(f"Creating test inventory from: {test_csv_file}")
    
    # Read CSV data
    hosts = []
    with open(test_csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            hosts.append(row)
    
    # Group hosts by environment
    environments = {}
    for host in hosts:
        env = host.get('environment')
        if env not in environments:
            environments[env] = []
        environments[env].append(host)
    
    # Create inventory for each environment
    for env, env_hosts in environments.items():
        inventory = {
            'all': {
                'children': {
                    f'env_{env}': {}
                }
            }
        }
        
        # Environment group
        env_group = f'env_{env}'
        inventory[env_group] = {
            'hosts': {},
            'children': {}
        }
        
        # Track batch groups for this environment
        batch_groups_in_env = {}
        
        # Add hosts to environment group and collect batch info
        for host in env_hosts:
            hostname = host.get('hostname')
            batch_number = host.get('batch_number')
            
            # Add to environment group
            inventory[env_group]['hosts'][hostname] = {}
            
            # Group by batch
            if batch_number:
                batch_group = f'batch_{batch_number}'
                if batch_group not in batch_groups_in_env:
                    batch_groups_in_env[batch_group] = []
                batch_groups_in_env[batch_group].append(hostname)
        
        # Add batch groups as children of environment group
        for batch_group in batch_groups_in_env.keys():
            inventory[env_group]['children'][batch_group] = {}
        
        # Create individual batch groups
        for batch_group, batch_hosts in batch_groups_in_env.items():
            inventory[batch_group] = {
                'hosts': {},
                'children': {}
            }
            for hostname in batch_hosts:
                inventory[batch_group]['hosts'][hostname] = {}
        
        # Write inventory file
        output_file = f'test_inventory_{env}.yml'
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write("# ----------------------------------------------------------------------\n")
            f.write("# TEST INVENTORY FILE - DEMONSTRATES BATCH_NUMBER GROUPING\n")
            f.write("# This file shows how batch_number creates groups in the inventory\n")
            f.write("# ----------------------------------------------------------------------\n")
            f.write(f"# {env.title()} Environment Test Inventory\n")
            f.write(f"# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Hosts in this environment: {len(env_hosts)}\n")
            f.write(f"# Batch groups: {', '.join(sorted(batch_groups_in_env.keys()))}\n")
            f.write("\n")
            
            # Write YAML
            yaml.dump(inventory, f, default_flow_style=False, sort_keys=True)
        
        print(f"Created: {output_file}")
        
        # Print summary
        print(f"  Environment: {env}")
        print(f"  Hosts: {len(env_hosts)}")
        print(f"  Batch groups: {', '.join(sorted(batch_groups_in_env.keys()))}")
        for batch_group, batch_hosts in sorted(batch_groups_in_env.items()):
            print(f"    {batch_group}: {len(batch_hosts)} hosts ({', '.join(batch_hosts)})")
        print()

if __name__ == "__main__":
    create_test_inventory()