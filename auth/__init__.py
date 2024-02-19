import dotenv
import os
from auth.session import Session

dotenv.load_dotenv()

token = os.environ['WIALON_HOSTING_API_TOKEN_DEV']

def query(keyword: str | None) -> dict | None:
    if keyword is None:
        return {
            "spec": {
                "itemsType": "user",
                "propName": "sys_name",
                "propValueMask": "*",
                "sortType": "sys_name"
            },
            "force": 1,
            "flags": 1,
            "from": 0,
            "to": 0
        }
    else:
        return {
            "spec": {
                "itemsType": "user",
                "propName": "sys_name",
                "propValueMask": f"*{keyword}*",
                "sortType": "sys_name"
            },
            "force": 1,
            "flags": 1,
            "from": 0,
            "to": 0
        }
    return None

PARAMETERS = {
        "core": {
            "get_items_access": {
                "userId": os.environ['WIALON_HOSTING_CREATOR_ID_DEV'],
                "directAccess": False,
                "itemSuperClass": 'user',
                "flags": 1
            },
            "get_account_data": {
                "type": 1
            },
        },
        "user": {
            "send_sms": {
                "phoneNumber": "79000000000",
                "smsMessage": "Hello, World!"
            },
        },
}
