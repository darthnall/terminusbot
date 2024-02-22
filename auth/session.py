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

    def token_list(self) -> dict: return self.wialon_api.token_list({"userId":27881459})

    def set_sms(self, user_id: str) -> dict:
        params = {
            "userId":user_id,
            "flags":0x20,
            "flagsMask":0x00
        }
        response = self.wialon_api.user_update_user_flags(**params)
        return response

    def create_user(self, creds: dict | None) -> dict | None:

        # TODO: Email user credentials to user
        email = creds['email']
        # TODO: Assign resource to new user
        imei = creds['imei']

        params = {
            "creatorId":27881459, # Terminus-1000's user id
            "name":creds['username'], # Generated username
            "password":creds['password'], # Generated password
            "dataFlags":1 # Default flags
        }

        print(params)

        response = self.wialon_api.core_create_user(**params)
        return response
