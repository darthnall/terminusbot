import urllib
from urllib.parse import urlencode
from urllib.parse import quote
import json

def make_url(svc: str, **kwargs: str | dict | None) -> str | None:
    url = ['https://hst-api.wialon.com/wialon/ajax.html?', f'svc={svc}']
    for key, value in kwargs.items():
        if key == 'sid':
            url.append(f'&eid={value}')
        if key == 'params':
            s_params = json.dumps(value)
            s_params.replace(' ', '')
            params = urllib.parse.quote(s_params, safe='{}:/?&"')
            url.append(f'&params={params}')

    return ''.join(url)
