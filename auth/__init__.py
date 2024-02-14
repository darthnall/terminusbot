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
        filename=f'./auth/logs/session.log',
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
        response = requests.post(url=url, headers=self.headers)
        r = response.json()
        print(r)

        try:
            self.sid = r['eid']
            logger.info(f'login success')
            logger.info(f'session eid: {r["eid"]}')
        except KeyError:
            logger.error(f'unexpected response')
            logger.error(f'response: {r}')

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        # If session interrupted, log exception and traceback
        if exception_type is not None:
            logger.error(f'session interrupted by exception')
            logger.error(f'exception: {exception_type} {exception_value} {traceback}')
            return False

        # Gracefully logout of session
        svc = 'core/logout'
        params = {}
        url = make_url(sid=self.sid, svc=svc, params=params)
        logging.debug(f'logout url: {url}')
        response = requests.post(url=url, headers=self.headers)

        if response.status_code != 200:
            logger.warn(f'logout failed')
            logger.warn(f'response: {response.json()}')
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

    def get_account_data(self, flags: int = 1) -> dict | None:
        # Get account data of current authenticated user
        valid_flags = [1, 2]
        if flags not in valid_flags:
            logger.warn(f'Invalid flags: {flags}')
            logger.warn(f'use {valid_flags}')
            return None

        svc = 'core/get_account_data'
        params = { "type": flags }
        url = make_url(sid=self.sid, svc=svc, params=params)
        logging.debug(f'get_account_data url: {url}')
        response = requests.post(url=url, headers=self.headers)
        return response.json()

    def create_user(self, username: str, password: str, flags: int) -> dict | None:
        valid_flags = [1, 2, 4, 8, 32, 64]
        if flags not in valid_flags:
            logger.warn(f'Invalid flags: {flags}')
            logger.warn(f'use {valid_flags}')
            return None

        svc = 'core/create_user'
        params = {
            "creatorId":os.environ['CREATOR_ID'],
            "name":username,
            "password":password,
            "dataFlags":flags
        }

        # Log new user
        logging.info(f'Creating user {username}')
        logging.info(f'user parameters {params}')

        url = make_url(sid=self.sid, svc=svc, params=params)
        logging.debug(f'create_user url: {url}')
        response = requests.post(url=url, headers=self.headers)
        return response.json()

    def get_token_list(self) -> dict | None:
        svc = 'token/list'
        params = {}
        url = make_url(sid=self.sid, svc=svc, params=params)
        logging.debug(f'get_token_list url: {url}')
        response = requests.post(url=url, headers=self.headers)
        return response.json()
