import requests
import os
import json
import urllib.parse
from dotenv import load_dotenv
from auth.url import make_url

load_dotenv()

class AuthSession:
    def __init__(self, access_token: str | None):
        self.headers = { "Content-Type": "application/x-www-form-urlencoded" }
        params = {
            "token":access_token,
            "fl":1
        }

        if access_token is None:
            print('Error: access_token is None')
            return None

        self.access_token = access_token
        url = make_url(svc='token/login', params=params, sid=None)
        response = requests.get(url=url, headers=self.headers)
        r = response.json()

        try:
            self.sid = r['eid']
            print(f'login success\neid: {r["eid"]}')
        except KeyError:
            print(r)

    def __repr__(self):
        details = {
            "access_token": self.access_token,
            "eid": self.sid
        }
        return json.dumps(details)

    def __exit__(self):
        params = {}
        url = make_url(svc='core/logout', sid=self.sid, params=params)

    def create_token(self) -> str | None:
        svc = 'token/update'
        params = {
            "callMode":"create",
            "app":"terminusgps",
            "at":0,
            "dur":0,
            "fl":-1,
            "p":"{}"
        }
        url = make_url(svc=svc, params=params, sid=self.sid)
        response = requests.get(url=url, headers=self.headers)
        print(response.json())

    def create_user(self, username: str, password: str, flags: int) -> str | None:
        svc = 'core/create_user'
        params = {
            "creatorId":"terminusgps",
            "name":username,
            "password":password,
            "dataFlags":flags

        }
        url = make_url(svc=svc, sid=self.sid, params=params)
        print(url)
        response = requests.get(url=url, headers=self.headers)
        print(response.json())

    def get_token_list(self) -> list | None:
        svc = 'token/list'
        url = make_url(svc=svc, params=None, sid=self.sid)
        response = requests.get(url=url, headers=self.headers)
        print(response.json())


#   TODO: Automatically refresh token when it expires (30 days)
    def refresh_token(self, user: str, passw: str, access_token: str | None) -> str | None:

        data = {
            'login':user,
            'passw':passw
        }

        return data['login']

if __name__ == '__main__':
    session = AuthSession(access_token=os.environ['WIALON_HOSTING_API_TOKEN'])
