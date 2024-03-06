import os

import dotenv

import wialon


class Session:
    def __init__(self, token: str) -> None:
        self.wialon_api = wialon.Wialon()
        self._token = token

    def __enter__(self):
        login = self.wialon_api.token_login(token=self._token)
        self.wialon_api.sid = login["eid"]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> str | None:
        __err = f"{exc_type = }, {exc_val = }, {exc_tb = }"
        self.wialon_api.core_logout()
        if exc_type is not None:
            return __err
        return None

    @property
    def sid(self) -> str:
        return self.wialon_api.sid
