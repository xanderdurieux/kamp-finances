# Kamp Finances - Scouting Trip Finance Manager

A Python desktop application designed to help manage finances during scouting trips, specifically for tracking daily grocery expenses, personal purchases (PA), and fridge drink consumption (POEF).

## Features

### 🛒 Receipt Management
- Enter daily store receipts from Colruyt or other stores
- Categorize items into three expense types:
  - **Groepskas**: Group account expenses
  - **POEF**: Fridge drinks (tracked separately)
  - **PA**: Personal purchases for individual leaders

### 👥 Leader Management
- Add and manage scouting leaders
- Track personal expenses for each leader
- Store contact information (phone, email)

### 📱 Text Message Processing
- Process text messages containing PA orders
- Automatically extract items and prices from messages
- Support for common formats like "PA: item1, item2" or "PA item1 €2.50"

### 🥤 POEF Tracking
- Track drinks taken from the common fridge
- Set individual prices per drink for each leader
- Maintain a physical list equivalent

### 📊 Financial Summary
- Generate comprehensive expense reports
- Calculate totals by category and leader
- Export summaries for distribution

### 💾 Data Management
- Automatic data persistence using JSON files
- Backup functionality
- Data validation to ensure consistency

## Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Setup
1. Clone or download the repository
2. Navigate to the project directory
3. Run the application:
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

### Text Message Processing
The application can parse messages like:
- "PA: cola, chips, chocolate"
- "PA cola €2.50, chips €1.80"
- "persoonlijke aankoop: energy drink"

## File Structure

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
│       ├── main_window.py   # Main application window
│       ├── leaders_tab.py   # Leaders management tab
│       ├── receipts_tab.py  # Receipts management tab
│       ├── poef_tab.py      # POEF tracking tab
│       ├── summary_tab.py   # Summary and reports tab
│       └── dialogs.py       # Dialog components
├── data/                    # Data storage (created automatically)
├── requirements.txt         # Dependencies (none required)
└── README.md               # This file
```

## Data Storage

The application stores all data in JSON files in the `data/` directory:
- `leaders.json`: Leader information, expenses, and POEF drink counts
- `receipts.json`: All store receipts and items

## Key Concepts

### Expense Categories
- **Groepskas**: Group expenses paid by the scout account
- **POEF**: Fridge drinks, tracked separately and paid by leaders
- **PA**: Personal purchases requested by individual leaders

### POEF System
- Physical list tracking drinks taken from common fridge
- Each leader has a personal counter
- Drinks are priced individually per leader
- Final settlement at end of trip

### Data Validation
The application ensures data consistency by:
- Validating receipt totals match item totals
- Checking PA items are assigned to valid leaders
- Preventing orphaned data references

## Tips for Best Use

1. **Regular Backups**: Use the backup function regularly
2. **Daily Validation**: Run data validation after each day's entries
3. **Consistent Naming**: Use consistent item names for better tracking
4. **Export Summaries**: Export summaries regularly for safekeeping

## Troubleshooting

### Common Issues
- **Data not saving**: Check file permissions in the data directory
- **Import errors**: Ensure you're running Python 3.7+
- **GUI not displaying**: Verify tkinter is available (included with most Python installations)

### Data Recovery
- Check the `data/backup_*` directories for automatic backups
- JSON files can be manually edited if needed
- Use the validation function to check data integrity

## Contributing

This application is designed specifically for scouting trip finance management. If you have suggestions for improvements or encounter issues, please consider the specific needs of scouting organizations.

## License

This project is designed for educational and organizational use within scouting groups.

---
