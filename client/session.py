from auth import Session

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
    def email(self, creds) -> str: return creds['email']

    @property
    def phone(self, creds) -> str: return creds['phoneNumber']

    def create(self) -> dict:
        pass

    def set_flags(self) -> bool:
        pass

    def create_password(self, length: int) -> str | False:
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
    def email_creds(self, creds)
