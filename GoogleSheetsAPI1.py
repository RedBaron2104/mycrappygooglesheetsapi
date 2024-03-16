from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# Initialize FastAPI app
app = FastAPI()

# Environment variables for Google Sheets API setup
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
SHEET_ID = os.getenv('GOOGLE_SHEET_ID')

# Check for necessary environment variables
if not SERVICE_ACCOUNT_FILE or not SHEET_ID:
    raise Exception("Necessary environment variables are not set.")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Request model
class SheetRange(BaseModel):
    range: str

# Response model
class AnalysisResult(BaseModel):
    summary: str
    details: str

@app.post("/read-analyze-sheet/", response_model=AnalysisResult)
async def read_analyze_sheet(request: SheetRange):
    try:
        result = sheet.values().get(spreadsheetId=SHEET_ID, range=request.range).execute()
        values = result.get('values', [])

        if not values:
            raise HTTPException(status_code=404, detail="No data found in the specified range.")

        num_rows = len(values)
        num_columns = max(len(row) for row in values) if values else 0
        analysis = f"Number of rows: {num_rows}, Number of columns: {num_columns}"

        return AnalysisResult(summary="Summary of the data analysis", details=analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
