# Simplified Ansible Inventory Usage

## Files Created

- `inventory/hosts.yml` - Simple base inventory
- `inventory/constructed.yml` - Dynamic group configuration
- `inventory/host_vars/*.yml` - Individual host variables

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
- ✅ Host variables (in `host_vars/` files)
- ✅ All Ansible commands work the same way

But with much less code to maintain!
