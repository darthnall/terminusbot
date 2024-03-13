from dataclasses import dataclass

from intuitlib.client import AuthClient

class QuickbooksSession:
    def __init__(self, client_id: str, client_secret: str, access_token: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

        self.auth_client = AuthClient(
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token=self.access_token
        )

    def __enter__(self):
        pass



@dataclass
class Customer:
    display_name: str
    primary_email_address: str
    given_name: str
    family_name: str
    telephone_number: str
    job: str | None = None

    def create(self) -> None:
        pass
