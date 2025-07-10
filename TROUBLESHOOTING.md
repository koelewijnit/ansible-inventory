# Troubleshooting Guide

## Issue: `ansible-inventory --list` Shows No Groups

### Problem Fixed ✅
The original issue was that `hosts.yml` was empty and didn't actually list any hosts. The `constructed` plugin needs a base inventory with hosts defined.

### Solution Applied
Updated `simple_csv_converter.py` to:
1. Create `hosts.yml` with all hosts listed
2. Add `sources: ['hosts.yml']` to `constructed.yml`
3. Ensure host variables are properly loaded from `host_vars/`

## Testing the Fix

### 1. Verify Base Inventory
Check that `inventory/hosts.yml` contains all hosts:
```bash
cat inventory/hosts.yml
```

Should show:
```yaml
all:
  hosts:
    test-web-01: {}
    test-api-01: {}
    # ... all your hosts
```

### 2. Verify Host Variables
Check that host_vars files exist:
```bash
ls inventory/host_vars/
cat inventory/host_vars/test-web-01.yml
```

Should show host variables including `batch_number`.

### 3. Test with Ansible (if installed)

#### Basic Test
```bash
# Test basic inventory listing
ansible-inventory -i inventory/constructed.yml --list

# Test specific batch group
ansible-inventory -i inventory/constructed.yml --list-hosts batch_1

# Show inventory graph
ansible-inventory -i inventory/constructed.yml --graph
```

#### Verbose Debugging
```bash
# Show detailed parsing information
ansible-inventory -i inventory/constructed.yml --list -vvv
```

### 4. Simulation Test (without Ansible)
If you don't have Ansible installed, use our simulation:
```bash
python simulate_ansible_inventory.py
```

This should show:
```
BATCH GROUPS FOUND:
batch_1: ['dev-db-01', 'dev-web-01', 'test-web-01'] (3 hosts)
batch_2: ['dev-api-01', 'test-api-01', 'test-cache-01'] (3 hosts)
batch_3: ['test-db-01', 'test-monitor-01'] (2 hosts)
✅ Batch groups created successfully!
```

## Common Issues & Solutions

### Issue 1: Empty Inventory Output
**Symptoms**: `ansible-inventory --list` returns just `{}`

**Causes & Solutions**:
- ❌ **No hosts in base inventory**: Regenerate with `python simple_csv_converter.py`
- ❌ **Wrong file path**: Use `-i inventory/constructed.yml` (not just `constructed.yml`)
- ❌ **Missing host_vars**: Ensure `inventory/host_vars/*.yml` files exist

### Issue 2: No Batch Groups
**Symptoms**: Groups shown but no `batch_1`, `batch_2`, etc.

**Causes & Solutions**:
- ❌ **Missing batch_number in CSV**: Ensure CSV has `batch_number` column
- ❌ **Empty batch_number values**: Check CSV for empty cells
- ❌ **Wrong keyed_groups config**: Verify `constructed.yml` has:
  ```yaml
  keyed_groups:
    - key: batch_number
      prefix: batch
      separator: _
  ```

### Issue 3: Plugin Not Found
**Symptoms**: `ERROR! Invalid plugin FQCN (ansible.builtin.constructed)`

**Causes & Solutions**:
- ❌ **Old Ansible version**: Upgrade to Ansible 2.9+
- ❌ **Missing plugin**: Install `ansible-core` package
- ❌ **Wrong plugin name**: Ensure `plugin: constructed` in YAML

### Issue 4: YAML Syntax Errors
**Symptoms**: `ERROR! We were unable to read either as JSON nor YAML`

**Causes & Solutions**:
- ❌ **Invalid YAML**: Use `yamllint inventory/constructed.yml`
- ❌ **Encoding issues**: Ensure files are UTF-8 encoded
- ❌ **Tabs vs spaces**: Use spaces only in YAML files

## Expected Output

After fixing, `ansible-inventory -i inventory/constructed.yml --graph` should show:
```
@all:
  |--@batch_1:
  |  |--dev-db-01
  |  |--dev-web-01
  |  |--test-web-01
  |--@batch_2:
  |  |--dev-api-01
  |  |--test-api-01
  |  |--test-cache-01
  |--@batch_3:
  |  |--test-db-01
  |  |--test-monitor-01
  |--@env_development:
  |  |--dev-api-01
  |  |--dev-db-01
  |  |--dev-web-01
  |--@env_production:
  |  |--test-api-01
  |  |--test-db-01
  |  |--test-web-01
  # ... more groups
```

## Verification Commands

### Test Batch Groups Work
```bash
# List all hosts in batch_1
ansible-inventory -i inventory/constructed.yml --list-hosts batch_1

# List all hosts in production batch_2
ansible-inventory -i inventory/constructed.yml --list-hosts production_batch_2

# Show host variables for specific host
ansible-inventory -i inventory/constructed.yml --host test-web-01
```

### Test Playbook Integration
```bash
# Run playbook on batch_1 only
ansible-playbook -i inventory/constructed.yml site.yml --limit batch_1 --check

# Run on production batch_3 hosts
ansible-playbook -i inventory/constructed.yml site.yml --limit production_batch_3 --check
```

## Alternative Testing Methods

### 1. JSON Output Analysis
```bash
ansible-inventory -i inventory/constructed.yml --list | jq 'keys[]' | grep batch_
```

Should output:
```
"batch_1"
"batch_2"
"batch_3"
```

### 2. Host Group Membership
```bash
ansible-inventory -i inventory/constructed.yml --host test-web-01 | jq '.group_names[]'
```

Should include groups like:
```
"batch_1"
"env_production"
"product_web"
"app_web_server"
```

## Getting Help

If you're still having issues:

1. **Check Ansible version**: `ansible --version` (need 2.9+)
2. **Validate YAML syntax**: `yamllint inventory/constructed.yml`
3. **Test with verbose output**: `ansible-inventory -i inventory/constructed.yml --list -vvv`
4. **Use our simulation**: `python simulate_ansible_inventory.py`
5. **Check the logs**: Look for error messages in verbose output

The fix ensures that the batch grouping functionality works exactly as intended!