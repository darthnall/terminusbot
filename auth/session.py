import dotenv
import os
import wialon

class Session:
    def __init__(self, token: str):
        self.wialon_api = wialon.Wialon()
        self._token = token

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

    def __repr__(self) -> str: return f'{self = }'

    @property
    def sid(self) -> str: return self.wialon_api.sid

    @property
    def token(self) -> str: return self._token

    @property
    def token_list(self) -> dict: return self.wialon_api.token_list({"userId":27881459})
