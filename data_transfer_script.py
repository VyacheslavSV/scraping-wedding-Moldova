"""
Module Documentation: main.py

This module main.py serves as the entry point for executing a sequence of tasks involving web scraping and data transfer to Google Sheets.

Functions:
main(custom_keywords, credentials_file, spreadsheet_id, data_file, sheet_name)

This function orchestrates the execution of two main tasks:

Web Scraping: Initiates a search using specified keywords on Google Maps, retrieves URLs of venues, parses individual venue pages to extract data, and saves the data in a JSON file.
Data Transfer to Google Sheets: Reads the JSON file containing venue data and transfers it to a specified Google Sheets document.

Parameters:
- custom_keywords (str): Keywords used for searching on Google Maps.
- credentials_file (str): Path to the JSON file containing Google API credentials for authentication.
- spreadsheet_id (str): ID of the Google Sheets document where data will be transferred.
- data_file (str): Path to the JSON file containing the scraped data.
- sheet_name (str): Name of the sheet within the Google Sheets document where data will be placed.

Usage:
custom_keywords = 'Event venues Moldova'
credentials_file = 'credentials.json'
spreadsheet_id = 'your_spreadsheet_id'
data_file = 'data_all_companies.json'
sheet_name = 'Sheet1'

main(custom_keywords, credentials_file, spreadsheet_id, data_file, sheet_name)
"""

from data_transfer_script import transfer_data_to_gsheets
from main_script import starts_cod_to_parse


def main(custom_keywords, credentials_file, spreadsheet_id, data_file, sheet_name):
    try:
        starts_cod_to_parse(custom_keywords)
    except Exception as e:
        print(f"An error occurred during parsing: {str(e)}")

    try:
        transfer_data_to_gsheets(credentials_file, data_file, spreadsheet_id, sheet_name)
    except Exception as e:
        print(f"An error occurred during data transfer to Google Sheets: {str(e)}")


if __name__ == "__main__":
    # Settings for starting the search
    custom_keywords = 'Wedding venues places Moldova'  # Keywords for search

    # Settings for data transfer to Google Sheets
    credentials_file = 'credentials.json'  # Path to credentials file
    spreadsheet_id = 'your_spreadsheet_id'  # Your Google Sheets document ID
    data_file = 'data_all_companies.json'  # DO NOT CHANGE! Path to data file for transfer
    sheet_name = 'Sheet1'  # Name of the sheet where you want to place the data

    main(custom_keywords, credentials_file, spreadsheet_id, data_file, sheet_name)
