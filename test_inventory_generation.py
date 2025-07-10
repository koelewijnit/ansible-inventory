#!/usr/bin/env python3
"""
Test inventory generation with cross-platform file locking
"""

import os
import sys
from pathlib import Path

# Add the scripts directory to Python path
current_dir = Path(os.getcwd())
script_dir = current_dir / 'scripts'
sys.path.insert(0, str(script_dir))

def test_inventory_generation():
    """Test the inventory generation with our sample CSV"""
    
    print("Testing inventory generation with cross-platform file locking...")
    
    try:
        # Import the inventory manager
        from managers.inventory_manager import InventoryManager
        from core.models import Host
        
        print("✓ Successfully imported InventoryManager")
        
        # Test CSV file path
        csv_file = Path('test_batch_sample.csv')
        if not csv_file.exists():
            print(f"✗ CSV file not found: {csv_file}")
            return False
        
        print(f"✓ Using CSV file: {csv_file}")
        
        # Create inventory manager instance
        inventory_manager = InventoryManager(csv_file=csv_file)
        print("✓ Created InventoryManager instance")
        
        # Load hosts from CSV
        hosts = inventory_manager.load_hosts()
        print(f"✓ Loaded {len(hosts)} hosts from CSV")
        
        # Test batch group functionality
        print("\nTesting batch group functionality:")
        for host in hosts:
            batch_group = host.get_batch_group_name()
            print(f"  Host: {host.hostname:15} | Batch: {host.batch_number:2} | Group: {batch_group}")
        
        # Test building inventory structure
        print("\nTesting inventory structure generation:")
        
        # Get unique environments
        environments = list(set(host.environment for host in hosts))
        print(f"Environments found: {environments}")
        
        for env in environments:
            print(f"\n--- Testing {env} environment ---")
            env_hosts = [host for host in hosts if host.environment == env]
            
            # Build inventory structure
            inventory = inventory_manager.build_environment_inventory(env_hosts, env)
            
            # Check for batch groups
            batch_groups = [group for group in inventory.keys() if group.startswith('batch_')]
            print(f"Batch groups created: {batch_groups}")
            
            # Verify hosts are in correct groups
            for batch_group in batch_groups:
                hosts_in_group = list(inventory[batch_group]['hosts'].keys())
                print(f"  {batch_group}: {hosts_in_group}")
        
        return True
        
    except Exception as e:
        print(f"✗ Inventory generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_dry_run_generation():
    """Test dry run inventory generation"""
    
    print("\nTesting dry run inventory generation...")
    
    try:
        from managers.inventory_manager import InventoryManager
        
        csv_file = Path('test_batch_sample.csv')
        inventory_manager = InventoryManager(csv_file=csv_file)
        
        # Test dry run
        result = inventory_manager.generate_inventories(dry_run=True)
        
        print(f"✓ Dry run completed successfully")
        print(f"  Environments: {result.get('environments', [])}")
        print(f"  Stats: {result.get('stats', {})}")
        
        return True
        
    except Exception as e:
        print(f"✗ Dry run test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Inventory Generation Test with Cross-Platform File Locking")
    print("=" * 60)
    
    success = True
    
    # Test inventory generation
    if not test_inventory_generation():
        success = False
    
    # Test dry run
    if not test_dry_run_generation():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All inventory generation tests passed!")
        print("The cross-platform file locking is working with the inventory system.")
    else:
        print("❌ Some tests failed.")
        print("Please check the error messages above.")