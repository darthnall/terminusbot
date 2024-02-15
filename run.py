from auth import Session
from dotenv import load_dotenv
from pprint import pprint
import os
import pprint

load_dotenv()

def main():
    token = os.environ['WIALON_HOSTING_API_TOKEN']
    try:
        with Session(token=token) as session:
            params = { 'type': 1 }
            pprint(session.get_account_data(params=params))
    except WialonError as e:
        print(f'Error code {e._code}, msg: {e._text}')

if __name__ == "__main__":
    main()
