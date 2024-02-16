from auth import Session
from pprint import pprint
from wialon import WialonError
import dotenv
import os
import pprint

dotenv.load_dotenv()

def main():
    token = os.environ['WIALON_HOSTING_API_TOKEN']
    try:
        with Session(token=token) as session:
            #params = { 'type': 1 }
            #pprint(session.get_account_data(params=params))

            params = {
                'creatorId': os.environ['CREATOR_ID'],
                'name': 'iwascreatedbypython',
                'password': 'Terminus@!',
                'dataFlags': 2
            }
            pprint(session.create_user(params=params))
    except WialonError as e:
        print(f'Error code {e._code}, msg: {e._text}')

if __name__ == "__main__":
    main()
