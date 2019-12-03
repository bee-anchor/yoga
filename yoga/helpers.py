from collections import namedtuple
import random
import string

Locator = namedtuple("Locator", ["find_method", "selector"])


def random_string(length: int):
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def random_ascii_string(length: int):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))
