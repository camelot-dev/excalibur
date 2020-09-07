import random
import string
import uuid


def generate_uuid():
    return str(uuid.uuid4())


def random_string(length):
    ret = ""
    while length:
        ret += random.choice(
            string.digits + string.ascii_lowercase + string.ascii_uppercase
        )
        length -= 1
    return ret
