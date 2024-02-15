import dotenv
import os
from pprint import pprint
from wialon import Wialon, WialonError

dotenv.load_dotenv()
wialon_api = Wialon()

token = os.environ['WIALON_HOSTING_API_TOKEN']
login = wialon_api.token_login(token=token)
wialon_api.sid = login['eid']

class Session:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.login = wialon_api.token_login(token=access_token)
        self.sid = self.login['eid']
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        wialon_api.core_logout()

    def create_unit():
        return response

    # Does not provide user ID, only billing information for user
    def get_account_data(_type: int):
        response = wialon_api.core_get_account_data(
            type=_type
        )
        return response

    def create_user(creatorId: int, name: str, password: str, dataFlags: int):
        response = wialon_api.core_create_user(
                creatorId=creatorId,
                name=name,
                password=password,
                dataFlags=dataFlags
        )
        return response

    def search_items(itemsType: str, propName: str, propValueMask: str, sortType: str, force: int, flags: int):
        response = wialon_api.core_search_items(
            itemsType=itemsType,
            propName=propName,
            propValueMask=propValueMask,
            sortType=sortType,
            force=force,
            flags=flags,
        )
        return response




if __name__ == '__main__':
    try:
        #password = 'Pa%24%24w0rd'
        #response = create_user(creatorId=os.environ['CREATOR_ID'], name='test_user', password=password, dataFlags=2)
        response = search_items(itemsType='user', propName='sys_name', propValueMask='AJ Exotic', sortType='sys_name', force=1, flags=1)
        pprint(response)
        wialon_api.core_logout()
    except WialonError as e:
        print(e)
