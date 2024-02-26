from auth import Session
from . import gen_creds


class User(Session):
    def __init__(self, data: dict, session):
        self.session = session
        self.creds = gen_creds(data)

    def __repr__(self) -> str: return f'User credentials: {self.creds}'

    @property
    def email(self) -> str: return self.creds['email']

    @property
    def phone(self) -> str | None: return self.creds['phoneNumber']

    @property
    def id(self) -> int | None: return self.creds['userId']

    def create(self) -> dict:
        params = {
            "creatorId":27881459, # Terminus-1000's user id
            "name":self.creds['username'], # Generated username
            "password":self.creds['password'], # Generated password
            "dataFlags":1 # Default flags
        }
        response = self.session.wialon_api.core_create_user(**params)
        self.creds['userId'] = response['item']['id']
        return response

    def set_default_flags(self) -> bool:
        params = {
            "userId": self.id,
            "flags": 0x02,
            "flagsMask": 0x00
        }
        response = self.session.wialon_api.user_update_user_flags(**params)
        if response.status_code == 200:
            return True
        return False

    def email_creds(self):
        pass

    def assign_phone(self) -> bool:
        params = { "itemId": self.id, "phoneNumber": self.phone }
        response = self.session.wialon_api.unit_update_phone(**params)
        if print(f'Assigned phone number {self.phone} to user'):
            return True
        return False

if __name__ == '__main__':
    pass
