#!/usr/bin/env python3
"""
Generate actual inventory files with batch groups
"""

import os
import sys
from pathlib import Path

# Add the scripts directory to Python path
current_dir = Path(os.getcwd())
script_dir = current_dir / 'scripts'
sys.path.insert(0, str(script_dir))

def generate_inventory():
    """Generate actual inventory files using our sample CSV"""
    
    print("Generating actual inventory files with batch groups...")
    
    try:
        from managers.inventory_manager import InventoryManager
        
        # Use our test CSV file
        csv_file = Path('test_batch_sample.csv')
        
        # Create inventory manager
        inventory_manager = InventoryManager(csv_file=csv_file)
        
        # Generate inventories for specific environments
        environments = ['production', 'development', 'test']
        
        print(f"Generating inventories for: {environments}")
        
        result = inventory_manager.generate_inventories(
            environments=environments,
            dry_run=False
        )
        
        print(f"✓ Generated {len(result['generated_files'])} inventory files")
        
        for file_path in result['generated_files']:
            print(f"  - {file_path}")
        
        # Display stats
        stats = result.get('stats', {})
        print(f"\nGeneration Statistics:")
        print(f"  Total hosts: {stats.get('total_hosts', 0)}")
        print(f"  Active hosts: {stats.get('active_hosts', 0)}")
        print(f"  Generation time: {stats.get('generation_time', 0):.3f}s")
        print(f"  Orphaned files removed: {stats.get('orphaned_files_removed', 0)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Inventory generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def display_generated_inventories():
    """Display the generated inventory files"""
    
    print("\nDisplaying generated inventory files...")
    
    inventory_files = [
        'inventory/production.yml',
        'inventory/development.yml', 
        'inventory/test.yml'
    ]
    
    for file_path in inventory_files:
        path = Path(file_path)
        if path.exists():
            print(f"\n--- {file_path} ---")
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Display first 30 lines to avoid too much output
                lines = content.split('\n')[:30]
                for line in lines:
                    print(line)
                total_lines = len(content.split('\n'))
                if total_lines > 30:
                    print(f"... [truncated - full file has {total_lines} lines]")
        else:
            print(f"✗ File not found: {file_path}")


if __name__ == "__main__":
    print("Ansible Inventory Generation with Batch Groups")
    print("=" * 50)
    
    success = generate_inventory()
    
    if success:
        display_generated_inventories()
        print("\n" + "=" * 50)
        print("✅ Inventory generation completed successfully!")
        print("Batch groups are now available in the inventory files.")
        print("\nYou can now use batch groups in Ansible commands:")
        print("  ansible-inventory -i inventory/production.yml --list-hosts batch_1")
        print("  ansible-playbook playbook.yml --limit batch_2")
    else:
        print("\n" + "=" * 50)
        print("❌ Inventory generation failed.")