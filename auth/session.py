import wialon


class Session:
    def __init__(self, token: str) -> None:
        # Load the Wialon API wrapper
        self.wialon_api = wialon.Wialon()
        self._token = token

    def __enter__(self):
        # Login to the Wialon API
        login = self.wialon_api.token_login(token=self._token)
        self.wialon_api.sid = login["eid"]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> str | None:
        # Logout of the Wialon API
        self.wialon_api.core_logout()

        __err = f"{exc_type = }, {exc_val = }, {exc_tb = }"
        if exc_type is not None:
            return __err
        return None

    @property
    def sid(self) -> str:
        return self.wialon_api.sid
