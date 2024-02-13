import urllib
from urllib.parse import urlencode
from urllib.parse import quote
import json

def make_url(svc: str, sid: str, **kwargs: str | dict | None) -> str | None:
    url = ['https://hst-api.wialon.com/wialon/ajax.html?', f'svc={svc}', f'&eid={sid}']
    s_params = json.dumps(params)
    if params:
        s_params.replace(' ', '')
    params = urllib.parse.quote(s_params, safe='{}:/?&"')
    url.append(f'&params={params}')

    return ''.join(url)
