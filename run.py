from auth import AuthSession
from dotenv import load_dotenv
import os

load_dotenv()

s = AuthSession(access_token=os.environ['WIALON_HOSTING_API_TOKEN'])
s.create_user(username='iwascreatedbypython', password='terminusgps', flags=1)
