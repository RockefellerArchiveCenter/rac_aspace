

def check_dictionary(func):
    def inner(*args, **kwargs):
        if not isinstance(args, dict):
            raise TypeException('{} is not a dictionary'.format(args[0])
        return func(*args, **kwargs)
    return inner
