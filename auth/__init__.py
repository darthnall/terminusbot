import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

class AuthSession:
    def __init__(self, access_token):
        self.access_token = access_token

    def __repr__(self):
        return f'access_token: {self.access_token}'

    def get_token(self, user: str, passw: str) -> str | None:
        url = 'https://support.wialon.com/login.html'
        data = {
            'login': user,
            'passw': passw
        }

        with requests.Session() as s:
            r = s.get(url, data=data)
            if requests.codes.ok:
                return r.json()
            else:
                return None

# TODO: Automatically refresh token when it expires (30 days)
    def refresh_token(self, user: str, passw: str, access_token: str) -> str | None:
        with open('urls.json', 'r') as f:
            j = json.load(f)
            url = j['url']['refresh']
            print(url)

        data = {
            'login': user,
            'passw': passw
        }

        return data['login']

if __name__ == '__main__':
    auth = AuthSession(access_token=os.environ['WIALON_HOSTING_API_KEY'])
    token = auth.get_token(user='Blake@terminusgps.com', passw=os.environ['WIALON_HOSTING_PASSWORD'])
    print(token)
