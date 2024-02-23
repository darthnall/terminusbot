import string
import random

def gen_username(first_name: str, last_name: str) -> str:
    first, last = first_name.lower(), last_name.lower()

    username = first + '.' + last

    while len(username) < 8:
        username += random.choice(string.digits)

    return username

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

    if length < 8:
        # TODO: Handle false return
        return False

    for i in range(length-3):
        password_list += random.choice(list(string.ascii_lowercase))
    password_list += random.choice(list(string.ascii_uppercase))
    password_list += random.choice(['!', '@', '#', '$'])
    password_list += str(random.choice(range(1, 9, 1)))
    return ''.join(password_list)

def gen_creds(data) -> dict | None:

    data = {t[0]: t[1] for t in data.items()}

    username = gen_username(data["firstName"], data["lastName"])
    password = gen_password(length=12)

    creds = {
             'username': username,
             'password': password,
             'email': data["email"],
             'imei': data["imei"],
             'phoneNumber': data["phoneNumber"],
             'userId': None
             }


    return creds
