# Kamp Finances - Scouting Trip Finance Manager

A Python desktop application designed to help manage finances during scouting trips, specifically for tracking daily grocery expenses, personal purchases (PA), and fridge drink consumption (POEF).

## Features

### 🛒 Receipt Management
- Enter daily store receipts from Colruyt or other stores
- Categorize items into three expense types:
  - **Groepskas**: Group account expenses
  - **POEF**: Fridge drinks (tracked separately)
  - **PA**: Personal purchases for individual leaders
- Add/edit receipts with store and date information
- Automatic total calculations by category

### 👥 Leader Management
- Add and manage scouting leaders
- Track personal expenses for each leader
- Update POEF drink and cigarette counts with increment/decrement buttons
- Generate individual leader reports
- Generate global summary reports
- View detailed expense breakdowns

### 📦 PA Items Management
- View all PA items from receipts
- Efficient assignment system with dynamic leader entries
- Assign PA items to multiple leaders
- Track assignment status and counts
- Auto-save assignments when selections change

### 🥤 POEF Tracking
- Track drinks and cigarettes taken from the common fridge
- Compare total bought vs total paid
- Visual indicators for discrepancies
- Bulk POEF count updates for all leaders
- Comprehensive consumption tracking

### 📊 Financial Summary & Reporting
- Generate comprehensive expense reports
- Calculate totals by category and leader
- Export summaries for distribution
- Individual leader reports with detailed breakdowns
- Global financial summaries

### 💾 Data Management
- Automatic data persistence using CSV files
- Real-time data validation
- Changes in one tab reflected across all tabs
- Comprehensive error handling

## Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Setup
1. Clone or download the repository
2. Navigate to the project directory
3. Run the application:
   ```bash
   python run.py
   ```
   or
   ```bash
   python src/main.py
   ```

## Usage

### Getting Started
1. **Add Leaders**: Go to the "Leaders" tab and add all scouting leaders
2. **Set POEF Prices**: Configure the price per drink for each leader
3. **Start Tracking**: Begin entering daily receipts and POEF entries

### Daily Workflow
1. **Morning Shopping**: Create a new receipt and add items, categorizing them appropriately
2. **Process Messages**: Use "Process Text Message" to handle PA orders from leaders
3. **Track POEF**: Add entries when leaders take drinks from the fridge
4. **End of Day**: Review and validate the day's data

### Receipt Entry
- **Groepskas**: Items paid by the scout group account
- **POEF**: Drinks that will be paid later by individual leaders
- **PA**: Personal purchases assigned to specific leaders

### PA Items Assignment
- **Dynamic Assignment**: Add multiple leader entries as needed
- **Auto-save**: Assignments are saved automatically when selections change
- **Visual Feedback**: Clear status indicators for assignment state
- **Efficient Workflow**: Quick single-person or multi-person assignments

### POEF Management
- **Real-time Updates**: POEF totals update immediately when counts change
- **Visual Controls**: Increment/decrement buttons for easy adjustment
- **Comparison View**: See bought vs paid totals with color-coded indicators

## Architecture

### Directory Structure

```
kamp-finances/
├── src/
│   ├── main.py              # Application entry point
│   ├── models/              # Data models
│   │   ├── leader.py        # Leader model
│   │   ├── receipt.py       # Receipt and item models
│   │   └── expense.py       # Expense model
│   ├── services/            # Business logic
│   │   ├── data_service.py  # Data persistence
│   │   └── finance_service.py # Financial calculations
│   └── ui/                  # User interface
│       ├── components/      # Reusable UI components
│       │   ├── base_components.py # Base classes and common components
│       ├── tabs/            # Application tabs
│       │   ├── leaders_tab.py    # Leaders management
│       │   ├── receipts_tab.py   # Receipts and expenses
│       │   ├── pa_items_tab.py   # PA items management
│       │   └── poef_tab.py       # POEF tracking
│       └── new_main_window.py    # Main application window
├── data/                    # Data storage (created automatically)
├── requirements.txt         # Dependencies (none required)
├── run.py                  # Application launcher
└── README.md               # This file
```

### Core Components

#### Base Components (`base_components.py`)
- **BaseTab**: Base class for all tabs with common functionality
- **DataTable**: Reusable table component with sorting and filtering
- **FormDialog**: Base class for form dialogs
- **ActionButton**: Enhanced button with confirmation support

#### Main Window (`new_main_window.py`)
- Manages the overall application state
- Provides data access methods for tabs
- Handles data persistence
- Coordinates between different tabs

## Tabs Overview

### 1. Leaders Tab
**Purpose**: Manage leaders and their financial information

**Features**:
- Add/remove leaders
- View leader expenses (PA and POEF)
- Update POEF drink and cigarette counts with +/- buttons
- Generate individual leader reports
- Generate global summary reports
- Detailed expense breakdown in summary section

**Key Components**:
- Leaders table with expense totals
- Leader details panel with summary
- POEF management controls with real-time totals
- Report generation buttons

### 2. Receipts Tab
**Purpose**: Manage receipts and categorize expenses

