from fastapi import FastAPI, HTTPException
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

# Initialize FastAPI app
app = FastAPI()

# Google Sheets API setup
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = None

if SERVICE_ACCOUNT_FILE:
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
else:
    raise Exception("The path to the Google Service Account credentials file is not set.")

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Your Google Sheet ID
SHEET_ID = '1tJP4mFtH-2bkquzrWxKvfw-D8ZF0Geb-I70Zw2p8IjA'

@app.get("/read-analyze-sheet/")
async def read_analyze_sheet(range: str):
    try:
        # Read data from the specified range
        result = sheet.values().get(spreadsheetId=SHEET_ID, range=range).execute()
        values = result.get('values', [])

        if not values:
            raise HTTPException(status_code=404, detail="No data found in the specified range.")

        # Example of a simple data analysis: Count the number of rows and columns
        num_rows = len(values)
        num_columns = max(len(row) for row in values) if values else 0
        analysis = f"Number of rows: {num_rows}, Number of columns: {num_columns}"

        # Return analysis
        return {"summary": "Summary of the data analysis", "details": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
