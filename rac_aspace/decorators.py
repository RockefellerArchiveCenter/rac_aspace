

def check_dictionary(func):
    def inner(*args, **kwargs):
        if not [isinstance(a, dict) for a in args]:
            raise TypeException('{} is not a dictionary'.format(args[0])
        return func(*args, **kwargs)
    return inner
