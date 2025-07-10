# Simplified Ansible Inventory Approach

## Current Complexity vs. Ansible Native Features

### Current Approach (Complex)
- Custom group creation logic
- Manual inventory file generation
- Complex hierarchy management
- Custom file locking
- Lots of Python code for group management

### Simplified Approach (Ansible Native)
- Use Ansible's `constructed` inventory plugin
- Use `keyed_groups` for automatic group creation
- Leverage Ansible's built-in inventory features
- Minimal custom code

## Simplified Implementation Options

### Option 1: Constructed Inventory Plugin with keyed_groups

Instead of generating static YAML files, use Ansible's `constructed` plugin:

```yaml
# inventory/constructed.yml
plugin: constructed
strict: false
compose:
  # Create composed variables
  env_batch: environment + "_" + batch_number
  app_product: application_service + "_" + product_1

keyed_groups:
  # Create batch groups automatically
  - key: batch_number
    prefix: batch
    separator: "_"
  
  # Create environment groups
  - key: environment
    prefix: env
    separator: "_"
  
  # Create application groups
  - key: application_service
    prefix: app
    separator: "_"
  
  # Create product groups
  - key: product_1
    prefix: product
    separator: "_"
    
  # Create site groups
  - key: site_code
    prefix: site
    separator: "_"

groups:
  # Create conditional groups
  production_batch_1: environment == "production" and batch_number == "1"
  development_batch_2: environment == "development" and batch_number == "2"
  
  # Create combined groups
  web_servers: application_service == "web_server"
  api_servers: application_service == "api_server"
  db_servers: application_service == "database_server"
```

### Option 2: Simple CSV to Inventory Converter

Create a much simpler Python script:

```python
#!/usr/bin/env python3
"""
Simplified CSV to Ansible inventory converter
"""

import csv
import yaml
import sys
from pathlib import Path

def csv_to_inventory(csv_file, output_file=None):
    """Convert CSV to simple Ansible inventory with host_vars"""
    
    # Read CSV
    hosts = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            hosts.append(row)
    
    # Create simple inventory structure
    inventory = {
        'all': {
            'hosts': {},
            'children': {
                'ungrouped': {
                    'hosts': {}
                }
            }
        }
    }
    
    # Add all hosts to ungrouped (let Ansible handle grouping)
    for host in hosts:
        hostname = host['hostname']
        inventory['all']['children']['ungrouped']['hosts'][hostname] = {}
        
        # Create host_vars file
        host_vars_dir = Path('inventory/host_vars')
        host_vars_dir.mkdir(exist_ok=True)
        
        with open(host_vars_dir / f"{hostname}.yml", 'w') as f:
            yaml.dump(host, f, default_flow_style=False)
    
    # Write simple inventory
    output_path = output_file or 'inventory/hosts.yml'
    with open(output_path, 'w') as f:
        yaml.dump(inventory, f, default_flow_style=False)
    
    print(f"✓ Created simple inventory: {output_path}")
    print(f"✓ Created {len(hosts)} host_vars files")
    print("✓ Use constructed.yml for dynamic grouping")

if __name__ == "__main__":
    csv_to_inventory('test_batch_sample.csv')
```

### Option 3: Use Ansible's auto plugin with host_vars

Even simpler - just create host_vars and let Ansible auto-discover:

```bash
# Create basic directory structure
mkdir -p inventory/host_vars

# Convert CSV to individual host_vars files (one-liner)
python3 -c "
import csv, yaml, pathlib
with open('test_batch_sample.csv') as f:
    for row in csv.DictReader(f):
        pathlib.Path(f'inventory/host_vars/{row[\"hostname\"]}.yml').write_text(yaml.dump(row))
"

# Create minimal inventory file
echo 'all:' > inventory/hosts.yml
```

Then use constructed plugin for grouping.

## Benefits of Simplified Approach

### 1. Less Code to Maintain
- ~3,000 lines → ~100 lines
- No custom group logic
- No file locking needed
- No complex hierarchy management

### 2. More Flexible
- Groups are created dynamically
- Easy to add new grouping criteria
- Ansible handles all the complexity
- Standard Ansible patterns

### 3. Better Performance
- Ansible's native code is optimized
- No Python overhead for group creation
- Faster inventory parsing
- Better caching

### 4. Ansible Best Practices
- Uses standard Ansible features
- Compatible with all Ansible tools
- Follows Ansible documentation
- Community supported

## Implementation Comparison

### Current Implementation (Complex)
```python
# 50+ lines of complex group creation logic
def build_environment_inventory(self, hosts, environment):
    inventory = defaultdict(lambda: {"hosts": {}, "children": {}})
    # ... complex logic for each group type
    for host in hosts:
        # ... manual group assignment
        if host.batch_number:
            batch_group = host.get_batch_group_name()
            # ... more complex logic
```

### Simplified Implementation (Ansible Native)
```yaml
# 5 lines in constructed.yml
keyed_groups:
  - key: batch_number
    prefix: batch
    separator: "_"
```

## Migration Path

### Step 1: Create Simplified CSV Converter
```python
# Simple 20-line script to convert CSV to host_vars
```

### Step 2: Create Constructed Inventory
```yaml
# configured.yml with keyed_groups
```

### Step 3: Test
```bash
ansible-inventory -i inventory/constructed.yml --list
```

### Step 4: Migrate Existing Usage
```bash
# Old way
ansible-playbook -i inventory/production.yml playbook.yml --limit batch_1

# New way (same result)
ansible-playbook -i inventory/constructed.yml playbook.yml --limit batch_1
```

## Recommended Approach

I recommend **Option 1** with the constructed plugin because:

1. **Minimal code** - Just a simple CSV to host_vars converter
2. **Maximum flexibility** - Easy to add new grouping rules
3. **Ansible native** - Uses standard Ansible features
4. **Future proof** - Compatible with Ansible updates
5. **Better performance** - Let Ansible handle the heavy lifting

Would you like me to implement this simplified approach?