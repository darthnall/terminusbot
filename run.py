from auth import AuthSession
from dotenv import load_dotenv
import os
import pprint

if __name__ == "__main__":
    load_dotenv()
    with AuthSession(access_token=os.environ['WIALON_HOSTING_API_TOKEN']) as session:
        pprint.pprint(session.create_user(username='iwascreatedbypython', password='Terminusgps@1', flags=1))
