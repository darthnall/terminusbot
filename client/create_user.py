import string
import random

def create_user(firstname: str, lastname: str, email: str) -> dict | None:
    username = f'{firstname.lower()}.{lastname.lower()}'

    while len(username) < 8:
        username += random.choice(string.digits)

    password = gen_pass(length=8)
    # Create the user in Wialon
    # Email user their credentials
    return True

def gen_pass(length: int) -> str | None:
    password_list = []
    for i in range(length-2):
        password_list += random.choice(list(string.ascii_lowercase))
    password_list += random.choice(list(string.ascii_uppercase))
    password_list += random.choice(['!', '@', '#', '$'])
    return ''.join(password_list)

if __name__ == "__main__":
    print(create_user(firstname='Blake',lastname='Nall',email='blakenall@proton.me'))
