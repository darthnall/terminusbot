from auth import Session
from dotenv import load_dotenv
from pprint import pprint
import os
import pprint

load_dotenv()

def main():
    with Session(access_token=os.environ['WIALON_HOSTING_API_TOKEN']) as session:
        _id = os.environ['CREATOR_ID']
        pprint(session.create_user(creatorId=_id, username='iwascreatedbypython', password='Terminusgps@1', flags=1))

if __name__ == "__main__":
    main()
