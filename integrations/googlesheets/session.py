from gspread import service_account
from datetime import datetime
from sheetconfig import SheetId

class GoogleSheetsLogger:
    def __init__(self, spreadsheet: SheetId) -> None:
        self.spreadsheet = spreadsheet
        self.gc = service_account()

    def __enter__(self):
        self.sheet = self.gc.open_by_key(self.spreadsheet)
        self.worksheet = self.sheet.get_worksheet_by_id(0)
        return self

    def __exit__(self, a, b, c) -> str | None:
        if a:
            return a

    def append_row(self, values: list) -> bool:
        success = False
        try:
            self.worksheet.append_row(values)
        except Exception as e:
            success = False
            print(e)
        else:
            success = True

        return success

def log_email(email: str) -> bool:
    with GoogleSheetsLogger(SheetId.SIGNUP_SHEET.value) as logger:
        logger.append_row([email, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

if __name__ == "__main__":
    if log_email("blake@terminusgps.com"):
        print("Email logged successfully")
