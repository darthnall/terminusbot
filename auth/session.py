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

    def search(self, category: str | None, keyword: str | None) -> dict | None:

        valid_categories = ['user']

        if category not in valid_categories:
            return None

        params = {
            "spec": {
                "itemsType": category,
                "propName": "sys_name",
                "propValueMask": "*",
                "sortType": "sys_name"
            },
            "force": 1,
            "flags": 1,
            "from": 0,
            "to": 0
        }

        if keyword is not None:
            params['spec']['propValueMask'] = f'*{keyword}*'

        response = self.wialon_api.core_search_items(**params)
        return response

    def create_user(self, username: str | None, password: str | None) -> dict | None:

        params = {
            "creatorId": 21438204,
            "name": username,
            "password": password,
            "dataFlags": 1
        }

        print(params)

        response = self.wialon_api.core_create_user(params)
        return response
