from pathlib import Path
import datetime
import logging


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSheetsAPIAuthLogger:
    DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @classmethod
    def get_logger(cls, level=logging.INFO):
        return cls.create_logger(level)

    def create_logger(
        self, level=logging.INFO, name="GoogleSheetsAPIAuth"
    ) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)

        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(f"{name}.log")
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.DEBUG)

        c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        f_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        return logger


class GoogleSheetsAPIAuth:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self, auth_dir: Path = None) -> None:
        self.logger = GoogleSheetsAPIAuthLogger.get_logger(level=logging.DEBUG)
        self.creds: Credentials = None

        # Set default auth directory
        if auth_dir is None:
            self.logger.info("No auth directory provided, using default")
            auth_dir = Path(__file__).parent / "auth"

        self.creds_file = auth_dir / "credentials.json"
        self.token_file = auth_dir / "token.json"

        # If no credentials file, raise error
        if not self.creds_file.exists():
            self.logger.critical("No creds file")
            raise FileNotFoundError(
                f"Couldn't find 'credentials.json' in {self.creds_file}"
            )

        # Authenticate and refresh token if expired
        self.authenticate()

    def get_creds(self) -> Credentials:
        return self.creds

    def authenticate(self) -> None:
        self.logger.debug("Authentication flow started")
        if self.token_file.exists():
            try:
                self.creds = Credentials.from_authorized_user_file(
                    str(self.token_file), self.SCOPES
                )
            except Exception:
                self.logger.warning("Failed to find token")
                self.creds = None

        if not self.creds or not self.creds.valid:
            self.creds = self.refresh(self.creds)
        self.logger.debug("Authentication flow ended")

    def refresh(self, creds: Credentials) -> Credentials:
        if creds and creds.expired and creds.refresh_token:
            self.logger.info("Refreshing token")
            creds.refresh(Request())
        else:
            self.logger.debug("Presenting user with consent screen")
            flow = InstalledAppFlow.from_client_secrets_file(
                self.creds_file, self.SCOPES
            )
            creds = flow.run_local_server(port=0)
            with open(self.token_file, "w") as token:
                self.logger.debug("Writing token to file")
                token.write(creds.to_json())
        return creds


class GoogleSheetsAPI:
    def __init__(self, auth: GoogleSheetsAPIAuth = None, id: str = None) -> None:
        self.SPREADSHEET_ID = id
        try:
            self.creds = auth.get_creds()
        except AttributeError:
            raise AttributeError("No authenticator provided")

    def clean_values(self, data: dict) -> list[list]:
        # Get current time in ISO and formatted strings
        time_stamps = [
            datetime.datetime.now().isoformat(),
            datetime.datetime.now().strftime("%Y/%m/%d"),
        ]
        # Replace empty strings with None
        user_input = [None if value == "" else value for value in data.values()]
        return [time_stamps + user_input]

    def write(self, data: dict) -> None:
        body = {"values": self.clean_values(data)}

        try:
            service = build("sheets", "v4", credentials=self.creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            results = (
                sheet.values()
                .append(
                    spreadsheetId=self.SPREADSHEET_ID,
                    range="raw",
                    valueInputOption="RAW",
                    body=body,
                )
                .execute()
            )
            print(f"Updated {results.get('updates').get('updatedCells')} cells")

        except HttpError as err:
            print(err)


if __name__ == "__main__":
    data = {
        "firstName": "Blake",
        "lastName": "Nall",
        "assetName": "Blake's Ride",
        "email": "blakenall@proton.me",
        "imeiNumber": "123456789012345",
        "phoneNumber": "",
        "vinNumber": "1903480245034",
    }
    auth = GoogleSheetsAPIAuth()
    api = GoogleSheetsAPI(auth)
    api.write(data)
