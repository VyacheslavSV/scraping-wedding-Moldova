# scraping-wedding-Moldova
scraping wedding Moldova use google map
Overview:
This repository contains Python scripts for web scraping venue data from Google Maps and transferring the scraped data to Google Sheets.

Prerequisites:
1. Python 3.x installed on your system.
2. Install required libraries:
    - pip install -r requirements.txt
Usage:
1. Setup:

    - Obtain Google API credentials (credentials.json) for Google Sheets API access.
    - Ensure your Google Sheets document is created with appropriate permissions.
2. Configuration:

    - Modify custom_keywords, credentials_file, spreadsheet_id, data_file, and sheet_name in main.py according to your needs.
3. Execution:
    - Run main.py:
        - python main.py
4. Error Handling:

    - Any errors encountered during web scraping or data transfer will be displayed in the console.
5. Notes:

    - Ensure all paths and IDs (spreadsheet_id, sheet_name, etc.) are correctly configured.
    - The main.py script integrates with data_transfer_script.py for Google Sheets data transfer and main_script.py for web scraping functionality.

