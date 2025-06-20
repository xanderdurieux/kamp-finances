#!/usr/bin/env python3
"""
Test script to verify that adding a leader works and gets saved.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.leader import Leader
from services.data_service import DataService

def test_add_leader():
    """Test adding a leader and verifying it's saved."""
    print("🧪 Testing leader addition and saving...")
    
    # Initialize data service
    data_service = DataService()
    
    # Create a test leader (like "Xander")
    test_leader = Leader(
        name="Xander",
        phone_number="987654321",
        email="xander@example.com"
    )
    
    # Set some POEF drink count
    test_leader.set_poef_drink_count(5)
    print(f"🥤 Set POEF drink count to: {test_leader.poef_drink_count}")
    
    # Load existing leaders
    existing_leaders = data_service.load_leaders()
    print(f"📂 Found {len(existing_leaders)} existing leaders")
    
    # Add the new leader
    existing_leaders.append(test_leader)
    print(f"➕ Added leader: {test_leader.name}")
    
    # Save all leaders
    data_service.save_leaders(existing_leaders)
    print("💾 Saved leaders to file")
    
    # Load leaders back to verify
    loaded_leaders = data_service.load_leaders()
    print(f"📂 Loaded {len(loaded_leaders)} leaders from file")
    
    # Check if Xander is in the loaded leaders
    xander = next((l for l in loaded_leaders if l.name == "Xander"), None)
    if xander:
        print(f"✅ Found Xander in saved data:")
        print(f"   Name: {xander.name}")
        print(f"   Phone: {xander.phone_number}")
        print(f"   Email: {xander.email}")
        print(f"   ID: {xander.id}")
        print(f"   POEF drinks: {xander.poef_drink_count}")
        print(f"   POEF total: €{xander.get_poef_total():.2f}")
        print("✅ Leader addition test PASSED!")
        return True
    else:
        print("❌ Xander not found in saved data!")
        print("❌ Leader addition test FAILED!")
        return False

if __name__ == "__main__":
    success = test_add_leader()
    if success:
        print("\n🎉 Test passed!")
    else:
        print("\n💥 Test failed!")
        sys.exit(1) 