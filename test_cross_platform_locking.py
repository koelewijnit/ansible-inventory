#!/usr/bin/env python3
"""
Test cross-platform file locking functionality
"""

import os
import sys
import tempfile
import time
from pathlib import Path

# Add the scripts directory to Python path
current_dir = Path(os.getcwd())
script_dir = current_dir / 'scripts'
sys.path.insert(0, str(script_dir))

def test_file_locking():
    """Test the cross-platform file locking"""
    
    print("Testing cross-platform file locking...")
    
    # Test platform detection
    try:
        import fcntl
        print("✓ fcntl module available (Unix/Linux/macOS)")
        has_fcntl = True
    except ImportError:
        print("✗ fcntl module not available")
        has_fcntl = False
    
    try:
        import msvcrt
        print("✓ msvcrt module available (Windows)")
        has_msvcrt = True
    except ImportError:
        print("✗ msvcrt module not available")
        has_msvcrt = False
    
    # Test importing our cross-platform utils
    try:
        from core.utils import file_lock, get_logger
        print("✓ Successfully imported cross-platform file_lock")
    except ImportError as e:
        print(f"✗ Failed to import file_lock: {e}")
        return False
    
    # Test file locking with a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_path = Path(tmp_file.name)
        tmp_file.write("test content")
    
    try:
        print(f"Testing file locking with: {tmp_path}")
        
        # Test acquiring and releasing lock
        with file_lock(tmp_path, mode='r', timeout=5) as locked_file:
            print("✓ Successfully acquired file lock")
            content = locked_file.read()
            print(f"✓ Read content: '{content.strip()}'")
            time.sleep(0.1)  # Hold lock briefly
        
        print("✓ Successfully released file lock")
        
        # Test reading without lock
        with open(tmp_path, 'r') as normal_file:
            content = normal_file.read()
            print(f"✓ Read without lock: '{content.strip()}'")
        
        return True
        
    except Exception as e:
        print(f"✗ File locking test failed: {e}")
        return False
    finally:
        # Clean up
        if tmp_path.exists():
            tmp_path.unlink()


def test_inventory_import():
    """Test importing the inventory management modules"""
    
    print("\nTesting inventory management imports...")
    
    try:
        # Test core modules
        from core.models import Host
        print("✓ Successfully imported Host model")
        
        from core.config import load_config
        print("✓ Successfully imported config")
        
        # Test creating a host
        host_data = {
            'hostname': 'test-host',
            'environment': 'development',
            'batch_number': '1'
        }
        
        host = Host.from_csv_row(host_data)
        batch_group = host.get_batch_group_name()
        print(f"✓ Created host: {host.hostname}")
        print(f"✓ Batch group: {batch_group}")
        
        return True
        
    except Exception as e:
        print(f"✗ Inventory import test failed: {e}")
        return False


if __name__ == "__main__":
    print("Cross-Platform File Locking Test")
    print("=" * 40)
    
    success = True
    
    # Test file locking
    if not test_file_locking():
        success = False
    
    # Test inventory imports
    if not test_inventory_import():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("✅ All tests passed!")
        print("The cross-platform file locking is working correctly.")
    else:
        print("❌ Some tests failed.")
        print("Please check the error messages above.")