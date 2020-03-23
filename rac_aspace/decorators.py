

def check_dictionary(func):
    def inner(*args, **kwargs):
        if not isinstance(args[0], dict):
            raise TypeError('{} is not a dictionary'.format(args[0]))
        if not args[0]:
            raise AttributeError('{} is empty'.format(args[0]))
        return func(*args, **kwargs)
    return inner


def check_list(func):
    def inner(*args, **kwargs):
        if not [isinstance(args[0], list):
            raise TypeError('{} is not a list'.format(args[0]))
        if len(args[0]) == 0:
            raise AttributeError('{} is empty'.format(args[0]))
        return func(*args, **kwargs)
    return inner


def check_str(func):
    def inner(*args, **kwargs):
        if not isinstance(args[0], str):
            raise TypeError('{} is not a string'.format(args[0]))
        return func(*args, **kwargs)
    return inner
