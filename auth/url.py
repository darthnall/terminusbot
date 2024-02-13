import urllib
from urllib.parse import urlencode
from urllib.parse import quote
import json

def make_url(svc: str, params: dict, sid: str | None) -> str | None:
    s_params = json.dumps(params)
    s_params.replace(' ', '')
    print(s_params)
    params = urllib.parse.quote(s_params, safe='{}:/?&"')
    if sid is None:
        url = f'https://hst-api.wialon.com/wialon/ajax.html?svc={svc}&params={params}'
        print(url)
        return url
    url = f'https://hst-api.wialon.com/wialon/ajax.html?svc={svc}&sid={sid}&params={params}'
    return url

if __name__ == '__main__':
    params = {
        "callMode":"create",
        "app":"terminusgps",
        "at":0,
        "dur":0,
        "fl":-1,
        "p":"{}"
    }
    make_url(svc="token/update", params=params, sid=None)
