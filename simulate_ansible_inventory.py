#!/usr/bin/env python3
"""
Simulate what ansible-inventory would show (for testing without Ansible installed)
"""

import yaml
import json
from pathlib import Path

def load_host_vars(hostname):
    """Load host variables for a hostname"""
    host_vars_file = Path(f'inventory/host_vars/{hostname}.yml')
    if host_vars_file.exists():
        with open(host_vars_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}

def simulate_constructed_inventory():
    """Simulate what the constructed plugin would create"""
    
    # Load base inventory
    with open('inventory/hosts.yml', 'r', encoding='utf-8') as f:
        base_inventory = yaml.safe_load(f)
    
    # Load constructed config
    with open('inventory/constructed.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Get all hosts from base inventory
    all_hosts = list(base_inventory.get('all', {}).get('hosts', {}).keys())
    
    print(f"Base hosts found: {all_hosts}")
    
    # Load host vars for all hosts
    hosts_data = {}
    for hostname in all_hosts:
        hosts_data[hostname] = load_host_vars(hostname)
        print(f"Host {hostname}: {hosts_data[hostname]}")
    
    # Simulate keyed_groups
    inventory = {
        'all': {
            'hosts': all_hosts
        },
        '_meta': {
            'hostvars': hosts_data
        }
    }
    
    keyed_groups = config.get('keyed_groups', [])
    for group_config in keyed_groups:
        key = group_config.get('key')
        prefix = group_config.get('prefix', '')
        separator = group_config.get('separator', '_')
        
        print(f"\nProcessing keyed_group: key={key}, prefix={prefix}")
        
        # Create groups based on key values
        groups_created = {}
        for hostname, host_vars in hosts_data.items():
            value = host_vars.get(key)
            if value:
                group_name = f"{prefix}{separator}{value}"
                if group_name not in groups_created:
                    groups_created[group_name] = []
                groups_created[group_name].append(hostname)
        
        # Add groups to inventory
        for group_name, group_hosts in groups_created.items():
            inventory[group_name] = {
                'hosts': group_hosts
            }
            print(f"  Created group: {group_name} with hosts: {group_hosts}")
    
    # Simulate conditional groups
    conditional_groups = config.get('groups', {})
    print(f"\nProcessing conditional groups...")
    
    for group_name, condition in conditional_groups.items():
        group_hosts = []
        
        # Simple condition evaluation (basic cases only)
        for hostname, host_vars in hosts_data.items():
            try:
                # Replace variable names with actual values in condition
                eval_condition = condition
                for var_name, var_value in host_vars.items():
                    if isinstance(var_value, str):
                        eval_condition = eval_condition.replace(var_name, f'"{var_value}"')
                    else:
                        eval_condition = eval_condition.replace(var_name, str(var_value))
                
                # Basic evaluation (simplified)
                if eval(eval_condition):
                    group_hosts.append(hostname)
            except:
                # Skip complex conditions for this simulation
                pass
        
        if group_hosts:
            inventory[group_name] = {
                'hosts': group_hosts
            }
            print(f"  Created conditional group: {group_name} with hosts: {group_hosts}")
    
    return inventory

def main():
    """Main simulation function"""
    print("Simulating ansible-inventory output...")
    print("=" * 50)
    
    try:
        inventory = simulate_constructed_inventory()
        
        print("\n" + "=" * 50)
        print("SIMULATED INVENTORY OUTPUT:")
        print("=" * 50)
        
        # Show groups like ansible-inventory --list would
        print(json.dumps(inventory, indent=2, sort_keys=True))
        
        print("\n" + "=" * 50)
        print("BATCH GROUPS FOUND:")
        print("=" * 50)
        
        batch_groups = {k: v for k, v in inventory.items() if k.startswith('batch_')}
        for group_name, group_data in sorted(batch_groups.items()):
            hosts = group_data.get('hosts', [])
            print(f"{group_name}: {hosts} ({len(hosts)} hosts)")
        
        if not batch_groups:
            print("❌ No batch groups found!")
            return False
        else:
            print("✅ Batch groups created successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error simulating inventory: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()