**Features**:
- Add/edit receipts with store and date information
- Add/edit expenses within receipts
- Categorize expenses (Groepskas, POEF, PA)
- View receipt summaries and totals
- Automatic total calculations

**Key Components**:
- Compact receipts table (Date, Store, Total)
- Receipt details panel with summary
- Expenses table taking most of the space
- Expense categorization controls

### 3. PA Items Tab
**Purpose**: Manage PA (Personal Aankoop) items and assign them to leaders

**Features**:
- View all PA items from receipts
- Dynamic leader assignment system
- Auto-save assignments when selections change
- Track assignment status and leader names
- Efficient single-person and multi-person assignments

**Key Components**:
- PA items table showing assigned leader names
- Item details panel with summary
- Dynamic leader assignment entries
- Assignment status display

### 4. POEF Tab
**Purpose**: Track POEF consumption and compare bought vs paid items

**Features**:
- View all POEF items from receipts
- Track leader POEF consumption (drinks and cigarettes)
- Compare total bought vs total paid
- Visual indicators for discrepancies
- Comprehensive consumption tracking

**Key Components**:
- POEF items table from receipts
- Leader consumption table
- Summary comparison display
- Color-coded difference indicators

## Key Features

### Data Management
- **Automatic Saving**: All changes are automatically saved to CSV files
- **Data Validation**: Form validation ensures data integrity
- **Real-time Updates**: Changes in one tab are reflected across all tabs
- **Selection Preservation**: Selected items remain selected when data refreshes

### User Experience
- **Intuitive Interface**: Clean, organized layout with clear sections
- **Confirmation Dialogs**: Important actions require confirmation
- **Status Feedback**: Clear feedback for all operations
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Auto-save**: No manual save buttons needed - changes apply immediately

### Reporting
- **Individual Reports**: Detailed reports for specific leaders
- **Global Summaries**: Comprehensive financial summaries
- **Export Functionality**: Save reports as text or CSV files
- **Formatted Output**: Well-structured, readable reports

## Data Storage

The application stores all data in CSV files in the `data/` directory:
- `leaders.csv`: Leader information, expenses, and POEF drink counts
- `receipts.csv`: All store receipts
- `receipt_items_*.csv`: Individual items for each receipt

## Key Concepts

### Expense Categories
- **Groepskas**: Group expenses paid by the scout account
- **POEF**: Fridge drinks and cigarettes, tracked separately and paid by leaders
- **PA**: Personal purchases requested by individual leaders

### POEF System
- Physical list tracking drinks and cigarettes taken from common fridge
- Each leader has a personal counter
- Drinks and cigarettes are priced individually per leader
- Final settlement at end of trip

### Data Validation
The application ensures data consistency by:
- Validating receipt totals match item totals
- Checking PA items are assigned to valid leaders
- Preventing orphaned data references
- Real-time validation and error feedback

## Technical Details

### Data Models
- **Leader**: Represents a scouting leader with financial tracking
- **Receipt**: Contains multiple expenses with category totals
- **Expense**: Individual expense items with categorization
- **ExpenseCategory**: Enum for Groepskas, POEF, and PA

### Services
- **DataService**: Handles data persistence and retrieval
- **FinanceService**: Provides business logic and calculations

### UI Patterns
- **MVC-like Architecture**: Separation of data, logic, and presentation
- **Observer Pattern**: Tabs update when data changes
- **Factory Pattern**: Reusable dialog creation
- **Command Pattern**: Action buttons with confirmation

## Benefits of the New System

1. **Modularity**: Each tab is self-contained and focused
2. **Maintainability**: Clear separation of concerns
3. **Extensibility**: Easy to add new features or tabs
4. **Reusability**: Common components shared across tabs
5. **User Experience**: Intuitive interface with clear workflows
6. **Data Integrity**: Comprehensive validation and error handling
7. **Efficiency**: Auto-save and real-time updates
8. **Visual Feedback**: Clear status indicators and progress feedback

## Tips for Best Use

1. **Regular Backups**: Use the backup function regularly
2. **Daily Validation**: Run data validation after each day's entries
3. **Consistent Naming**: Use consistent item names for better tracking
4. **Export Summaries**: Export summaries regularly for safekeeping
5. **Use Auto-save**: No need to manually save - changes apply immediately
6. **Check Status**: Monitor the status bar for operation feedback

## Troubleshooting

### Common Issues
- **Data not saving**: Check file permissions in the data directory
- **Import errors**: Ensure you're running Python 3.7+
- **GUI not displaying**: Verify tkinter is available (included with most Python installations)
- **Empty summaries**: Check if leaders have PA assignments or POEF counts

### Data Recovery
- Check the `data/backup_*` directories for automatic backups
- CSV files can be manually edited if needed
- Use the validation function to check data integrity

## Contributing

This application is designed specifically for scouting trip finance management. If you have suggestions for improvements or encounter issues, please consider the specific needs of scouting organizations.

## License

This project is designed for educational and organizational use within scouting groups.

---

*Last updated: January 2024*
