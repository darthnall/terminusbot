import random
import string


def gen_password(length: int) -> str:
    """
    Password requirements:
        - At least one lowercase letter
        - At least one number
        - At least one special character
        - At least one uppercase letter
        - Different from username
        - Minumum 8 charcters
    """
    password_list: list = []

    for i in range(length - 3):
        password_list += random.choice(list(string.ascii_lowercase))
    password_list += random.choice(list(string.ascii_uppercase))
    password_list += random.choice(["!", "@", "#", "$"])
    password_list += str(random.choice(range(1, 9, 1)))
    return "".join(password_list)
