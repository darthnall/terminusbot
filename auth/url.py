import urllib
from urllib.parse import urlencode
from urllib.parse import quote
import json

def make_url(svc: str, sid: str | None, params: dict) -> str | None:
    url = ['https://hst-api.wialon.com/wialon/ajax.html?']
    if sid:
        url.append(f'sid={sid}')
        url.append(f'&svc={svc}')
    else:
        url.append(f'svc={svc}')
    s_params = json.dumps(params)
    if params:
        s_params.replace(' ', '')
    params = urllib.parse.quote(s_params, safe='{}:/?&"')
    url.append(f'&params={params}')
    encoded_url= ''.join(url)
    print(f'generated url: {encoded_url}')
    return encoded_url
