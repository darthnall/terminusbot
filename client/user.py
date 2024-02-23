from auth import Session
from . import gen_creds

class User(Session):
    def __init__(self, data: dict):
        super().__init__()
        self.creds = gen_creds(data)

    def __repr__(self) -> str: return f'User credentials: {self.creds}'

    @property
    def email(self) -> str: return self.creds['email']

    @property
    def phone(self) -> str: return self.creds['phoneNumber']

    @property
    def id(self) -> int: return self.creds['userId']

    def create(self) -> dict:
        pass

    def set_flags(self) -> bool:
        pass

    def email_creds(self):
        pass

    def assign_phone(self) -> bool:
        params = { "itemId": self.id, "phoneNumber": self.phone }
        response = wialon_api.unit_update_phone(**params)
        if response['error'] == 0:
            return True
        return False

if __name__ == '__main__':
    data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@gmail.com",
        "phoneNumber": "1234567890"
    }
    user = User(data=data)
    if user.assign_phone():
        print('Assigned phone number to user')
