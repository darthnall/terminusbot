from auth import AuthSession
from dotenv import load_dotenv
import os

load_dotenv()

s = AuthSession(access_token=os.environ['WIALON_HOSTING_API_TOKEN'])
print(s)
