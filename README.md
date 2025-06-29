# Kamp Finances - Scouting Trip Finance Manager

A Python desktop application designed to help manage finances during scouting trips, specifically for tracking daily grocery expenses, personal purchases (PA), and fridge drink consumption (POEF).

## 📁 Project Structure

```
kamp-finances/
├── src/                          # Source code directory
│   ├── main.py                   # Main application entry point
│   ├── models/                   # Data models
│   │   ├── leader.py            # Leader model with POEF tracking
│   │   ├── receipt.py           # Receipt model with expense items
│   │   └── expense.py           # Expense model with categories
│   ├── services/                 # Business logic services
│   │   ├── data_service.py      # Data persistence and CSV handling
│   │   └── finance_service.py   # Financial calculations and reporting
│   └── ui/                      # User interface components
│       ├── main_window.py       # Main application window with tabs
│       ├── base_components.py   # Reusable UI components
│       ├── leaders_tab.py       # Leaders management tab
│       ├── pa_tab.py           # PA items assignment tab
│       ├── poef_tab.py         # POEF tracking tab
│       └── receipts_tab.py     # Receipts management tab
├── data/                        # Data storage directory
│   ├── leaders.csv             # Leaders data file
│   └── receipts.csv            # Receipts data file
├── dist/                       # Built executable (after build)
├── venv/                       # Python virtual environment
├── run.py                      # Application launcher script
├── requirements.txt            # Python dependencies (none external)
├── kamp_finances.spec          # PyInstaller specification file
├── build.sh                    # Build script for executable
├── test_executable.sh          # Test script for built executable
└── README.md                   # This file
```

## 🏗️ Architecture & Components

### Data Models (`src/models/`)
- **Leader**: Manages leader information, POEF counts, and PA purchases
- **Receipt**: Handles store receipts with date, store name, and expense items
- **Expense**: Represents individual items with price, quantity, and category

### Services (`src/services/`)
- **DataService**: Handles CSV file operations, data persistence, and serialization
- **FinanceService**: Provides financial calculations, reporting, and summary generation

### User Interface (`src/ui/`)
- **MainWindow**: Tabbed interface container with automatic data refresh
- **BaseComponents**: Reusable UI components (DataTable, FormDialog, ActionButton)
- **Tab Components**: Specialized tabs for each functional area

### Key Features

#### 🛒 Receipt Management
- Add, edit, and remove daily store receipts from Colruyt or other stores
- Categorize items into three expense types:
  - **Groepskas**: Group account expenses
  - **POEF**: Fridge drinks (tracked separately)
  - **PA**: Personal purchases for individual leaders
- Add, edit, and remove individual expenses within receipts
- Automatic total calculations by category
- Confirmation dialogs for safe deletion operations
- Compact receipt list showing date, store, and total

#### 👥 Leader Management
- Add, edit, and remove scouting leaders
- Track personal expenses for each leader
- Update POEF drink and cigarette counts with increment/decrement buttons (+/-)
- Direct entry of POEF counts with auto-save on focus out or Enter key
- Real-time total calculations for drinks and cigarettes
- Generate individual leader reports with detailed breakdowns
- Export leader summaries to TXT and CSV formats
- Detailed expense breakdown showing shared PA items and costs
- Selection preservation when updating POEF counts

#### 📦 PA Items Management
- View all PA items from receipts with assigned leader information
- Dynamic assignment system with add/remove leader entries
- Assign PA items to multiple leaders with automatic cost splitting
- Auto-save assignments when selections change
- Track assignment status and individual leader amounts
- Visual feedback showing assigned leader names and their share amounts
- Advanced assignment management dialog for bulk operations
- Cost sharing: when multiple leaders share an item, cost is split equally

#### 🥤 POEF Tracking
- View all POEF items from receipts with store and date information
- Track drinks and cigarettes taken from the common fridge
- Compare total bought vs total paid with visual indicators
- Color-coded difference display (green=balanced, orange=overbought, red=underbought)
- Comprehensive consumption tracking per leader
- Real-time summary updates showing totals and discrepancies

#### 📊 Financial Summary & Reporting
- Generate comprehensive expense reports for individual leaders
- Calculate totals by category and leader
- Export summaries for distribution (TXT and CSV formats)
- Individual leader reports with detailed breakdowns
- Global financial summaries
- Detailed expense tracking with sharing information

#### 💾 Data Management
- Automatic data persistence using CSV files
- Real-time data validation and error handling
- Changes in one tab reflected across all tabs automatically
- Comprehensive error handling with user-friendly messages
- Auto-save functionality - no manual save buttons needed
- Data consistency maintained across all operations
- Proper cleanup when removing receipts (removes PA assignments and CSV files)

#### 🔄 User Experience
- Tab-based interface with automatic data refresh on tab changes
- Confirmation dialogs for all deletion operations
- Selection preservation during data updates
- Intuitive layout with clear sections and visual feedback
- Status indicators and progress feedback
- Error handling with clear user messages

## 🚀 Installation & Usage

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Development Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd kamp-finances
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Run the application:
   ```bash
   python run.py
   ```

### Building Executable
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   ./build.sh
   ```

3. Test the executable:
   ```bash
   ./test_executable.sh
   ```

The executable will be created in `dist/KampFinances` and can be run on any Linux system without Python installed.

## 📖 Usage Guide

### Getting Started
1. **Add Leaders**: Go to the Leaders tab and add the scouting leaders who will be participating
2. **Add Receipts**: In the Receipts tab, add daily store receipts from your shopping trips
3. **Categorize Items**: For each item in a receipt, assign it to the appropriate category:
   - **Groepskas**: Group expenses (food, supplies, etc.)
   - **POEF**: Drinks and snacks for the common fridge
   - **PA**: Personal purchases for individual leaders
4. **Assign PA Items**: In the PA Items tab, assign personal purchases to the appropriate leaders
5. **Track POEF**: Update drink and cigarette counts for each leader in the Leaders tab
6. **Generate Reports**: Use the export features to generate financial summaries

### Key Workflows

#### Daily Receipt Entry
1. Add a new receipt with date and store name
2. Add individual items with price, quantity, and category
3. Items are automatically categorized and totals calculated

#### PA Item Assignment
1. Select a PA item from the list
2. Add leaders to the assignment using the "+ Add Leader" button
3. Assignments are automatically saved and costs split equally

#### POEF Tracking
1. Select a leader in the Leaders tab
2. Use +/- buttons or direct entry to update drink/cigarette counts
3. Totals are calculated automatically in real-time

#### Financial Reporting
1. Select a leader and click "Generate Report" for individual summaries
2. Use "Export to TXT/CSV" for distribution
3. View global summaries for overall trip finances

## 🔧 Technical Details

### Data Storage
- All data is stored in CSV files in the `data/` directory
- Automatic backup and recovery mechanisms
- Data integrity maintained across all operations

### Error Handling
- Comprehensive validation for all user inputs
- Graceful error recovery with user-friendly messages
- Automatic data consistency checks

### Performance
- Efficient data loading and caching
- Real-time updates without performance impact
- Optimized for typical scouting trip data volumes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues or questions:
1. Check the existing issues
2. Create a new issue with detailed information
3. Include system information and error messages

---

**Kamp Finances** - Making scouting trip finances simple and organized! 🏕️💰
