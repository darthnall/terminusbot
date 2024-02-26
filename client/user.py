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
    def username(self) -> str: return self.creds['email']

    @property
    def phone(self) -> str | None: return self.creds['phoneNumber']

    @property
    def id(self) -> int | None: return self.creds['userId']

    @property
    def password(self) -> str: return self.creds['password']

    def create(self) -> dict:
        # TODO: Check if user exists at this point
        params = {
            "creatorId": 27881459, # Terminus-1000's user id
            "name": self.username, # Generated username
            "password": self.password, # Generated password
            "dataFlags": 1 # Default flags
        }
        print('Creating user in Wialon...')
        response = self.session.wialon_api.core_create_user(**params)
        self.creds['userId'] = response['item']['id']
        print('Setting user flags...')
        self.set_default_flags()
        return response

    def set_default_flags(self) -> bool:
        params = {
            "userId": self.id,
            "flags": 0x02,
            "flagsMask": 0x00
        }
        response = self.session.wialon_api.user_update_user_flags(**params)
        if response:
            return True
        return False

    def email_creds(self) -> bool:
        pass

    def assign_phone(self) -> bool:
        params = { "itemId": self.id, "phoneNumber": self.phone }
        response = self.session.wialon_api.unit_update_phone(**params)
        if print(f'Assigned phone number {self.phone} to user'):
            return True
        return False
