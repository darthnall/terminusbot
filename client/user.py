from auth import Session
from . import EmailUser
from . import gen_creds


class User(Session):
    def __init__(self, data: dict, session: Session):
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
    def id(self) -> str | int | None: return self.creds['userId']

    @property
    def password(self) -> str: return self.creds['password']

    def create(self) -> dict:
        # TODO: Check if user exists
        params = {
            "creatorId": 27881459, # Terminus-1000's user id
            "name": self.username, # Generated username
            "password": self.password, # Generated password
            "dataFlags": 1 # Default flags
        }

        print('Creating user in Wialon...')
        response = self.session.wialon_api.core_create_user(**params)

        self.creds['userId'] = response['item']['id']
        print('Setting user flags')
        self.set_default_flags()
        #self.set_default_perms(unit_id=self.id)

        return response

    def set_default_perms(self, unit_id: str | int | None) -> None:
        flags = [
            0x0001, # View item and basic properties
            0x0002, # View detailed item properties
            0x0004, # Manage access to this item
            0x0010, # Rename item
            0x0100, # Change icon
            0x0200, # Query reports or messages
            0x4000  # View attached files
        ]
        params = {
            "userId": self.id,
            "itemId": unit_id,
            "accessMask": sum(flags)
        }
        self.session.wialon_api.user_update_item_access(**params)

    def set_default_flags(self) -> None:
        params = {
            "userId": self.id,
            "flags": 0x02,
            "flagsMask": 0x00
        }
        self.session.wialon_api.user_update_user_flags(**params)

    def email_creds(self, data: dict) -> bool:
        email = EmailUser(data=data)
        return email.send()

    def assign_phone(self) -> None:
        params = { "itemId": self.id, "phoneNumber": self.phone }
        self.session.wialon_api.unit_update_phone(**params)
