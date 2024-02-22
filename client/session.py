from auth import Session
from . import gen_creds

class User():
    def __init__(self, creds: dict, session: Session):
        self.creds = creds
        self.wialon_api = session.wialon_api

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f'exc_type: {exc_type}, exc_val: {exc_val}, exc_tb: {exc_tb}')
            return False
        self.wialon_api.core_logout()
        return True

    def __repr__(self) -> str: return f'{self.creds}'

    @property
    def email(self) -> str: return self.creds['email']

    @property
    def phone(self) -> str: return self.creds['phoneNumber']

    def create(self) -> dict:
        pass

    def set_flags(self) -> bool:
        pass

    def create_password(self, length: int) -> str | bool:
        """
        Password requirements:
            - At least one lowercase letter
            - At least one number
            - At least one special character
            - At least one uppercase letter
            - Different from username
            - Minumum 8 charcters
        """
        password_list = []

        if length < 8:
            # TODO: Handle false return
            return False

        for i in range(length-3):
            password_list += random.choice(list(string.ascii_lowercase))
        password_list += random.choice(list(string.ascii_uppercase))
        password_list += random.choice(['!', '@', '#', '$'])
        password_list += str(random.choice(range(1, 9, 1)))
        return ''.join(password_list)

    def email_creds(self):
        pass

    def assign_phone(self, item_id: int):
        params = { "itemId": item_id, "phoneNumber": self.phone }
        response = wialon_api.unit_update_phone(**params)
        return response

if __name__ == '__main__':
    pass
