import urllib
from urllib.parse import urlencode
from urllib.parse import quote
import json

def make_url(svc: str, params: dict | None, sid: str | None) -> str | None:
    if params is None:
        url = f'https://hst-api.wialon.com/wialon/ajax.html?svc={svc}&eid={sid}'
        return url
    s_params = json.dumps(params)
    s_params.replace(' ', '')
    params = urllib.parse.quote(s_params, safe='{}:/?&"')
    if sid is None:
        url = f'https://hst-api.wialon.com/wialon/ajax.html?svc={svc}&params={params}'
        return url
    url = f'https://hst-api.wialon.com/wialon/ajax.html?svc={svc}&eid={sid}&params={params}'
    return url
