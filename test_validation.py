#!/usr/bin/env python3
"""
Comprehensive validation of the simplified inventory system
"""

import yaml
import csv
import json
from pathlib import Path

def test_csv_reading():
    """Test CSV file can be read properly"""
    print("Testing CSV reading...")
    
    csv_file = Path('inventory_source/sample_hosts.csv')
    if not csv_file.exists():
        print("❌ CSV file not found")
        return False
    
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            print(f"✅ Read {len(rows)} rows from CSV")
            
            # Check required columns
            required_cols = ['hostname', 'batch_number']
            if rows:
                for col in required_cols:
                    if col not in rows[0]:
                        print(f"❌ Missing required column: {col}")
                        return False
                print(f"✅ Required columns present: {required_cols}")
            
            # Show sample data
            if rows:
                print("Sample row:", dict(rows[0]))
            
            return True
    except Exception as e:
        print(f"❌ CSV reading error: {e}")
        return False

def test_yaml_syntax():
    """Test that generated YAML files have valid syntax"""
    print("\nTesting YAML syntax...")
    
    yaml_files = [
        'inventory/hosts.yml',
        'inventory/constructed.yml'
    ]
    
    for yaml_file in yaml_files:
        file_path = Path(yaml_file)
        if not file_path.exists():
            print(f"❌ YAML file not found: {yaml_file}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            print(f"✅ Valid YAML syntax: {yaml_file}")
        except yaml.YAMLError as e:
            print(f"❌ YAML syntax error in {yaml_file}: {e}")
            return False
    
    return True

def test_constructed_config():
    """Test constructed.yml configuration"""
    print("\nTesting constructed.yml configuration...")
    
    config_file = Path('inventory/constructed.yml')
    if not config_file.exists():
        print("❌ constructed.yml not found")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Check required fields
        required_fields = ['plugin', 'keyed_groups']
        for field in required_fields:
            if field not in config:
                print(f"❌ Missing required field in constructed.yml: {field}")
                return False
        
        print(f"✅ Required fields present: {required_fields}")
        
        # Check plugin type
        if config['plugin'] != 'constructed':
            print(f"❌ Wrong plugin type: {config['plugin']}")
            return False
        
        print("✅ Plugin type correct: constructed")
        
        # Check keyed_groups structure
        keyed_groups = config.get('keyed_groups', [])
        batch_group_found = False
        
        for group in keyed_groups:
            if not isinstance(group, dict):
                print(f"❌ Invalid keyed_group structure: {group}")
                return False
            
            if 'key' not in group or 'prefix' not in group:
                print(f"❌ Missing key or prefix in keyed_group: {group}")
                return False
            
            if group.get('key') == 'batch_number':
                batch_group_found = True
                if group.get('prefix') != 'batch':
                    print(f"❌ Wrong prefix for batch_number: {group.get('prefix')}")
                    return False
        
        if not batch_group_found:
            print("❌ batch_number keyed_group not found")
            return False
        
        print("✅ batch_number keyed_group configured correctly")
        return True
        
    except Exception as e:
        print(f"❌ Error testing constructed.yml: {e}")
        return False

def test_host_vars():
    """Test host_vars files"""
    print("\nTesting host_vars files...")
    
    host_vars_dir = Path('inventory/host_vars')
    if not host_vars_dir.exists():
        print("❌ host_vars directory not found")
        return False
    
    host_files = list(host_vars_dir.glob('*.yml'))
    if not host_files:
        print("❌ No host_vars files found")
        return False
    
    print(f"✅ Found {len(host_files)} host_vars files")
    
    # Test a sample file
    sample_file = host_files[0]
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            host_data = yaml.safe_load(f)
        
        # Check for required fields
        if 'hostname' not in host_data and 'batch_number' not in host_data:
            print(f"❌ Missing required fields in {sample_file.name}")
            return False
        
        print(f"✅ Valid host_vars structure in {sample_file.name}")
        print(f"   Sample data: {dict(list(host_data.items())[:3])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading {sample_file}: {e}")
        return False

def test_expected_groups():
    """Test that we can predict what groups should be created"""
    print("\nTesting expected group creation...")
    
    # Read CSV to predict groups
    csv_file = Path('inventory_source/sample_hosts.csv')
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Predict batch groups
        batch_numbers = set()
        environments = set()
        applications = set()
        
        for row in rows:
            if row.get('batch_number'):
                batch_numbers.add(row['batch_number'])
            if row.get('environment'):
                environments.add(row['environment'])
            if row.get('application_service'):
                applications.add(row['application_service'])
        
        expected_batch_groups = [f"batch_{bn}" for bn in sorted(batch_numbers)]
        expected_env_groups = [f"env_{env}" for env in sorted(environments)]
        expected_app_groups = [f"app_{app}" for app in sorted(applications)]
        
        print(f"✅ Expected batch groups: {expected_batch_groups}")
        print(f"✅ Expected environment groups: {expected_env_groups}")
        print(f"✅ Expected application groups: {expected_app_groups}")
        
        # Verify constructed.yml would create these
        config_file = Path('inventory/constructed.yml')
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        keyed_groups = config.get('keyed_groups', [])
        group_keys = [kg.get('key') for kg in keyed_groups]
        
        expected_keys = ['batch_number', 'environment', 'application_service']
        for key in expected_keys:
            if key not in group_keys:
                print(f"❌ Missing keyed_group for {key}")
                return False
        
        print(f"✅ All expected keyed_groups configured: {expected_keys}")
        return True
        
    except Exception as e:
        print(f"❌ Error predicting groups: {e}")
        return False

def main():
    """Run all validation tests"""
    print("Comprehensive Validation of Simplified Inventory System")
    print("=" * 60)
    
    tests = [
        test_csv_reading,
        test_yaml_syntax,
        test_constructed_config,
        test_host_vars,
        test_expected_groups
    ]
    
    passed = 0
    for test_func in tests:
        if test_func():
            passed += 1
        else:
            print("❌ Test failed!")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("✅ ALL TESTS PASSED - System appears to be working correctly!")
        print("\nNext step: Test with actual Ansible commands:")
        print("  ansible-inventory -i inventory/constructed.yml --list")
    else:
        print("❌ Some tests failed - please review the errors above")
    
    return passed == len(tests)

if __name__ == "__main__":
    main()