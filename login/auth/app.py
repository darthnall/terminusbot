from dotenv import load_dotenv
from requests import codes
import requests
import os
from bs4 import BeautifulSoup
load_dotenv()

url = f'https://hosting.wialon.com/login.html'

data = {
    'login': 'Blake@terminusgps.com',
    'passw': os.environ['WIALON_HOSTING_PASSWORD']
}

with requests.Session() as s:
    r = s.get(url, data=data)
    soup = BeautifulSoup(r.text, 'html.parser')
    if codes.ok:
        print(soup.title)
        print('done')
    else:
        print('something went wrong')
