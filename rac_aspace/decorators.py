

def check_dictionary(func):
    def inner(*args, **kwargs):
        if not [isinstance(a, dict) for a in args]:
            raise TypeError('{} is not a dictionary'.format(args[0]))
        if not [a for a in args]:
            raise AttributeError('{} is empty'.format(args[0]))
        return func(*args, **kwargs)
    return inner


def check_list(func):
    def inner(*args, **kwargs):
        if not [isinstance(a, list) for a in args]:
            raise TypeError('{} is not a list'.format(args[0]))
        if [len(a) == 0 for a in args]:
            raise AttributeError('{} is empty'.format(args[0]))
        return func(*args, **kwargs)
    return inner


def check_str(func):
    def inner(*args, **kwargs):
        if not [isinstance(a, str) for a in args]:
            raise TypeError('{} is not a string'.format(args[0]))
        return func(*args, **kwargs)
    return inner
