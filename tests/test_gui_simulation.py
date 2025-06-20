#!/usr/bin/env python3
"""
Test script to simulate the GUI flow for adding a leader.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.leader import Leader
from services.data_service import DataService
from ui.main_window import MainWindow
import tkinter as tk

def test_gui_simulation():
    """Simulate the exact GUI flow for adding a leader."""
    print("🧪 Testing GUI simulation for adding a leader...")
    
    # Create a minimal root window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Initialize services
    from services.finance_service import FinanceService
    data_service = DataService()
    finance_service = FinanceService(data_service)
    
    # Load existing data
    leaders = data_service.load_leaders()
    receipts = data_service.load_receipts()
    
    print(f"📂 Initial leaders count: {len(leaders)}")
    
    # Create main window (this simulates what happens in the real app)
    main_window = MainWindow(
        root, 
        finance_service,
        data_service,
        leaders,  # Pass reference to leaders list
        receipts  # Pass reference to receipts list
    )
    
    # Simulate adding a leader (this is what happens when you click "Add Leader")
    test_leader = Leader(
        name="GUI Test Leader",
        phone_number="555123456",
        email="gui.test@example.com"
    )
    
    print(f"➕ Creating leader: {test_leader.name}")
    
    # Call the add_leader method (this is what the GUI does)
    main_window.add_leader(test_leader)
    
    print(f"📂 Leaders count after adding: {len(main_window.leaders)}")
    
    # Check if the leader was added to the list
    added_leader = next((l for l in main_window.leaders if l.name == "GUI Test Leader"), None)
    if added_leader:
        print(f"✅ Leader found in main window: {added_leader.name}")
    else:
        print("❌ Leader not found in main window!")
        return False
    
    # Check if the file was actually saved
    data_service.save_all_data(main_window.leaders, main_window.receipts)
    
    # Load from file to verify
    loaded_leaders = data_service.load_leaders()
    print(f"📂 Leaders loaded from file: {len(loaded_leaders)}")
    
    # Check if the leader is in the file
    file_leader = next((l for l in loaded_leaders if l.name == "GUI Test Leader"), None)
    if file_leader:
        print(f"✅ Leader found in file: {file_leader.name}")
        print(f"   Phone: {file_leader.phone_number}")
        print(f"   Email: {file_leader.email}")
        print("✅ GUI simulation test PASSED!")
        return True
    else:
        print("❌ Leader not found in file!")
        print("❌ GUI simulation test FAILED!")
        return False

if __name__ == "__main__":
    success = test_gui_simulation()
    if success:
        print("\n🎉 Test passed!")
    else:
        print("\n💥 Test failed!")
        sys.exit(1) 