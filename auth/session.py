import dotenv
import os
import wialon

class Session:
    def __init__(self, token: str):
        self.wialon_api = wialon.Wialon()
        self.token = token

    def __enter__(self):
        login = self.wialon_api.token_login(token=self.token)
        self.wialon_api.sid = login['eid']
        print(f'Logged in with session id: {login["eid"]}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f'exc_type: {exc_type}, exc_val: {exc_val}, exc_tb: {exc_tb}')
            return False
        self.wialon_api.core_logout()
        return True

    def __repr__(self):
        return f'Session(access_token={self.access_token})'

    @property
    def sid(self) -> str: return self.wialon_api.sid

    def create_user(self, creds: dict | None) -> dict | None:

        params = {}

        email = creds['email']
        imei = creds['imei']

        params = {
            "creatorId": 21438204,
            "name": creds['username'],
            "password": creds['password'],
            "dataFlags": 1
        }

        response = self.wialon_api.core_create_user(**params)
        return response
