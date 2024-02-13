import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

class AuthSession:
    def __init__(self, access_token: str | None):
        self.headers = { "Content-Type": "application/x-www-form-urlencoded" }
        params = {
            "token": access_token,
            "fl": 1
        }

        if access_token is None:
            print('Error: access_token is None')
            return None

        self.access_token = access_token

        try:
            url = make_url(svc='token/login', params=params)
            response = requests.get(url=url, headers=self.headers)
            print(response.json())
        except requests.JSONDecodeError:
            print('Error: JSONDecodeError')

    def __repr__(self):
        details = {
            "access_token": self.access_token,
        }
        return details

    def __exit__(self):
        pass

    def create_token(self) -> str | None:
        svc = 'token/update'
        params = {
            "callMode": "create",
            "app": "terminusgps",
            "at": 0,
            "dur": 0,
            "fl": -1,
            "p": "{}"
        }
        url = make_url(svc=svc, params=params, sid=None)
        response = requests.get(url=url, headers=self.headers)
        print(response.json())


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

def make_url(svc: str, params: dict, sid: str | None) -> str | None:
    if sid is None:
        url = f'https://hst-api.wialon.com/wialon/ajax.html?svc={svc}&params={params}'
        return url
    url = f'https://hst-api.wialon.com/wialon/ajax.html?svc={svc}&params={params}&sid={sid}'
    return url

if __name__ == '__main__':
    session = AuthSession(access_token=os.environ['WIALON_HOSTING_API_KEY'])
    session.create_token()
