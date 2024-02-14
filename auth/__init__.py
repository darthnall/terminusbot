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
        self.access_token = access_token

    def __enter__(self):
        svc = 'token/login'
        params = {
            "token":self.access_token,
            "fl":1
        }
        url = make_url(sid=None, svc=svc, params=params)
        response = requests.get(url=url, headers=self.headers)
        r = response.json()

        try:
            self.sid = r['eid']
            print(f'login success\n\neid: {r["eid"]}')
        except KeyError:
            print(r)

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            print(f'Exception: {exception_type} {exception_value} {traceback}')
            return False

        svc = 'core/logout'
        params = {}
        url = make_url(sid=self.sid, svc=svc, params=params)
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f'__exit__ Wialon response: {response.json()}')
            return False
        else:
            print(f'{response.json()}\n\nlogout success\n\neid: {self.sid}')
        return True

    def __repr__(self):
        details = {
            "access_token": self.access_token,
            "eid": self.sid
        }
        return json.dumps(details)

    def get_account_data(self, flags: int = 1, flag: int = 1) -> dict | None:
        valid_flags = [1, 2]
        if flag:
            flags = flag

        if flags not in valid_flags:
            print(f'Invalid flags: {flags}\nuse 1 or 2')
            return None

        svc = 'core/get_account_data'
        params = { "type":flags }
        url = make_url(sid=self.sid, svc=svc, params=params)
        response = requests.get(url=url, headers=self.headers)
        return response.json()

    def create_user(self, username: str, password: str, flags: int) -> dict | None:
        svc = 'core/create_user'
        params = {
            "creatorId":os.environ['CREATOR_ID'],
            "name":username,
            "password":password,
            "dataFlags":flags
        }
        url = make_url(svc=svc, sid=self.sid, params=params)
        response = requests.get(url=url, headers=self.headers)

    def get_token_list(self) -> list | None:
        svc = 'token/list'
        url = make_url(svc=svc, sid=self.sid, params=params)
        response = requests.get(url=url, headers=self.headers)
        print(response.json())


#   TODO: Automatically refresh token when it expires (30 days)
    def refresh_token(self, user: str, passw: str, access_token: str | None) -> str | None:
        pass
