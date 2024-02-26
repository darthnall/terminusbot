import string
import random

def gen_username(email: str) -> str:
    username = email.split('@')
    return username[0]

def gen_password(length: int) -> str | bool:
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

    for i in range(length-3):
        password_list += random.choice(list(string.ascii_lowercase))
    password_list += random.choice(list(string.ascii_uppercase))
    password_list += random.choice(['!', '@', '#', '$'])
    password_list += str(random.choice(range(1, 9, 1)))
    return ''.join(password_list)

def gen_creds(data) -> dict | None:

    data = {t[0]: t[1] for t in data.items()}

    username = data['email']
    password = gen_password(length=12)

    creds = {
         'username': username,
         'password': password,
    }

    creds.update(data)
    return creds
