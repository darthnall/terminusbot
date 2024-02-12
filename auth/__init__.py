import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

class AuthSession:
    def __init__(self, access_token: str | None):
        self.headers = { "Content-Type": "application/x-www-form-urlencoded" }
        if access_token is not None:
            self.access_token = access_token
        try:
            with open('data.json', 'r') as data:
                data = json.load(data)
            try:
                params = {
                    "token": access_token,
                    "fl": 1
                }
                print(params)
                url = f'https://hst-api.wialon.com/wialon/ajax.html?svc=token/login&params={params}'
                response = requests.get(url=url, headers=self.headers)
                print(response.json())
            except requests.JSONDecodeError:
                print('Error: JSONDecodeError')
        except FileNotFoundError:
            print('data.json not found')

    def __repr__(self):
        if self.access_token is None:
            return f'access_token: None'
        else:
            return f'access_token: {self.access_token}'

    def token_update(self, **kwargs: str) -> str | None:
        for key, value in kwargs.items():
            if key == 'access_token':
                self.access_token = value
                return self.access_token
            else:
                return None

    def get_token(self, access_token: str | None, fl: int) -> str | None:
        try:
            svc = 'token/login'
            params = {
                "token": access_token,
                "fl": fl
            }
            url = f'https://hst-api.wialon.com/wialon/ajax.html?svc={svc}&params={params}'
            response = requests.get(url, headers=self.headers)
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
    session.get_token(access_token=os.environ['WIALON_HOSTING_API_KEY'], fl=1)
