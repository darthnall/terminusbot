from os import environ as env


class Config:
    EMAIL_PASSWORD = env["EMAIL_PASSWORD"]
    SECRET_KEY = env["SECRET_KEY"]
    WIALON_HOSTING_API_TOKEN = env["WIALON_HOSTING_API_TOKEN"]
    SPREADSHEET_ID = env["SPREADSHEET_ID"]
