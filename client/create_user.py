import string
import random

def gen_creds(data: dict) -> tuple | None:

    username = f'{data["firstName"].lower()}.{data["lastName"].lower()}'

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

if __name__ == "__main__":
    print(create_user(firstname='Blake',lastname='Nall',email='blakenall@proton.me'))
