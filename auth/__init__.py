import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

class AuthSession:
    def __init__(self, access_token: str | None):
        try:
            with open('data.json', 'r') as data:
                self.data = json.load(data)
        except FileNotFoundError:
            print('data.json not found')
        if access_token is not None:
            self.access_token = access_token

    def __repr__(self):
        if self.access_token is None:
            return f'access_token: None'
        else:
            return f'access_token: {self.access_token}'

    def get_token(self, access_token: str | None, client_id: str, fl: int) -> str | None:
        try:
            svc = self.data['svc']['token']
            params = {
                "token": access_token,
                "operateAs": client_id,
                "fl": fl
            }
            url = f'https://hst-api.wialon.com/wialon/ajax.html?svc={svc}&params={params}'
            response = requests.get(url, headers=self.data['headers'])
            return response.json()
        except TypeError:
            return None

#   TODO: Automatically refresh token when it expires (30 days)
    def refresh_token(self, user: str, passw: str, access_token: str | None) -> str | None:

        data = {
            'login': user,
            'passw': passw
        }

        return data['login']


    def create_user(self, user_data: dict) -> dict | None:
        svc = 'core/create_user'
        params = {}
        url = f'https://hst-api.wialon.com/wialon/ajax.html?svc={svc}&params={params}'

if __name__ == '__main__':
    session = AuthSession(access_token=os.environ['WIALON_HOSTING_API_KEY'])
    session.get_token(access_token=os.environ['WIALON_HOSTING_API_KEY'], client_id=os.environ['WIALON_CLIENT_ID'], fl=1)
