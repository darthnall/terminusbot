import requests
import os
import json
import urllib.parse
from dotenv import load_dotenv
from auth.url import make_url
import logging
import datetime

# Load environment variables and set up logging
load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(
        filename=f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}-session.log',
        format='[%(levelname)s] [%(asctime)s]: %(message)s',
        level=logging.DEBUG
)


class AuthSession:
    def __init__(self, access_token: str):
        # Required headers for all requests
        self.headers = { "Content-Type": "application/x-www-form-urlencoded" }
        # Access token for authentication, must be provided
        self.access_token = access_token

    def __enter__(self):
        # Login to wialon api using provided access token
        svc = 'token/login'
        params = {
            "token":self.access_token,
            "fl":1
        }
        url = make_url(sid=None, svc=svc, params=params)
        logging.debug(f'login url: {url}')
        # Retrieve session id from response
        response = requests.get(url=url, headers=self.headers)
        r = response.json()

        try:
            self.sid = r['eid']
            logger.info(f'login success')
            logger.info(f'session eid: {r["eid"]}')
        except KeyError:
            logger.critical(f'unexpected response')
            logger.critical(f'response: {r}')

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        # If session interrupted, log exception and traceback
        if exception_type is not None:
            logger.critical(f'session interrupted by exception')
            logger.critical(f'exception: {exception_type} {exception_value} {traceback}')
            return False

        # Gracefully logout of session
        svc = 'core/logout'
        params = {}
        url = make_url(sid=self.sid, svc=svc, params=params)
        logging.debug(f'logout url: {url}')
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            logger.critical(f'logout failed')
            logger.critical(f'response: {response.json()}')
            return False
        else:
            logger.info(f'logout success')
            logger.info(f'session eid: {self.sid}')
            logger.debug(f'response: {response.json()}')
        return True

    def __repr__(self):
        details = {
            "access_token": self.access_token,
            "eid": self.sid
        }
        return json.dumps(details)

    def get_account_data(self, flags: int = 1, flag: int = 1) -> dict | None:
        # Get account data of current authenticated user
        valid_flags = [1, 2]
        if flag:
            flags = flag

        if flags not in valid_flags:
            print(f'Invalid flags: {flags}\nuse 1 or 2')
            return None

        svc = 'core/get_account_data'
        params = { "type": flags }
        url = make_url(sid=self.sid, svc=svc, params=params)
        response = requests.get(url=url, headers=self.headers)
        return response.json()

    def create_user(self, username: str, password: str, flags: int, flag: int) -> dict | None:
        # TODO: Finish writing this function, these flags are random numbers I chose
        valid_flags = [1, 4, 32]
        if flag:
            flags = flag
        if flags not in valid_flags:
            logger.warn(f'Invalid flags: {flags}')
            logger.warn(f'use 1, 4, or 32')
            return None

        svc = 'core/create_user'
        params = {
            "creatorId":os.environ['CREATOR_ID'],
            "name":username,
            "password":password,
            "dataFlags":flags
        }
        url = make_url(sid=self.sid, svc=svc, params=params)
        response = requests.get(url=url, headers=self.headers)
        return response.json()

    def get_token_list(self) -> dict | None:
        svc = 'token/list'
        params = {}
        url = make_url(sid=self.sid, svc=svc, params=params)
        response = requests.get(url=url, headers=self.headers)
        return response.json()


#   TODO: Automatically refresh token when it expires (30 days)
    def refresh_token(self, user: str, passw: str, access_token: str | None) -> str | None:
        pass
