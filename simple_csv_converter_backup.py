#!/usr/bin/env python3
"""
Simplified CSV to Ansible inventory converter using Ansible's native features
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
        for row in reader:
            hostname = row.get('hostname')
            if hostname:
                # Clean up empty values
                clean_vars = {k: v for k, v in row.items() if v and v.strip()}
                hosts_data[hostname] = clean_vars
    
    print(f"✓ Read {len(hosts_data)} hosts from CSV")
    return hosts_data


def create_simple_inventory(hosts_data):
    """Create a base inventory file with all hosts and variables embedded"""
    
    inventory_file = Path('inventory/hosts.yml')
    inventory_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create inventory with all hosts and variables
    simple_inventory = {
        'all': {
            'hosts': {}
        }
    }
    
    # Add all hosts and their variables to the inventory
    for hostname, variables in hosts_data.items():
        simple_inventory['all']['hosts'][hostname] = variables
    
    with open(inventory_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("# Base inventory file with all hosts and variables listed\n")
        f.write("# Groups are created dynamically by constructed.yml\n\n")
        yaml.dump(simple_inventory, f, default_flow_style=False)
    
    print(f"✓ Created base inventory with {len(hosts_data)} hosts and variables: {inventory_file}")
    return inventory_file


def create_constructed_config():
    """Create Ansible constructed inventory configuration"""
    
    config_file = Path('inventory/constructed.yml')
    
    constructed_config = {
        'plugin': 'constructed',
        'strict': False,
        'sources': ['hosts.yml'],
        'compose': {
            # Create useful composed variables
            'env_batch': 'environment + "_" + (batch_number | string)',
            'app_env': 'application_service + "_" + environment',
            'site_env': 'site_code + "_" + environment'
        },
        'keyed_groups': [
            # Batch groups - the main feature you wanted
            {
                'key': 'batch_number',
                'prefix': 'batch',
                'separator': '_'
            },
            # Environment groups
            {
                'key': 'environment',
                'prefix': 'env',
                'separator': '_'
            },
            # Application service groups
            {
                'key': 'application_service',
                'prefix': 'app',
                'separator': '_'
            },
            # Product groups
            {
                'key': 'product_1',
                'prefix': 'product',
                'separator': '_'
            },
            # Site groups
            {
                'key': 'site_code',
                'prefix': 'site',
                'separator': '_'
            },
            # Status groups
            {
                'key': 'status',
                'prefix': 'status',
                'separator': '_'
            }
        ],
        'groups': {
            # Create conditional groups
            'production_hosts': 'environment == "production"',
            'development_hosts': 'environment == "development"',
            'test_hosts': 'environment == "test"',
            'active_hosts': 'status == "active"',
            'web_servers': 'application_service == "web_server"',
            'api_servers': 'application_service == "api_server"',
            'db_servers': 'application_service == "database_server"',
            
            # Combined groups
            'production_batch_1': 'environment == "production" and batch_number == "1"',
            'production_batch_2': 'environment == "production" and batch_number == "2"',
            'production_batch_3': 'environment == "production" and batch_number == "3"',
            'development_batch_1': 'environment == "development" and batch_number == "1"',
            'development_batch_2': 'environment == "development" and batch_number == "2"',
        }
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("# Ansible constructed inventory plugin configuration\n")
        f.write("# This creates groups dynamically based on host variables\n")
        f.write("# Usage: ansible-inventory -i inventory/constructed.yml --list\n\n")
        yaml.dump(constructed_config, f, default_flow_style=False, sort_keys=True)
    
    print(f"✓ Created constructed config: {config_file}")
    return config_file


def create_usage_examples():
    """Create usage examples and documentation"""
    
    examples_file = Path('inventory/USAGE.md')
    
    usage_content = """# Simplified Ansible Inventory Usage

## Files Created

- `inventory/hosts.yml` - Base inventory with embedded host variables
- `inventory/constructed.yml` - Dynamic group configuration

## Usage Examples

### List all hosts
```bash
ansible-inventory -i inventory/constructed.yml --list
```

### List hosts in batch_1
```bash
ansible-inventory -i inventory/constructed.yml --list-hosts batch_1
```

### Show all batch groups
```bash
ansible-inventory -i inventory/constructed.yml --list | grep batch_
```

### Run playbook on specific batch
```bash
ansible-playbook -i inventory/constructed.yml playbook.yml --limit batch_1
```

### Run playbook on production batch_2
```bash
ansible-playbook -i inventory/constructed.yml playbook.yml --limit production_batch_2
```

### List all groups
```bash
ansible-inventory -i inventory/constructed.yml --graph
```

### Get host variables
```bash
ansible-inventory -i inventory/constructed.yml --host test-web-01
```

## Available Groups

### Automatic Groups (keyed_groups)
- `batch_1`, `batch_2`, `batch_3` - Based on batch_number
- `env_production`, `env_development`, `env_test` - Based on environment
- `app_web_server`, `app_api_server`, `app_database_server` - Based on application_service
- `product_web`, `product_api`, `product_db` - Based on product_1
- `site_us_east_1` - Based on site_code
- `status_active` - Based on status

### Conditional Groups
- `production_hosts` - All production hosts
- `development_hosts` - All development hosts
- `test_hosts` - All test hosts
- `active_hosts` - All active hosts
- `web_servers` - All web servers
- `api_servers` - All API servers
- `db_servers` - All database servers

### Combined Groups
- `production_batch_1` - Production hosts in batch 1
- `production_batch_2` - Production hosts in batch 2
- `development_batch_1` - Development hosts in batch 1
- etc.

## Benefits

1. **Dynamic** - Groups are created automatically based on host variables
2. **Flexible** - Easy to add new grouping criteria
3. **Standard** - Uses Ansible's built-in features
4. **Fast** - No custom Python code to maintain
5. **Powerful** - Supports complex conditional grouping

## Customization

Edit `inventory/constructed.yml` to:
- Add new keyed_groups
- Modify group naming patterns
- Add conditional groups
- Create composed variables

## Migration from Complex System

The simplified system provides the same functionality:
- ✅ Batch groups (`batch_1`, `batch_2`, etc.)
- ✅ Environment groups (`env_production`, etc.)
- ✅ Application groups (`app_web_server`, etc.)
- ✅ Product groups (`product_web`, etc.)
- ✅ Site groups (`site_us_east_1`, etc.)
|- ✅ Host variables (embedded in hosts.yml)
- ✅ All Ansible commands work the same way

But with much less code to maintain!
"""
    
    with open(examples_file, 'w', encoding='utf-8') as f:
        f.write(usage_content)
    
    print(f"✓ Created usage examples: {examples_file}")
    return examples_file


def main():
    """Main function to create simplified inventory system"""
    
    print("Creating Simplified Ansible Inventory System")
    print("=" * 50)
    
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
        
        # Create constructed configuration
        create_constructed_config()
        
        # Create usage examples
        create_usage_examples()
        
        print("\n" + "=" * 50)
        print("✅ Simplified inventory system created successfully!")
        print(f"✅ Converted {len(hosts_data)} hosts from CSV")
        print("\nNext steps:")
        print("1. Test the inventory:")
        print("   ansible-inventory -i inventory/constructed.yml --list")
        print("2. List batch groups:")
        print("   ansible-inventory -i inventory/constructed.yml --list-hosts batch_1")
        print("3. View the graph:")
        print("   ansible-inventory -i inventory/constructed.yml --graph")
        print("4. Read the usage guide:")
        print("   cat inventory/USAGE.md")
        
    except Exception as e:
        print(f"❌ Error creating simplified inventory: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()