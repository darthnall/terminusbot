from auth import AuthSession
from dotenv import load_dotenv
import os
import pprint

if __name__ == "__main__":
    load_dotenv()
    with AuthSession(access_token=os.environ['WIALON_HOSTING_API_TOKEN']) as session:
        pprint.pprint(session.get_account_data(flag=1))
