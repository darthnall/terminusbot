import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

import os

class MailchimpApi:
    def __init__(self) -> None:
        self.client = MailchimpTransactional.Client(os.environ.get("MAILCHIMP_API_KEY"))

    def ping_users(self) -> str:
        return self.client.users.ping()

    def send_email(self, email):
        try:
            response = self.client.messages.send({"message": email})
            return response
        except ApiClientError as e:
            raise MailchimpApiError(str(e))

class MailchimpApiError(Exception):
    pass

if __name__ == "__main__":
    m = MailchimpApi()
    response = m.ping_users()
    print(response)
