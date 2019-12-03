import functools
from colorama import Fore


def scenario(description: str):
    def decorator_test(func):
        @functools.wraps(func)
        def wrapper_test(*args, desc_print=True, **kwargs):
            if desc_print:
                print(Fore.CYAN + '\n-----------------------------------------------------')
                print(Fore.LIGHTCYAN_EX + description + Fore.RESET)
            return func(*args, **kwargs)

        return wrapper_test

    return decorator_test


def step(description: str):
    def decorator_step(func):
        @functools.wraps(func)
        def wrapper_step(*args, desc_print=True, **kwargs):
            if desc_print:
                print(Fore.LIGHTMAGENTA_EX + description.format(*args, *list(kwargs.values())) + Fore.RESET)
            return func(*args, **kwargs)

        return wrapper_step

    return decorator_step
