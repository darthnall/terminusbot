import dotenv
import os
from pprint import pprint
from wialon import Wialon, WialonError

dotenv.load_dotenv()

class Session:
    def __init__(self, token: str):
        self.wialon_api = Wialon()
        self.token = token

    def __enter__(self):
        login = self.wialon_api.token_login(token=token)
        self.wialon_api.sid = login['eid']
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f'exc_type: {exc_type}, exc_val: {exc_val}, exc_tb: {exc_tb}')
            return False
        self.wialon_api.core_logout()
        print('logout successful')
        return True

    def __repr__(self):
        return f'Session(access_token={self.access_token})'

    def create_unit(self):
        return response

    # Does not provide user ID, only billing information for user
    def get_account_data(self, params: dict | None):
        if params is None:
            params = {}
        response = self.wialon_api.core_get_account_data(params=params)
        return response

    def create_user(self, params: dict | None):
        response = self.wialon_api.core_create_user(
                creatorId=creatorId,
                name=name,
                password=password,
                dataFlags=dataFlags
        )
        return response

    def search_items(self, params: dict | None):
        if params is None:
            params = {}
        response = self.wialon_api.core_search_items(params)
        return response




if __name__ == '__main__':
    token = os.environ['WIALON_HOSTING_API_TOKEN']
    try:
        with Session(token=token) as session:
            params = {
                    'type': 1
            }
            session.get_account_data()
    except WialonError as e:
        print(f'Error code {e._code}, msg: {e._text}')
