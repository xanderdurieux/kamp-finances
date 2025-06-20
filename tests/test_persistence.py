#!/usr/bin/env python3
"""
Test script to verify data persistence is working.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.leader import Leader
from services.data_service import DataService

def test_persistence():
    """Test that data persistence is working."""
    print("🧪 Testing data persistence...")
    
    # Initialize data service
    data_service = DataService()
    print(f"📁 Data directory: {data_service.data_dir}")
    print(f"📄 Leaders file path: {data_service._get_file_path('leaders.json')}")
    
    # Create a test leader
    test_leader = Leader(
        name="Test Leader",
        phone_number="123456789",
        email="test@example.com"
    )
    
    # Save the leader
    print(f"💾 Saving leader: {test_leader.name}")
    data_service.save_leaders([test_leader])
    
    # Check if file exists and has content
    leaders_file = data_service._get_file_path("leaders.json")
    if os.path.exists(leaders_file):
        with open(leaders_file, 'r') as f:
            content = f.read()
            print(f"📄 File content: {content}")
    else:
        print("❌ Leaders file does not exist!")
    
    # Load leaders back
    print("📂 Loading leaders...")
    loaded_leaders = data_service.load_leaders()
    
    # Check if the leader was saved correctly
    if loaded_leaders:
        leader = loaded_leaders[0]
        print(f"✅ Leader loaded: {leader.name}")
        print(f"   Phone: {leader.phone_number}")
        print(f"   Email: {leader.email}")
        print(f"   ID: {leader.id}")
        
        # Verify data matches
        if (leader.name == test_leader.name and 
            leader.phone_number == test_leader.phone_number and
            leader.email == test_leader.email):
            print("✅ Data persistence test PASSED!")
            return True
        else:
            print("❌ Data persistence test FAILED - data mismatch!")
            return False
    else:
        print("❌ Data persistence test FAILED - no leaders loaded!")
        return False

if __name__ == "__main__":
    success = test_persistence()
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n💥 Tests failed!")
        sys.exit(1) 