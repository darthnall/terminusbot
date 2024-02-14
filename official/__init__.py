import dotenv
import os
from wialon import Wialon, WialonError

dotenv.load_dotenv()
token = os.environ['WIALON_HOSTING_API_TOKEN']

try:
    wialon_api = Wialon()
    response = wialon_api.token_login(token=token)
    wialon_api.sid = response['eid']

    response = wialon_api.avl_evts()
    print(response)

    wialon_api.core_logout()
except WialonError as e:
    print(e)
    pass
