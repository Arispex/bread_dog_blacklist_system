import random
import string


def random_str(l: int):
    s = string.digits + string.ascii_letters
    return "".join(random.choices(s, k=l))
