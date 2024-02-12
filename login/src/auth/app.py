from dotenv import load_dotenv
from requests import codes
import requests
import os
load_dotenv()

url = f'https://hosting.wialon.com/login.html'

# NOTE: Wialon's authentication page expects:
# login = Wialon Hosting username
# passw = Wialon Hosting password

data = {
    'login': 'Blake@terminusgps.com',
    'passw': os.environ['WIALON_HOSTING_PASSWORD']
}

with requests.Session() as s:
    r = s.get(url, data=data)
    if codes.ok:
        print('done')
    else:
        print('something went wrong')
