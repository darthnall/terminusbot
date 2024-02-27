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

        print('Setting user flags...')
        if self.set_default_flags():
            print('User flags set to default')

        print('Setting Terminus-1000 permissions...')
        if self.set_creator_perms():
            print('Terminus-1000 permissions set')

        return response

    def set_creator_perms(self) -> bool:
        flags = [
            0x0001, # View item and basic properties
            0x0002, # View detailed item properties
            0x0004, # Manage access to this item
            0x0010, # Rename item
            0x0020, # View custom fields
            0x0040, # Manage custom fields
            0x0080, # Edit not mentioned properties
            0x0100, # Change icon
            0x0200, # Query reports or messages
            0x0400, # Edit ACL propagated items
            0x0800, # Manage item log
            0x1000, # View administrative fields
            0x2000, # Edit administrative fields
            0x4000, # View attached files
            0x8000  # Edit attached files
        ]
        params = {
            "userId": 27881459,
            "itemId": self.id,
            "accessMask": sum(flags)
        }
        response = self.session.wialon_api.user_update_item_access(**params)
        if response is None:
            return True
        return False

    def set_user_perms(self, unit_id: str) -> bool:
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
        response = self.session.wialon_api.user_update_user_flags(**params)
        if response is None:
            return True
        return False

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
        # TODO: Email credentials to user
        pass

    def assign_phone(self) -> bool:
        params = { "itemId": self.id, "phoneNumber": self.phone }
        response = self.session.wialon_api.unit_update_phone(**params)
        if response:
            print(f'Assigned phone number {self.phone} to user')
            return True
        return False
