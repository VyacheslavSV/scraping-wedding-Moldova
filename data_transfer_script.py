import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def transfer_data_to_gsheets(credentials_file, data_file, spreadsheet_id, sheet_name):
    # Authorization and access to the spreadsheet
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(spreadsheet_id)
    sheet = spreadsheet.worksheet(sheet_name)

    # Reading data from the JSON file
    with open(data_file) as file:
        data = json.load(file)

    # Check that the data is not empty and is a list
    if data and isinstance(data, list):
        # Get headers (keys of dictionaries)
        headers = list(data[0].keys())
        # Write headers to the first row
        sheet.insert_row(headers, index=1)

        # Write data to Google Sheets starting from the second row
        rows = [[item[key] for key in headers] for item in data]
        sheet.insert_rows(rows, row=2)

    print("Data successfully transferred to Google Sheets!")
