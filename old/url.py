import urllib
from urllib.parse import urlencode
from urllib.parse import quote
import json
import requests
import dotenv

dotenv.load_dotenv()

def make_url(sid: str | None, svc: str, params: dict, **kwargs) -> str | None:
    url = ['https://hst-api.wialon.com/wialon/ajax.html?']
    for key, value in kwargs.items():
        if key == 'cms':
            url = ['https://cms.wialon.com/wialon/ajax.html?']
    if sid:
        url.append(f'sid={sid}')
        url.append(f'&svc={svc}')
    else:
        url.append(f'svc={svc}')
    s_params = json.dumps(params)
    s_params.replace(' ', '')
    params = urllib.parse.quote(s_params, safe='{}:/?&"')
    url.append(f'&params={params}')
    encoded_url= ''.join(url)
    return encoded_url

def req(sid: str | None, svc: str, params: dict, **kwargs) -> dict | str:
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    if sid is None:
        payload = {
                'svc': svc,
                'params': params
        }
    else:
        payload = {
            'sid': sid,
            'svc': svc,
            'params': params
        }
    response = requests.post(url='https://hst-api.wialon.com/wialon/ajax.html?', data=payload, headers=headers)
    try:
        return response.json()
    except JSONDecodeError:
        return response.text
