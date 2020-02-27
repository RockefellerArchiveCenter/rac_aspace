

def check_dictionary(func):
    def inner(*args, **kwargs):
        if not isinstance(args, dict):
            print('Parameter is not a dictionary')
            return
        return func(*args, **kwargs)
    return inner
