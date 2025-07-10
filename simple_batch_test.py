#!/usr/bin/env python3
"""
Simple test to verify batch_number grouping functionality
"""

import csv
from pathlib import Path

def test_batch_grouping():
    """Test batch_number grouping functionality"""
    
    # Read test CSV data
    test_csv_file = 'test_batch_sample.csv'
    
    print(f"Testing batch_number grouping functionality...")
    print(f"Using CSV file: {test_csv_file}")
    
    # Read CSV data
    hosts = []
    with open(test_csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            hosts.append(row)
    
    print(f"\nTotal hosts in CSV: {len(hosts)}")
    
    # Test batch group name generation
    print("\n=== Host and Batch Information ===")
    for host in hosts:
        hostname = host.get('hostname', 'N/A')
        batch_number = host.get('batch_number', 'N/A')
        environment = host.get('environment', 'N/A')
        batch_group = f"batch_{batch_number}" if batch_number != 'N/A' else 'N/A'
        print(f"Host: {hostname:15} | Env: {environment:12} | Batch: {batch_number:2} | Group: {batch_group}")
    
    # Test inventory structure
    print("\n=== Batch Group Summary ===")
    batch_groups = {}
    for host in hosts:
        batch_number = host.get('batch_number')
        if batch_number:
            batch_group = f"batch_{batch_number}"
            if batch_group not in batch_groups:
                batch_groups[batch_group] = []
            batch_groups[batch_group].append(host.get('hostname'))
    
    for batch_group in sorted(batch_groups.keys()):
        hosts_in_batch = batch_groups[batch_group]
        print(f"{batch_group}: {hosts_in_batch} ({len(hosts_in_batch)} hosts)")
    
    # Test environment + batch grouping
    print("\n=== Environment + Batch Grouping ===")
    env_batch_groups = {}
    for host in hosts:
        env = host.get('environment')
        batch_number = host.get('batch_number')
        if env and batch_number:
            key = f"{env}_batch_{batch_number}"
            if key not in env_batch_groups:
                env_batch_groups[key] = []
            env_batch_groups[key].append(host.get('hostname'))
    
    for key in sorted(env_batch_groups.keys()):
        hosts_in_group = env_batch_groups[key]
        print(f"{key}: {hosts_in_group} ({len(hosts_in_group)} hosts)")
    
    # Generate sample inventory YAML structure
    print("\n=== Sample Inventory Structure ===")
    environments = list(set(host.get('environment') for host in hosts))
    
    for env in sorted(environments):
        print(f"\n--- {env.upper()} ENVIRONMENT ---")
        env_hosts = [host for host in hosts if host.get('environment') == env]
        
        # Environment group
        env_group = f"env_{env}"
        print(f"{env_group}:")
        print(f"  hosts:")
        for host in env_hosts:
            print(f"    {host.get('hostname')}: {{}}")
        
        # Batch groups for this environment
        batch_groups_in_env = {}
        for host in env_hosts:
            batch_number = host.get('batch_number')
            if batch_number:
                batch_group = f"batch_{batch_number}"
                if batch_group not in batch_groups_in_env:
                    batch_groups_in_env[batch_group] = []
                batch_groups_in_env[batch_group].append(host.get('hostname'))
        
        print(f"  children:")
        for batch_group in sorted(batch_groups_in_env.keys()):
            print(f"    {batch_group}: {{}}")
        
        # Individual batch groups
        for batch_group in sorted(batch_groups_in_env.keys()):
            print(f"{batch_group}:")
            print(f"  hosts:")
            for hostname in batch_groups_in_env[batch_group]:
                print(f"    {hostname}: {{}}")
    
    return True

if __name__ == "__main__":
    test_batch_grouping()