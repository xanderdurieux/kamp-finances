#!/usr/bin/env python3
"""
Test script for Kamp Finances application.
This script tests if the application can start without errors.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import tkinter as tk
from tkinter import ttk, messagebox

def test_imports():
    """Test if all modules can be imported."""
    try:
        print("Testing imports...")
        
        # Test model imports
        from models.leader import Leader
        from models.receipt import Receipt, ReceiptItem, ExpenseCategory
        from models.expense import Expense
        
        # Test service imports
        from services.data_service import DataService
        from services.finance_service import FinanceService
        
        # Test UI imports
        from ui.main_window import MainWindow
        from ui.leaders_tab import LeadersTab
        from ui.receipts_tab import ReceiptsTab
        from ui.poef_tab import PoefTab
        from ui.summary_tab import SummaryTab
        from ui.dialogs import LeaderDialog, ReceiptItemDialog, TextMessageDialog
        
        print("✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_models():
    """Test model creation and basic functionality."""
    try:
        print("Testing models...")
        
        from models.leader import Leader
        from models.receipt import Receipt, ReceiptItem, ExpenseCategory
        
        # Test Leader model
        leader = Leader(name="Test Leader", phone_number="123456789", email="test@example.com")
        assert leader.name == "Test Leader"
        assert leader.total_pa_expenses == 0.0
        assert leader.poef_drink_count == 0
        assert leader.poef_price_per_drink == 0.75
        
        # Test POEF functionality
        leader.set_poef_drink_count(5)
        assert leader.poef_drink_count == 5
        assert leader.get_poef_total() == 5 * 0.75
        
        # Test Receipt model
        receipt = Receipt(date="2024-01-01")
        assert receipt.date == "2024-01-01"
        assert receipt.total_amount == 0.0
        
        # Test ReceiptItem model
        item = ReceiptItem(name="Test Item", price=2.50, category=ExpenseCategory.GROEPSKAS)
        assert item.name == "Test Item"
        assert item.price == 2.50
        assert item.get_total_price() == 2.50
        
        print("✅ All model tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Model test error: {e}")
        return False

def test_services():
    """Test service functionality."""
    try:
        print("Testing services...")
        
        from services.data_service import DataService
        from services.finance_service import FinanceService
        
        # Test DataService
        data_service = DataService(data_dir="test_data")
        assert data_service.data_dir == "test_data"
        
        # Test FinanceService
        finance_service = FinanceService(data_service)
        assert finance_service.data_service == data_service
        
        print("✅ All service tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Service test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Kamp Finances Application")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Models", test_models),
        ("Services", test_services),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed!")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("python src/main.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 