import requests
import os
from dotenv import load_dotenv

load_dotenv()

class AuthSession:
    def __init__(self, access_token: str | None):
        if access_token is not None:
            self.access_token = access_token
        else:
            pass

    def __repr__(self):
        return f'access_token: {self.access_token}'

    def get_token(self, user: str, client_id: str, fl: int) -> str | None:
        url = f'http://support.wialon.com/login.html?client_id={client_id}&user={user}&flags={fl}'

# TODO: Automatically refresh token when it expires (30 days)
    def refresh_token(self, user: str, passw: str, access_token: str) -> str | None:

        data = {
            'login': user,
            'passw': passw
        }

        return data['login']


    def create_user(self, user_data: list[str]) -> list[str] | None:
        svc = 'core/create_user'
        url = f'https://hst-api.wialon.com/wialon/ajax.html?svc={svc}&params={"token": {access_token}}'

if __name__ == '__main__':
    session = AuthSession(access_token=os.environ['WIALON_HOSTING_API_KEY'])
