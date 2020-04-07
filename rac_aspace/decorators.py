from functools import wraps
def check_type(obj_type):
    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not isinstance(args[0], obj_type):
                raise TypeError("{} is not a {}".format(args[0], obj_type))
            return func(*args, **kwargs)
        return wrapper
    return real_decorator
