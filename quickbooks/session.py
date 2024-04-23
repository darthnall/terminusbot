from intuitlib.client import AuthClient

from quickbooks import Quickbooks

from quickbooks.objects.customer import Customer

from .config import Config

class QuickbooksSession:
    def __init__(self) -> None:
        self.auth_client = AuthClient(
            client_id=Config.QB_CLIENT_ID,
            client_secret=Config.QB_CLIENT_SECRET,
            access_token=Config.QB_ACCESS_TOKEN,
            environment="sandbox",
            redirect_uri="http://localhost:5000/callback"
        )

    def __enter__(self):
        self.client = Quickbooks(
            auth_client=self.auth_client,
            refresh_token=self.refresh_token,
            company_id=1
        )

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        if exc_type is not None:
            print(exc_type, exc_value, exc_traceback)

    def all_customers(self) -> list[Customer]:
        return [customer for customer in Customer.all(qb=self.client)]
