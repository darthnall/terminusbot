from config import Config
from pathlib import Path

from .errors import LightMetricsError as error

import requests
from requests.models import Response


class LightMetrics:
    class LightMetricsCredentials:
        def __init__(self, filepath: Path = None) -> None:
            if filepath is None:
                self.username = Config.LIGHTMETRICS_USERNAME
                self.passw = Config.LIGHTMETRICS_PASSW

            return None

    class LightMetricsRefreshToken:
        def __init__(self, value: str, expires_in: int) -> None:
            self.value = value
            self._expires_in = expires_in

        def __str__(self) -> str:
            return self.value

        @property
        def expires_in(self) -> int:
            return self._expires_in


    def __init__(self, credentials: LightMetricsCredentials = None) -> None:
        self.base_url: str = "https://api.lightmetrics.co/v1"
        self.headers: dict = { "Content-Type": "application/json" }
        self.access_token: str = None
        self.refresh_token: self.LightMetricsRefreshToken = None
        self.id_token: str = None
        self.is_authenticated: bool = False

        if credentials is None:
            credentials = self.LightMetricsCredentials()

        auth_response = self.authorize(credentials=credentials)
        self.post_auth(auth_response, auth_response.status_code)

        return None

    def post_auth(self, response: Response, status_code: int) -> None:
        match status_code:
            case 200:
                self.access_token = response.get("access_token")
                self.id_token = response.get("id_token")
                self.refresh_token = self.LightMetricsRefreshToken(
                    response.get("refresh_token"),
                    response.get("expires_in")
                )

                self.headers.update({
                    "authorization": f"bearer {self._access_token}",
                    "id-token": self._id_token,
                })

                self.is_authenticated = True

            case 401:
                raise error.UnauthorizedRequestError

            case _:
                raise error.UnexpectedStatusCodeError

        return None

    def authorize(self, credentials: LightMetricsCredentials) -> Response:
        url = "https://api.lightmetrics.co/v1/auth/oauth2/token"
        json_data = {
            "grant_type": "password",
            "username": credentials.username,
            "password": credentials.passw,
        }

        response = requests.post(
            url=url,
            headers=self.headers,
            json=json_data,
        )

        return response
