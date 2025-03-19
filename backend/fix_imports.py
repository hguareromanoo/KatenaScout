#!/usr/bin/env python3
"""
Script to fix import statements by removing 'backend.' prefix
This is needed for deployment environments where the backend directory is the root
"""

import os
import re
import glob

def fix_imports_in_file(file_path):
    """Fix imports in a single file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace import statements
    fixed_content = re.sub(r'from backend\.', 'from ', content)
    fixed_content = re.sub(r'import backend\.', 'import ', fixed_content)
    
    # If changes were made, write back to file
    if fixed_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        return True
    return False

def main():
    """Find and fix all .py files"""
    # Get script directory (backend root)
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all .py files
    py_files = glob.glob(f"{backend_dir}/**/*.py", recursive=True)
    
    # Exclude virtual environment files
    py_files = [f for f in py_files if "venv" not in f]
    
    fixed_count = 0
    for py_file in py_files:
        if fix_imports_in_file(py_file):
            fixed_count += 1
            print(f"Fixed imports in {os.path.relpath(py_file, backend_dir)}")
    
    print(f"\nFixed imports in {fixed_count} files.")

if __name__ == "__main__":
    main()