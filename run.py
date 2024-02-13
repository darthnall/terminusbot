from auth import AuthSession
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    with AuthSession(access_token=os.environ['WIALON_HOSTING_API_TOKEN']) as session:
        print(session.get_account_data())
        #session.create_user(username='iwascreatedbypython', password='terminusgps', flags=1)
