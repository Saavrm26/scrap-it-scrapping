from functools import wraps, partial
from scrapping.utils.color_printing import prRed, prYellow, prGreen


def catch_exception(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        try:
            prYellow(f"Inside {f.__name__}")
            yield partial(f(self), *args, **kwargs)
        except Exception as e:
            prRed(e)
            prRed(f"At {f.__name__}")
        return wrapper
