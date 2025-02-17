# FIFA World Cup Finals Web Scraping

A Python script that scrapes FIFA World Cup finals data from Wikipedia and optionally exports it to Google Sheets.

## Features

- Scrapes World Cup finals data including:
  - Year
  - Winner
  - Score
  - Runners-up
- Interactive filtering options
- Custom notes addition
- Column selection for export
- Google Sheets integration

## Prerequisites

- Python 3.x
- BeautifulSoup4
- Requests
- Google Sheets API


You'll also need:
- Chrome WebDriver installed
- Google Sheets API credentials file

## Usage

1. Configure Google Sheets:
   - Set your `SHEET_ID` in the script
   - Place your credentials file and update `CREDENTIALS_FILE` path

2. Run the script:

3. Interactive Features:
   - Choose number of rows to fetch (1-22)
   - Optional search functionality
   - Click interactions for specific years
   - Toggle additional details
   - Apply filters:
     - All data
     - Winners with >2 goals
     - Specific year range
   - Add custom notes
   - Select columns for export
   - Export to Google Sheets

## Implementation Details

### Key Components

1. **Page Navigation**
   - Opens Wikipedia page for FIFA World Cup finals
   - Handles dynamic page loading

2. **Data Extraction**
   - Uses Selenium WebDriver for reliable scraping
   - Implements explicit waits for element loading
   - Extracts data from specific table cells using XPath

3. **User Interactions**
   - Search functionality
   - Click operations
   - Checkbox toggles
   - Custom note addition
   - Column selection

4. **Data Processing**
   - Pandas DataFrame operations
   - Data filtering options
   - Column selection

5. **Google Sheets Integration**
   - Appends data to specified sheet
   - Handles API authentication
   - Error handling for failed operations

## Error Handling

- Robust error handling for:
  - Web element interactions
  - Data extraction
  - Google Sheets operations
  - User input validation

## Functions

- `fill_search_field()`: Handles search input
- `click_element()`: Manages click operations
- `toggle_checkbox()`: Controls checkbox states
- `append_to_sheets()`: Handles Google Sheets export
- `get_world_cup_data()`: Main scraping function
- `get_filtered_data()`: Implements filtering options
- `add_custom_notes()`: Manages custom annotations
- `select_columns()`: Handles column selection