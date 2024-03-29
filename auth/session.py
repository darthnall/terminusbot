from config import Config
from wialon import Wialon


class Session:
    def __init__(self) -> None:
        self.wialon_api = Wialon()
        self._token = Config.WIALON_HOSTING_API_TOKEN

    def __enter__(self):
        login = self.wialon_api.token_login(token=self._token)
        self.wialon_api.sid = login["eid"]
        self._sid = login["eid"]

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> str | None:
        self.wialon_api.core_logout()

        __err = f"{exc_type = }, {exc_val = }, {exc_tb = }"
        if exc_type is not None:
            return __err
        return None

    @property
    def sid(self) -> str:
        return self._sid
