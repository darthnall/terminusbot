import urllib
from urllib.parse import urlencode
from urllib.parse import quote
import json

def make_url(sid: str | None, svc: str, params: dict) -> str | None:
    url = ['https://hst-api.wialon.com/wialon/ajax.html?']
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
