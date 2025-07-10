#!/usr/bin/env python3
"""
Test script to verify batch_number grouping functionality
"""

import sys
import os
import yaml
import csv
from pathlib import Path

# Add the scripts directory to Python path
current_dir = Path(os.getcwd())
script_dir = current_dir / 'scripts'
sys.path.insert(0, str(script_dir))

# Import the necessary modules
from core.models import Host
from managers.inventory_manager import InventoryManager

def test_batch_grouping():
    """Test batch_number grouping functionality"""
    
    # Create test CSV data
    test_csv_file = Path(os.getcwd()) / 'test_batch_sample.csv'
    
    print(f"Testing batch_number grouping functionality...")
    print(f"Using CSV file: {test_csv_file}")
    
    # Read CSV data manually and create hosts
    hosts = []
    with open(test_csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                host = Host.from_csv_row(row)
                hosts.append(host)
                print(f"Created host: {host.hostname} (batch: {host.batch_number})")
            except Exception as e:
                print(f"Error creating host from row {row}: {e}")
    
    print(f"\nTotal hosts created: {len(hosts)}")
    
    # Test batch group name generation
    print("\n=== Testing batch group name generation ===")
    for host in hosts:
        batch_group = host.get_batch_group_name()
        print(f"Host: {host.hostname:15} | Batch: {host.batch_number:2} | Group: {batch_group}")
    
    # Test inventory generation logic (simplified)
    print("\n=== Testing inventory structure ===")
    
    # Group hosts by environment
    env_groups = {}
    for host in hosts:
        if host.environment not in env_groups:
            env_groups[host.environment] = []
        env_groups[host.environment].append(host)
    
    # Build inventory for each environment
    for env, env_hosts in env_groups.items():
        print(f"\n--- Environment: {env} ---")
        
        # Create inventory structure
        inventory = {
            'all': {'children': {}},
            f'env_{env}': {'hosts': {}, 'children': {}}
        }
        
        # Add hosts to environment group
        for host in env_hosts:
            host_key = host.hostname
            inventory[f'env_{env}']['hosts'][host_key] = {}
            
            # Add batch group
            if host.batch_number:
                batch_group = host.get_batch_group_name()
                if batch_group not in inventory:
                    inventory[batch_group] = {'hosts': {}, 'children': {}}
                inventory[f'env_{env}']['children'][batch_group] = {}
                inventory[batch_group]['hosts'][host_key] = {}
        
        # Add environment group to 'all'
        inventory['all']['children'][f'env_{env}'] = {}
        
        # Display the inventory structure
        print(f"Inventory structure for {env}:")
        for group, data in inventory.items():
            if group == 'all':
                continue
            hosts_in_group = list(data.get('hosts', {}).keys())
            if hosts_in_group:
                print(f"  {group}: {hosts_in_group}")
    
    print("\n=== Batch group summary ===")
    batch_groups = {}
    for host in hosts:
        if host.batch_number:
            batch_group = host.get_batch_group_name()
            if batch_group not in batch_groups:
                batch_groups[batch_group] = []
            batch_groups[batch_group].append(host.hostname)
    
    for batch_group, batch_hosts in sorted(batch_groups.items()):
        print(f"{batch_group}: {batch_hosts}")
    
    return True

if __name__ == "__main__":
    test_batch_grouping()