import string
import random

def gen_creds(data) -> dict | None:

    data = {t[0]: t[1] for t in data.items()}
    print(data)

    first = data['firstName'].lower()
    last = data['lastName'].lower()

    username = first + '.' + last

    while len(username) < 8:
        username += random.choice(string.digits)

    password = gen_pass(length=12)

    creds = {
             'username': username,
             'password': password,
             'email': data["email"],
             'imei': data["num"]
             }

    return creds

def validate(data: dict | None) -> dict | None:
    if data is None:
        return None
    else:
        for key, value in data.items():
            if value == '':
                return None
        print(data)
        return data

def gen_pass(length: int) -> str | None:
    password_list = []
    for i in range(length-2):
        password_list += random.choice(list(string.ascii_lowercase))
    password_list += random.choice(list(string.ascii_uppercase))
    password_list += random.choice(['!', '@', '#', '$'])
    return ''.join(password_list)
