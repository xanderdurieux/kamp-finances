#!/usr/bin/env python3
"""
Test script to check the current state of the leaders.json file.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.data_service import DataService

def test_current_state():
    """Check the current state of the data."""
    print("🔍 Checking current data state...")
    
    # Initialize data service
    data_service = DataService()
    
    # Load current data
    leaders = data_service.load_leaders()
    receipts = data_service.load_receipts()
    
    print(f"📂 Current leaders in file: {len(leaders)}")
    print(f"📂 Current receipts in file: {len(receipts)}")
    
    # Show all leaders
    for i, leader in enumerate(leaders, 1):
        print(f"  {i}. {leader.name} (ID: {leader.id})")
        print(f"     Phone: {leader.phone_number}")
        print(f"     Email: {leader.email}")
        print(f"     POEF drinks: {leader.poef_drink_count}")
        print(f"     PA expenses: €{leader.total_pa_expenses:.2f}")
        print()
    
    # Check file size
    import os
    leaders_file = data_service._get_file_path("leaders.json")
    if os.path.exists(leaders_file):
        size = os.path.getsize(leaders_file)
        print(f"📄 Leaders.json file size: {size} bytes")
        
        # Show file content
        with open(leaders_file, 'r') as f:
            content = f.read()
            print(f"📄 File content preview: {content[:200]}...")
    else:
        print("❌ Leaders.json file does not exist!")
    
    return True

if __name__ == "__main__":
    test_current_state() 