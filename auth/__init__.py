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
    def get_account_data(self, _type: int):
        response = self.wialon_api.core_get_account_data(
            type=_type
        )
        return response

    def create_user(self, creatorId: int, name: str, password: str, dataFlags: int):
        response = self.wialon_api.core_create_user(
                creatorId=creatorId,
                name=name,
                password=password,
                dataFlags=dataFlags
        )
        return response

    def search_items(self, itemsType: str, propName: str, propValueMask: str, sortType: str, force: int, flags: int):
        response = self.wialon_api.core_search_items(
            {
                'spec': {
                    'itemsType': itemsType,
                    'propName': propName,
                    'propValueMask': propValueMask,
                    'sortType': sortType,
                    'force': force,
                    'flags': flags,
                    'from': 0,
                    'to': 0
                }
            }
        )
        return response




if __name__ == '__main__':
    token = os.environ['WIALON_HOSTING_API_TOKEN']
    try:
        with Session(token=token) as session:
            print('nice')
    except WialonError as e:
        print(f'Error code {e._code}, msg: {e._text}')
