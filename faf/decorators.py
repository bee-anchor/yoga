import functools
from colorama import Fore


def scenario(description):
    def decorator_test(func):
        @functools.wraps(func)
        def wrapper_test(*args, **kwargs):
            print(Fore.CYAN + '\n-----------------------------------------------------')
            print(Fore.LIGHTCYAN_EX + description + Fore.RESET)
            return func(*args, **kwargs)
        return wrapper_test
    return decorator_test


def step(description):
    def decorator_step(func):
        @functools.wraps(func)
        def wrapper_step(*args, **kwargs):
            print(Fore.LIGHTMAGENTA_EX + description + Fore.RESET)
            return func(*args, **kwargs)
        return wrapper_step
    return decorator_step



