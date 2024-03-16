from googleapiclient.discovery import build
from fastapi import FastAPI, HTTPException
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

# Initialize FastAPI app
app = FastAPI()

# Google Sheets API setup
SERVICE_ACCOUNT_FILE = r"C:\Users\ASUSPC\Documents\programming\storyteller-ssmenu-pull-sheets-f80576101f4a.json"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Your Google Sheet ID
SHEET_ID = '1tJP4mFtH-2bkquzrWxKvfw-D8ZF0Geb-I70Zw2p8IjA'

@app.get("/read-analyze-sheet/")
async def read_analyze_sheet(range: str):
    try:
        # Read data from the specified range
        result = sheet.values().get(spreadsheetId=SHEET_ID,
                                    range=range).execute()
        values = result.get('values', [])

        if not values:
            raise HTTPException(status_code=404, detail="No data found.")

        # Analyze data (this part will depend on your specific analysis requirements)
        analysis = "Data analysis results here."

        # Return analysis
        return {"summary": "Summary of the analysis", "details": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
